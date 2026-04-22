export default function PostsGrid({ posts }) {
  if (!posts || posts.length === 0) return null

  return (
    <section className="posts-section">
      <h3 className="section-title">📱 Publicaciones</h3>
      <div className="posts-grid">
        {/* Muestra cada post analizado con sus metricas principales. */}
        {posts.map((post, idx) => (
          <article key={idx} className="post-card">
            <div className="post-header">
              <span className="post-number">#{idx + 1}</span>
              <span className="post-date">{post.date}</span>
            </div>

            <div className="post-stats">
              <div className="post-stat">
                <span className="icon">❤️</span>
                <span className="value">{post.likes}</span>
              </div>
              <div className="post-stat">
                <span className="icon">💬</span>
                <span className="value">{post.comments}</span>
              </div>
            </div>

            {post.hashtags && post.hashtags.length > 0 && (
              <div className="hashtags">
                {post.hashtags.slice(0, 5).map((tag, i) => (
                  <span key={i} className="hashtag">#{tag}</span>
                ))}
              </div>
            )}

            <a href={post.url} target="_blank" rel="noopener noreferrer" className="post-link">
              Ver en Instagram →
            </a>
          </article>
        ))}
      </div>
    </section>
  )
}
