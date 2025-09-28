import React, { useState } from 'react';
import './index.css';

function App() {
  const [form, setForm] = useState({
    name: '',
    skills: '',
    goals: '',
    work_experience: '',
    posts: ''
  });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResults(null);
    // Prepare payload
    const payload = {
      name: form.name,
      skills: form.skills.split(',').map(s => s.trim()).filter(Boolean),
      goals: form.goals.split(',').map(s => s.trim()).filter(Boolean),
      work_experience: form.work_experience.split(',').map(s => s.trim()).filter(Boolean),
      posts: form.posts.split(',').map(s => s.trim()).filter(Boolean)
    };
    try {
      const res = await fetch('http://127.0.0.1:8000/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      setResults(data);
    } catch (err) {
      setResults({ error: 'Failed to fetch recommendations.' });
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
      <div className="bg-white shadow-md rounded-lg p-8 w-full max-w-xl">
        <h1 className="text-2xl font-bold mb-4 text-center">LinkUp: Smart Networking</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input name="name" value={form.name} onChange={handleChange} placeholder="Your Name (optional)" className="w-full border rounded px-3 py-2" />
          <input name="skills" value={form.skills} onChange={handleChange} placeholder="Skills (comma separated)" className="w-full border rounded px-3 py-2" required />
          <input name="goals" value={form.goals} onChange={handleChange} placeholder="Goals (comma separated)" className="w-full border rounded px-3 py-2" required />
          <input name="work_experience" value={form.work_experience} onChange={handleChange} placeholder="Work Experience (comma separated)" className="w-full border rounded px-3 py-2" required />
          <input name="posts" value={form.posts} onChange={handleChange} placeholder="Recent Posts (comma separated)" className="w-full border rounded px-3 py-2" />
          <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition">{loading ? 'Finding...' : 'Find Who to Meet'}</button>
        </form>
        {results && (
          <div className="mt-6">
            {results.error ? (
              <div className="text-red-600">{results.error}</div>
            ) : (
              results.map((rec, idx) => (
                <div key={idx} className="bg-blue-50 rounded p-4 mb-4">
                  <div className="font-semibold">Meet: {rec.name}</div>
                  <div className="mb-2 text-gray-700">{rec.why}</div>
                  <div className="font-medium">Conversation Starters:</div>
                  <ul className="list-disc ml-6">
                    {rec.conversation_starters.map((s, i) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
