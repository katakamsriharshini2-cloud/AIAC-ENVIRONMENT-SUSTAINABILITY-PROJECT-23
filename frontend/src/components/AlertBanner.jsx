import React from 'react';

export default function AlertBanner({ message, type = 'info', onDismiss }) {
  return (
    <div
      className={`alert-banner${type ? ` ${type}` : ''}`}
      style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '1rem' }}
    >
      <span style={{ flex: 1 }}>{message}</span>
      {onDismiss && (
        <button
          onClick={onDismiss}
          style={{
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            fontSize: '1rem',
            lineHeight: 1,
            padding: '0 0.25rem',
            opacity: 0.7,
          }}
          aria-label="Dismiss"
        >
          ✕
        </button>
      )}
    </div>
  );
}
