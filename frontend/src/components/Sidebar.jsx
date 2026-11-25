import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const navItems = [
  { icon: '🏠', label: 'Dashboard', to: '/' },
  { icon: '🌬️', label: 'Air Quality', to: '/air-quality' },
  { icon: '💧', label: 'Water Quality', to: '/water-quality' },
  { icon: '🌤️', label: 'Weather', to: '/weather' },
  { icon: '📊', label: 'Analytics', to: '/analytics' },
  { icon: '🤖', label: 'AI Forecasting', to: '/ai-forecasting' },
  { icon: '⚙️', label: 'Optimization', to: '/optimization' },
  { icon: '🗺️', label: 'Map View', to: '/map' },
  { icon: '🦋', label: 'Biodiversity', to: '/biodiversity' },
  { icon: '🚨', label: 'Incidents', to: '/incidents' },
  { icon: '📡', label: 'Data Sources', to: '/data-sources' },
  { icon: '🌏', label: 'Public Portal', to: '/portal' },
];

const roleBadgeClass = {
  admin: 'badge badge-danger',
  officer: 'badge badge-warning',
  public: 'badge badge-success',
};

export default function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const role = user?.role || 'public';
  const badgeClass = roleBadgeClass[role] || 'badge badge-info';

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <span style={{ fontSize: '1.5rem' }}>🌿</span>
        <span style={{ marginLeft: '0.5rem', fontWeight: 700, letterSpacing: '0.03em' }}>
          ECOSPHERE AI
        </span>
      </div>

      <nav className="sidebar-nav">
        {navItems.map(({ icon, label, to }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}
          >
            <span style={{ marginRight: '0.65rem', fontSize: '1.1rem' }}>{icon}</span>
            {label}
          </NavLink>
        ))}
      </nav>

      {user && (
        <div
          className="sidebar-user"
          style={{
            marginTop: 'auto',
            padding: '1rem',
            borderTop: '1px solid rgba(255,255,255,0.15)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.4rem' }}>
            <span style={{ fontSize: '1.2rem' }}>👤</span>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div
                style={{
                  fontWeight: 600,
                  fontSize: '0.9rem',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                }}
              >
                {user.name || user.username || 'User'}
              </div>
              <span className={badgeClass} style={{ fontSize: '0.7rem' }}>
                {role.toUpperCase()}
              </span>
            </div>
          </div>
          <button
            className="btn btn-secondary btn-sm"
            onClick={handleLogout}
            style={{ width: '100%', marginTop: '0.4rem' }}
          >
            Logout
          </button>
        </div>
      )}
    </aside>
  );
}
