export default function ProfileSection({ data }) {
  if (!data.posts) return null

  // Resume los acumulados del usuario usando solo las publicaciones analizadas.
  const totalLikes = data.posts.reduce((sum, p) => sum + (parseInt(p.likes) || 0), 0)
  const totalComments = data.posts.reduce((sum, p) => sum + (parseInt(p.comments) || 0), 0)
  const avgLikes = data.posts.length > 0 ? (totalLikes / data.posts.length).toFixed(0) : 0

  return (
    <section className="profile-section">
      <div className="profile-header">
        <div>
          <h2>{data.name || data.username}</h2>
          <p className="username">@{data.username}</p>
          {data.bio && <p className="bio">{data.bio}</p>}
        </div>
      </div>

      <div className="profile-stats">
        <div className="stat-card">
          <div className="stat-value">{data.posts_count}</div>
          <div className="stat-label">Publicaciones</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{data.followers}</div>
          <div className="stat-label">Seguidores</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{data.posts.length}</div>
          <div className="stat-label">Analizados</div>
        </div>
      </div>

      <div className="aggregate-stats">
        <div className="agg-stat">
          <span className="agg-icon">❤️</span>
          <span className="agg-value">{totalLikes.toLocaleString()}</span>
          <span className="agg-label">Likes Totales</span>
        </div>
        <div className="agg-stat">
          <span className="agg-icon">💬</span>
          <span className="agg-value">{totalComments.toLocaleString()}</span>
          <span className="agg-label">Comentarios Totales</span>
        </div>
        <div className="agg-stat">
          <span className="agg-icon">📈</span>
          <span className="agg-value">{avgLikes}</span>
          <span className="agg-label">Promedio Likes</span>
        </div>
      </div>
    </section>
  )
}
