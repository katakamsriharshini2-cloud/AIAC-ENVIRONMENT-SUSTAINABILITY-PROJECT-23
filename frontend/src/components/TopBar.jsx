import React, { useState, useEffect } from 'react';

export default function TopBar({ title }) {
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const formatted = now.toLocaleString('en-IN', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });

  return (
    <header className="topbar">
      <div className="topbar-title">{title}</div>
      <div className="topbar-actions">
        <span style={{ marginRight: '1.2rem', fontSize: '0.9rem' }}>📍 Warangal, Telangana</span>
        <span style={{ marginRight: '1.2rem', fontSize: '0.9rem' }}>🟢 System Online</span>
        <span style={{ fontSize: '0.85rem', opacity: 0.85 }}>{formatted}</span>
      </div>
    </header>
  );
}
