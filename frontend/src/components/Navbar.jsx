function Navbar({ apiStatus, isOnline }) {
  return (
    <header className="topbar">
      <a className="brand" href="/" aria-label="Fullstack AI home">
        <span className="brand-mark">F</span>
        <span>Fullstack AI</span>
      </a>
      <div className={`service-status ${isOnline ? 'is-online' : ''}`}>
        <span className="status-dot" />
        API {apiStatus}
      </div>
    </header>
  )
}

export default Navbar
