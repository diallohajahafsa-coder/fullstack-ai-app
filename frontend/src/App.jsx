import { useEffect, useState } from 'react'
import { analyzeText, getHealth } from './api'
import './App.css'

function App() {
  const [health, setHealth] = useState({ loading: true, data: null, error: '' })
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)

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

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setResult(null)
    setIsAnalyzing(true)

    try {
      setResult(await analyzeText(text))
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const apiStatus = health.loading
    ? 'Checking'
    : health.data
      ? 'Online'
      : 'Unavailable'

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="Fullstack AI home">
          <span className="brand-mark">F</span>
          <span>Fullstack AI</span>
        </a>
        <div className={`service-status ${health.data ? 'is-online' : ''}`}>
          <span className="status-dot" />
          API {apiStatus}
        </div>
      </header>

      <section className="hero">
        <p className="eyebrow">YOUR FULL-STACK STARTER</p>
        <h1>Ideas in. Insights out.</h1>
        <p className="hero-copy">
          A React interface connected to a Flask API, ready for your next AI
          feature.
        </p>
      </section>

      <section className="workspace" aria-labelledby="analyzer-title">
        <div className="section-heading">
          <div>
            <p className="eyebrow">EXPERIMENT 01</p>
            <h2 id="analyzer-title">Sentiment analyzer</h2>
          </div>
          <span className="demo-badge">RULE-BASED DEMO</span>
        </div>

        <form className="analyzer-form" onSubmit={handleSubmit}>
          <label htmlFor="analysis-text">What would you like to analyze?</label>
          <textarea
            id="analysis-text"
            maxLength={5000}
            onChange={(event) => setText(event.target.value)}
            placeholder="Type a short review or thought..."
            required
            rows={5}
            value={text}
          />
          <div className="form-footer">
            <span className="character-count">{text.length} / 5000</span>
            <button disabled={isAnalyzing || !text.trim()} type="submit">
              {isAnalyzing ? 'Analyzing...' : 'Analyze text'}
              {!isAnalyzing && <span aria-hidden="true">↗</span>}
            </button>
          </div>
        </form>

        {error && (
          <p className="message error-message" role="alert">
            {error}
          </p>
        )}

        {result && (
          <div className="result-card" role="status">
            <div className={`result-icon ${result.label}`}>
              {result.label === 'positive' ? '+' : result.label === 'negative' ? '−' : '·'}
            </div>
            <div className="result-copy">
              <span className="result-label">DEMO RESULT</span>
              <strong>{result.label}</strong>
              <span className="result-detail">
                Signal strength: {Math.round(result.strength * 100)}%
              </span>
            </div>
            <span className={`storage-tag ${result.stored ? 'saved' : ''}`}>
              {result.stored ? 'Saved to MongoDB' : 'Not saved'}
            </span>
          </div>
        )}

        <p className="demo-note">
          This starter uses a small keyword-based demo, not a trained AI model.
          Configure MongoDB to save analyses.
        </p>
      </section>

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

export default App
