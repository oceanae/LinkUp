# LinkUp

LinkUp is a smart networking system that recommends people you should meet and provides contextual conversation starters, based on your skills, goals, and experience.

## Features
- **People You Should Meet:** Recommends members based on skills, goals, and activity using embeddings and similarity search.
- **Conversation Starters:** Generates 2–3 contextual icebreakers for each suggested connection.
- **Demo Data:** Uses fake AI-related LinkedIn-style profiles for demonstration.

## How to Run

### Backend (FastAPI)
1. Navigate to the `backend` directory:
   ```sh
   cd backend
   ```
2. (Optional) Create and activate a virtual environment:
   ```sh
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Mac/Linux
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Start the FastAPI server:
   ```sh
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.

### Frontend (React + Tailwind)
1. Navigate to the `frontend` directory:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the React app:
   ```sh
   npm start
   ```
   The app will open at `http://localhost:3000`.

## Usage
- Fill in your LinkedIn-style profile (skills, goals, work experience, posts) in the form.
- Click "Find Who to Meet" to get a recommended connection and conversation starters.

## Notes
- No real LinkedIn integration; all data is demo/fake.
- For best results, keep both backend and frontend running simultaneously.

---

Feel free to modify the fake profiles in `backend/main.py` for more diverse recommendations!
