import React from 'react';

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    console.error('[Ecosphere ErrorBoundary]', error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          display: 'flex', flexDirection: 'column', alignItems: 'center',
          justifyContent: 'center', minHeight: '60vh', gap: '1rem', padding: '2rem'
        }}>
          <div style={{ fontSize: '3rem' }}>⚠️</div>
          <h2 style={{ color: '#c62828', margin: 0 }}>Page crashed — rendering error</h2>
          <p style={{ color: '#555', textAlign: 'center', maxWidth: '480px' }}>
            {this.state.error?.message || 'An unexpected error occurred while rendering this page.'}
          </p>
          <p style={{ color: '#777', fontSize: '0.85rem', textAlign: 'center' }}>
            Make sure the backend is running: <code>cd backend &amp;&amp; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload</code>
          </p>
          <button
            onClick={() => this.setState({ hasError: false, error: null })}
            style={{
              padding: '0.6rem 1.5rem', background: '#2e7d32', color: '#fff',
              border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 600
            }}
          >
            🔄 Try Again
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
