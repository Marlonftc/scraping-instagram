import { useState } from 'react';

export default function SearchBar({ onComplete }) {
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username) return;
    setLoading(true);

    try {
      const res = await fetch('http://localhost:5000/api/scrape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username }),
      });

      if (!res.ok) {
        const text = await res.text();
        alert('Scraping failed: ' + text);
      } else {
        if (onComplete) onComplete();
      }
    } catch (err) {
      alert('Error contacting backend: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="search-bar" onSubmit={handleSubmit}>
      <input
        className="search-input"
        type="text"
        placeholder="Buscar usuario"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        aria-label="Instagram username"
      />
      <button className="search-button" type="submit" disabled={loading}>
        {loading ? 'Scraping…' : 'Buscar'}
      </button>
    </form>
  );
}
