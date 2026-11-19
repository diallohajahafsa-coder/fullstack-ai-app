import { useEffect, useState } from 'react'
import Navbar from '../components/Navbar'
import SentimentAnalyzer from '../components/SentimentAnalyzer'
import { getHealth } from '../services/api'

function Sentiment() {
  const [health, setHealth] = useState({ loading: true, data: null, error: '' })

  useEffect(() => {
    let active = true

    getHealth()
      .then((data) => {
        if (active) setHealth({ loading: false, data, error: '' })
      })
      .catch((requestError) => {
        if (active) {
          setHealth({ loading: false, data: null, error: requestError.message })
        }
      })

    return () => {
      active = false
    }
  }, [])

  const apiStatus = health.loading
    ? 'Checking'
    : health.data
      ? 'Online'
      : 'Unavailable'

  return (
    <main className="app-shell">
      <Navbar apiStatus={apiStatus} isOnline={Boolean(health.data)} />

      <section className="hero">
        <p className="eyebrow">YOUR FULL-STACK STARTER</p>
        <h1>Ideas in. Insights out.</h1>
        <p className="hero-copy">
          A React interface connected to a Flask API, ready for your next AI
          feature.
        </p>
      </section>

      <SentimentAnalyzer />

      <section className="tech-strip" aria-label="Technology stack">
        <div>
          <span className="tech-label">FRONTEND</span>
          <strong>React + Vite</strong>
        </div>
        <span className="stack-divider" aria-hidden="true">→</span>
        <div>
          <span className="tech-label">API</span>
          <strong>Python + Flask</strong>
        </div>
        <span className="stack-divider" aria-hidden="true">→</span>
        <div>
          <span className="tech-label">DATA</span>
          <strong>MongoDB optional</strong>
        </div>
      </section>

      {health.error && (
        <p className="health-message" role="status">
          {health.error}. Start the backend to use the analyzer.
        </p>
      )}
    </main>
  )
}

export default Sentiment
