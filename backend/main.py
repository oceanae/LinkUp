from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pydantic import BaseModel
from typing import List, Optional
import numpy as np


# Initialize FastAPI app first
app = FastAPI(title="LinkUp Backend")

# Allow CORS for frontend, configurable via env var
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Serve React static files
frontend_build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build'))
print("Serving React build from:", frontend_build_dir)
if os.path.exists(frontend_build_dir):
    print("Files in build:", os.listdir(frontend_build_dir))
else:
    print("Build directory not found!")
static_dir = os.path.join(frontend_build_dir, "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Catch-all route for React Router (serves index.html for non-API, non-static routes)
from fastapi import Request
from fastapi import HTTPException

@app.get("/{full_path:path}")
async def serve_react_app(full_path: str, request: Request):
    # Don't override API or static routes
    if full_path.startswith("api") or full_path.startswith("recommend") or full_path.startswith("profiles") or full_path.startswith("static"):
        raise HTTPException(status_code=404)
    index_path = os.path.join(frontend_build_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "index.html not found"}

# --- Fake AI-related LinkedIn profiles ---
FAKE_PROFILES = [
    {
        "id": 1,
        "name": "Alex Kim",
        "skills": ["AI Safety", "Machine Learning", "Python"],
        "goals": ["Build safe AI systems"],
        "work_experience": ["Researcher at OpenAI"],
        "posts": ["Excited about AI regulation!", "Working on robust ML models."]
    },
    {
        "id": 2,
        "name": "Samira Patel",
        "skills": ["AI Ethics", "NLP", "Data Science"],
        "goals": ["Promote ethical AI"],
        "work_experience": ["AI Policy at DeepMind"],
        "posts": ["AI ethics in startups.", "NLP for social good."]
    },
    {
        "id": 3,
        "name": "Jordan Lee",
        "skills": ["Reinforcement Learning", "AI Safety", "C++"],
        "goals": ["Advance RL safety"],
        "work_experience": ["Engineer at Anthropic"],
        "posts": ["RL for safe agents.", "Attending NeurIPS 2025!"]
    }
]

# --- Embedding simulation (replace with real model in prod) ---
def fake_embed(profile):
    # Simple hash-based embedding for demo
    text = ' '.join(profile.get(k, '') if isinstance(profile.get(k, ''), str) else ' '.join(profile.get(k, [])) for k in ["skills", "goals", "work_experience", "posts"])
    np.random.seed(abs(hash(text)) % (2**32))
    return np.random.rand(128)

# Precompute embeddings for fake profiles
for p in FAKE_PROFILES:
    p["embedding"] = fake_embed(p)

class ProfileInput(BaseModel):
    name: Optional[str] = None
    skills: List[str]
    goals: List[str]
    work_experience: List[str]
    posts: List[str] = []

class Recommendation(BaseModel):
    name: str
    why: str
    conversation_starters: List[str]

@app.post("/recommend", response_model=List[Recommendation])
def recommend(profile: ProfileInput):
    user_emb = fake_embed(profile.dict())
    # Compute cosine similarity
    def cosine(a, b):
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    scored = []
    for p in FAKE_PROFILES:
        sim = cosine(user_emb, p["embedding"])
        scored.append((sim, p))
    scored.sort(reverse=True, key=lambda x: x[0])
    top = [p for _, p in scored[:1]]  # Recommend top 1 for demo
    results = []
    for match in top:
        why = f"You share interests in {', '.join(set(profile.skills) & set(match['skills'])) or 'AI topics'}. {match['name']} is working on {', '.join(match['goals'])}."
        starters = []
        if set(profile.skills) & set(match['skills']):
            starters.append(f"Ask {match['name']} about their experience with {list(set(profile.skills) & set(match['skills']))[0]}.")
        if set(profile.goals) & set(match['goals']):
            starters.append(f"Discuss your shared goal: {list(set(profile.goals) & set(match['goals']))[0]}.")
        if match['posts']:
            starters.append(f"Mention their recent post: '{match['posts'][0]}'")
        if not starters:
            starters = [f"Ask {match['name']} about their work in AI."]
        results.append(Recommendation(name=match['name'], why=why, conversation_starters=starters))
    return results

@app.get("/profiles")
def get_profiles():
    return [{k: v for k, v in p.items() if k != "embedding"} for p in FAKE_PROFILES]
