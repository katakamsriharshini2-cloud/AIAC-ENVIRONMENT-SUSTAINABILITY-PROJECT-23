import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { authApi } from '../api/client';
import AlertBanner from '../components/AlertBanner';

export default function Login() {
  const [tab, setTab] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [role, setRole] = useState('public_user');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const { login, setAuthSession } = useAuth();
  const navigate = useNavigate();

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(email, password);
      navigate('/');
    } catch (err) {
      setError(err.message || 'Login failed. Please verify credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await authApi.register({
        email,
        password,
        full_name: fullName,
        role,
      });
      if (res.access_token && res.user) {
        if (setAuthSession) {
          setAuthSession(res.access_token, res.user);
        } else {
          login(res.access_token, res.user);
        }
      }
      navigate('/');
    } catch (err) {
      setError(err.message || 'Registration failed.');
    } finally {
      setLoading(false);
    }
  };

  const fillCreds = (demoEmail, demoPass) => {
    setEmail(demoEmail);
    setPassword(demoPass);
    setTab('login');
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #1b4d3e 0%, #2e7d32 50%, #0f2b20 100%)',
      padding: '1.5rem',
      fontFamily: 'Inter, system-ui, sans-serif'
    }}>
      <div style={{
        background: '#ffffff',
        borderRadius: '16px',
        boxShadow: '0 20px 40px rgba(0,0,0,0.25)',
        width: '100%',
        maxWidth: '460px',
        overflow: 'hidden'
      }}>
        <div style={{
          background: '#2e7d32',
          padding: '2rem 1.5rem 1.5rem',
          textAlign: 'center',
          color: '#ffffff'
        }}>
          <div style={{ fontSize: '2.5rem', marginBottom: '0.25rem' }}>🌿</div>
          <h1 style={{ margin: 0, fontSize: '1.6rem', fontWeight: 700, letterSpacing: '0.5px' }}>ECOSPHERE AI</h1>
          <p style={{ margin: '0.4rem 0 0', fontSize: '0.85rem', opacity: 0.9 }}>
            Smart Environmental Monitoring & Sustainability Platform
          </p>
        </div>

        <div style={{ display: 'flex', borderBottom: '1px solid #e0e0e0' }}>
          <button
            type="button"
            onClick={() => { setTab('login'); setError(null); }}
            style={{
              flex: 1,
              padding: '0.85rem',
              background: tab === 'login' ? '#ffffff' : '#f5f5f5',
              border: 'none',
              borderBottom: tab === 'login' ? '3px solid #2e7d32' : 'none',
              fontWeight: tab === 'login' ? 600 : 400,
              cursor: 'pointer',
              color: tab === 'login' ? '#2e7d32' : '#666'
            }}
          >
            Sign In
          </button>
          <button
            type="button"
            onClick={() => { setTab('register'); setError(null); }}
            style={{
              flex: 1,
              padding: '0.85rem',
              background: tab === 'register' ? '#ffffff' : '#f5f5f5',
              border: 'none',
              borderBottom: tab === 'register' ? '3px solid #2e7d32' : 'none',
              fontWeight: tab === 'register' ? 600 : 400,
              cursor: 'pointer',
              color: tab === 'register' ? '#2e7d32' : '#666'
            }}
          >
            Register Account
          </button>
        </div>

        <div style={{ padding: '1.75rem' }}>
          {error && <AlertBanner message={error} type="error" onDismiss={() => setError(null)} />}

          {tab === 'login' ? (
            <form onSubmit={handleLoginSubmit}>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.35rem', color: '#333' }}>
                  Email Address
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  placeholder="admin@ecosphere.org"
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.75rem',
                    borderRadius: '8px',
                    border: '1px solid #ccc',
                    fontSize: '0.9rem',
                    boxSizing: 'border-box'
                  }}
                />
              </div>

              <div style={{ marginBottom: '1.25rem' }}>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.35rem', color: '#333' }}>
                  Password
                </label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  placeholder="••••••••"
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.75rem',
                    borderRadius: '8px',
                    border: '1px solid #ccc',
                    fontSize: '0.9rem',
                    boxSizing: 'border-box'
                  }}
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="btn btn-primary"
                style={{ width: '100%', padding: '0.75rem', borderRadius: '8px', fontWeight: 600, fontSize: '0.95rem' }}
              >
                {loading ? 'Authenticating...' : 'Sign In to Dashboard'}
              </button>
            </form>
          ) : (
            <form onSubmit={handleRegisterSubmit}>
              <div style={{ marginBottom: '0.85rem' }}>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.35rem', color: '#333' }}>
                  Full Name
                </label>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  required
                  placeholder="Dr. Rajesh Kumar"
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.75rem',
                    borderRadius: '8px',
                    border: '1px solid #ccc',
                    fontSize: '0.9rem',
                    boxSizing: 'border-box'
                  }}
                />
              </div>

              <div style={{ marginBottom: '0.85rem' }}>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.35rem', color: '#333' }}>
                  Email Address
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  placeholder="officer@ecosphere.org"
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.75rem',
                    borderRadius: '8px',
                    border: '1px solid #ccc',
                    fontSize: '0.9rem',
                    boxSizing: 'border-box'
                  }}
                />
              </div>

              <div style={{ marginBottom: '0.85rem' }}>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.35rem', color: '#333' }}>
                  Password
                </label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  placeholder="••••••••"
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.75rem',
                    borderRadius: '8px',
                    border: '1px solid #ccc',
                    fontSize: '0.9rem',
                    boxSizing: 'border-box'
                  }}
                />
              </div>

              <div style={{ marginBottom: '1.25rem' }}>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.35rem', color: '#333' }}>
                  Role
                </label>
                <select
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.75rem',
                    borderRadius: '8px',
                    border: '1px solid #ccc',
                    fontSize: '0.9rem',
                    boxSizing: 'border-box',
                    background: '#fff'
                  }}
                >
                  <option value="public_user">Public Citizen / Researcher</option>
                  <option value="environmental_officer">Environmental Officer</option>
                </select>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="btn btn-primary"
                style={{ width: '100%', padding: '0.75rem', borderRadius: '8px', fontWeight: 600, fontSize: '0.95rem' }}
              >
                {loading ? 'Creating Account...' : 'Register Account'}
              </button>
            </form>
          )}

          <div style={{ marginTop: '1.5rem', paddingTop: '1.25rem', borderTop: '1px dashed #e0e0e0' }}>
            <p style={{ margin: '0 0 0.5rem', fontSize: '0.78rem', fontWeight: 600, color: '#666', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
              Quick Demo Accounts
            </p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
              <button
                type="button"
                onClick={() => fillCreds('admin@ecosphere.org', 'Admin@123456')}
                style={{
                  textAlign: 'left',
                  background: '#f9f9f9',
                  border: '1px solid #e0e0e0',
                  borderRadius: '6px',
                  padding: '0.45rem 0.7rem',
                  fontSize: '0.8rem',
                  cursor: 'pointer'
                }}
              >
                <strong>Admin:</strong> admin@ecosphere.org <span style={{ opacity: 0.6 }}>(Admin@123456)</span>
              </button>
              <button
                type="button"
                onClick={() => fillCreds('officer@ecosphere.org', 'Officer@123456')}
                style={{
                  textAlign: 'left',
                  background: '#f9f9f9',
                  border: '1px solid #e0e0e0',
                  borderRadius: '6px',
                  padding: '0.45rem 0.7rem',
                  fontSize: '0.8rem',
                  cursor: 'pointer'
                }}
              >
                <strong>Officer:</strong> officer@ecosphere.org <span style={{ opacity: 0.6 }}>(Officer@123456)</span>
              </button>
              <button
                type="button"
                onClick={() => fillCreds('citizen@ecosphere.org', 'Citizen@123456')}
                style={{
                  textAlign: 'left',
                  background: '#f9f9f9',
                  border: '1px solid #e0e0e0',
                  borderRadius: '6px',
                  padding: '0.45rem 0.7rem',
                  fontSize: '0.8rem',
                  cursor: 'pointer'
                }}
              >
                <strong>Public Citizen:</strong> citizen@ecosphere.org <span style={{ opacity: 0.6 }}>(Citizen@123456)</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
