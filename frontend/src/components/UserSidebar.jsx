export default function UserSidebar({ users, selectedUser, onSelect }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h3>👥 Usuarios Scaneados</h3>
      </div>
      <div className="users-list">
        {/* Permite cambiar entre usuarios ya guardados en el JSON consolidado. */}
        {users.length > 0 ? (
          users.map(user => (
            <button
              key={user}
              className={`user-btn ${selectedUser === user ? 'active' : ''}`}
              onClick={() => onSelect(user)}
            >
              @{user}
            </button>
          ))
        ) : (
          <p className="no-users">Ejecuta el scraper para comenzar</p>
        )}
      </div>
    </aside>
  )
}
