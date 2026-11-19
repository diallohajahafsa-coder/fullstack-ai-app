import { useState } from 'react'
import { analyzeText } from '../services/api'

function SentimentAnalyzer() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)

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

  return (
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
  )
}

export default SentimentAnalyzer
