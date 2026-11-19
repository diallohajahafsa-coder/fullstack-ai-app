const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

async function request(path, options) {
  const response = await fetch(`${API_BASE_URL}${path}`, options)
  let payload

  try {
    payload = await response.json()
  } catch {
    throw new Error('The API returned an invalid response.')
  }

  if (!response.ok) {
    throw new Error(payload.error || payload.message || 'The API request failed.')
  }

  return payload
}

export function getHealth() {
  return request('/health')
}

export function analyzeText(text) {
  return request('/sentiment', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  })
}
