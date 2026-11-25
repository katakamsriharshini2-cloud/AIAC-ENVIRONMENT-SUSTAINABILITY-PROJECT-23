import React from 'react';

export default function LoadingSpinner({ message = 'Loading...' }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '2rem' }}>
      <div
        style={{
          width: '36px',
          height: '36px',
          border: '3px solid #e0e0e0',
          borderTop: '3px solid #2e7d32',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite'
        }}
      />
      <style>
        {`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}
      </style>
      {message && <p style={{ marginTop: '0.8rem', color: '#666', fontSize: '0.9rem' }}>{message}</p>}
    </div>
  );
}
