import { useState, useEffect } from 'react';
import ProfileSection from './components/ProfileSection';
import PostsGrid from './components/PostsGrid';
import UserSidebar from './components/UserSidebar';
import SearchBar from './components/SearchBar';

function App() {
  const [profiles, setProfiles] = useState([]);
  const [data, setData] = useState(null);
  const [selectedUser, setSelectedUser] = useState(null);
  const [loading, setLoading] = useState(false);
  // La lista lateral se arma desde el JSON consolidado ya cargado.
  const users = profiles.map((entry) => entry.username);

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    // Carga una sola vez el archivo que resume todos los usuarios scrapeados.
    setLoading(true);
    try {
      const res = await fetch('/scraping_data.json');
      if (!res.ok) throw new Error('Failed to fetch users');

      const unifiedData = await res.json();
      const availableProfiles = Array.isArray(unifiedData)
        ? unifiedData.filter((entry) => entry && entry.username)
        : [];

      setProfiles(availableProfiles);
      if (availableProfiles.length > 0 && !selectedUser) {
        setSelectedUser(availableProfiles[0].username);
        setData(availableProfiles[0]);
      } else if (availableProfiles.length === 0) {
        setData(null);
      }
    } catch (error) {
      console.error('Error loading users:', error);
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  const loadUserData = (username) => {
    // Cambia el usuario activo reutilizando los datos ya cargados en memoria.
    setSelectedUser(username);
    setData(profiles.find((entry) => entry.username === username) || null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>📊 Instagram Scraper Dashboard</h1>
        {/* <p>Visual analysis of extracted data</p> */}
        <SearchBar onComplete={loadUsers} />
      </header>

      <div className="app-container">
        <UserSidebar users={users} selectedUser={selectedUser} onSelect={loadUserData} />

        <main className="main-content">
          {loading ? (
            <div className="loading"> Loading data...</div>
          ) : data ? (
            <>
              <ProfileSection data={data} />
              <PostsGrid posts={data.posts} />
            </>
          ) : (
            <div className="no-data">
              <p> No data to display</p>
              <small>Run: python main.py</small>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
