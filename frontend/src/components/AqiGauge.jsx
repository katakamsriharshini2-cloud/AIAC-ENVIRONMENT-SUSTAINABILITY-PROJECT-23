import React from 'react';

function getAqiMeta(aqi) {
  if (aqi <= 50)  return { color: '#4caf50', category: 'Good' };
  if (aqi <= 100) return { color: '#8bc34a', category: 'Satisfactory' };
  if (aqi <= 200) return { color: '#ffc107', category: 'Moderate' };
  if (aqi <= 300) return { color: '#ff9800', category: 'Poor' };
  if (aqi <= 400) return { color: '#f44336', category: 'Very Poor' };
  return { color: '#880e4f', category: 'Severe' };
}

export default function AqiGauge({ aqi, showLabel = true }) {
  if (aqi === null || aqi === undefined) {
    return (
      <div style={{ textAlign: 'center' }}>
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: '6rem',
            height: '6rem',
            borderRadius: '50%',
            background: '#ccc',
            color: '#fff',
            fontSize: '1.6rem',
            fontWeight: 700,
          }}
        >
          N/A
        </div>
        {showLabel && (
          <div style={{ marginTop: '0.5rem', fontWeight: 600, color: '#888' }}>Unknown</div>
        )}
      </div>
    );
  }

  const { color, category } = getAqiMeta(aqi);

  return (
    <div style={{ textAlign: 'center' }}>
      <div
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          width: '6rem',
          height: '6rem',
          borderRadius: '50%',
          background: color,
          color: '#fff',
          fontSize: '1.8rem',
          fontWeight: 700,
          boxShadow: `0 4px 16px ${color}55`,
        }}
      >
        {aqi}
      </div>
      {showLabel && (
        <div
          style={{
            marginTop: '0.5rem',
            fontWeight: 600,
            color: color,
            fontSize: '0.95rem',
          }}
        >
          {category}
        </div>
      )}
    </div>
  );
}
