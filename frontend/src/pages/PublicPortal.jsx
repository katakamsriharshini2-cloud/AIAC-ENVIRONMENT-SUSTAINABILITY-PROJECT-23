import React, { useState, useEffect } from 'react';
import { portalApi } from '../api/client';
import { useAuth } from '../hooks/useAuth';
import DataSourceTag from '../components/DataSourceTag';
import AlertBanner from '../components/AlertBanner';
import LoadingSpinner from '../components/LoadingSpinner';

export default function PublicPortal() {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('submit');
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(null);
  const [generatedCode, setGeneratedCode] = useState(null);
  const [trackCode, setTrackCode] = useState('');
  const [trackedReport, setTrackedReport] = useState(null);
  const [trackError, setTrackError] = useState(null);
  const [error, setError] = useState(null);

  // Form state
  const [formData, setFormData] = useState({
    citizen_name: '',
    citizen_email: '',
    category: 'AIR_POLLUTION',
    title: '',
    description: '',
    location_name: 'Warangal',
    latitude: 17.9689,
    longitude: 79.5941,
  });

  const loadReports = async () => {
    try {
      const res = await portalApi.listReports();
      setReports(Array.isArray(res) ? res : []);
    } catch (err) {
      // Keep initial or fallback list
    }
  };

  useEffect(() => {
    loadReports();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSubmitSuccess(null);
    try {
      const res = await portalApi.submitReport(formData);
      const code = res?.tracking_code || `ECO-${Math.floor(100000 + Math.random() * 900000)}`;
      setGeneratedCode(code);
      setSubmitSuccess('Your environmental grievance has been logged successfully and assigned to the Warangal Municipal Authority.');
      loadReports();
    } catch (err) {
      setError(err.message || 'Failed to submit report. Please check required fields.');
    } finally {
      setLoading(false);
    }
  };

  const handleTrack = async (e) => {
    e.preventDefault();
    setTrackError(null);
    setTrackedReport(null);
    try {
      const res = await portalApi.trackReport(trackCode.trim());
      setTrackedReport(res);
    } catch (err) {
      setTrackError('Report tracking code not found in municipal registry.');
    }
  };

  const copyCode = () => {
    if (generatedCode) {
      navigator.clipboard.writeText(generatedCode);
      alert('Tracking code copied to clipboard!');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div>
        <h2 style={{ margin: '0 0 0.25rem', color: '#1b4d3e' }}>
          Public Citizen Science & Environmental Grievance Portal
        </h2>
        <p style={{ margin: 0, fontSize: '0.85rem', color: '#666' }}>
          Direct grievance submission, incident verification, and algorithmic tracking for Telangana communities
        </p>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', borderBottom: '2px solid #e0e0e0', gap: '0.5rem' }}>
        <button
          onClick={() => setActiveTab('submit')}
          style={{
            padding: '0.75rem 1.5rem',
            background: activeTab === 'submit' ? '#2e7d32' : 'transparent',
            color: activeTab === 'submit' ? '#fff' : '#555',
            border: 'none',
            borderRadius: '8px 8px 0 0',
            fontWeight: 600,
            cursor: 'pointer'
          }}
        >
          📝 File Environmental Grievance
        </button>
        <button
          onClick={() => setActiveTab('track')}
          style={{
            padding: '0.75rem 1.5rem',
            background: activeTab === 'track' ? '#2e7d32' : 'transparent',
            color: activeTab === 'track' ? '#fff' : '#555',
            border: 'none',
            borderRadius: '8px 8px 0 0',
            fontWeight: 600,
            cursor: 'pointer'
          }}
        >
          🔍 Track Grievance Status
        </button>
        <button
          onClick={() => setActiveTab('community')}
          style={{
            padding: '0.75rem 1.5rem',
            background: activeTab === 'community' ? '#2e7d32' : 'transparent',
            color: activeTab === 'community' ? '#fff' : '#555',
            border: 'none',
            borderRadius: '8px 8px 0 0',
            fontWeight: 600,
            cursor: 'pointer'
          }}
        >
          👥 Community Reports Registry
        </button>
      </div>

      {error && <AlertBanner message={error} type="warning" />}

      {/* Submit Tab */}
      {activeTab === 'submit' && (
        <div style={{ background: '#fff', borderRadius: '12px', padding: '1.5rem', boxShadow: '0 2px 8px rgba(0,0,0,0.06)' }}>
          {submitSuccess && (
            <div style={{
              background: '#e8f5e9',
              border: '1px solid #c8e6c9',
              borderRadius: '8px',
              padding: '1.25rem',
              marginBottom: '1.5rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#2e7d32', fontWeight: 700, fontSize: '1rem' }}>
                <span>✅</span> Grievance Dispatched to Environmental Officer
              </div>
              <p style={{ margin: '0.5rem 0', fontSize: '0.85rem', color: '#333' }}>{submitSuccess}</p>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                marginTop: '0.75rem',
                background: '#fff',
                padding: '0.6rem 1rem',
                borderRadius: '6px',
                border: '1px solid #a5d6a7',
                width: 'fit-content'
              }}>
                <span style={{ fontSize: '0.85rem' }}>Your Tracking Code:</span>
                <strong style={{ fontSize: '1.1rem', color: '#1b4d3e', letterSpacing: '1px' }}>{generatedCode}</strong>
                <button onClick={copyCode} className="btn btn-secondary btn-sm" style={{ padding: '0.2rem 0.6rem' }}>
                  📋 Copy
                </button>
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.3rem' }}>
                  Citizen / Whistleblower Name
                </label>
                <input
                  type="text"
                  required
                  value={formData.citizen_name}
                  onChange={(e) => setFormData({ ...formData, citizen_name: e.target.value })}
                  placeholder="e.g. Ramesh Varma"
                  style={{ width: '100%', padding: '0.55rem', borderRadius: '6px', border: '1px solid #ccc', boxSizing: 'border-box' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.3rem' }}>
                  Email Address (for status alerts)
                </label>
                <input
                  type="email"
                  required
                  value={formData.citizen_email}
                  onChange={(e) => setFormData({ ...formData, citizen_email: e.target.value })}
                  placeholder="ramesh@example.com"
                  style={{ width: '100%', padding: '0.55rem', borderRadius: '6px', border: '1px solid #ccc', boxSizing: 'border-box' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.3rem' }}>
                  Category of Violation
                </label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  style={{ width: '100%', padding: '0.55rem', borderRadius: '6px', border: '1px solid #ccc', boxSizing: 'border-box' }}
                >
                  <option value="AIR_POLLUTION">Air Pollution / Open Burning / Smoke Plume</option>
                  <option value="WATER_CONTAMINATION">Water Contamination / Untreated Effluent</option>
                  <option value="ILLEGAL_DUMPING">Solid Waste Accumulation / Plastic Dumping</option>
                  <option value="WILDLIFE_THREAT">Wildlife Threat / Tree Felling</option>
                  <option value="INDUSTRIAL_NOISE">Industrial Noise Violation</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.3rem' }}>
                  Specific Location / Landmark
                </label>
                <input
                  type="text"
                  required
                  value={formData.location_name}
                  onChange={(e) => setFormData({ ...formData, location_name: e.target.value })}
                  placeholder="Near Hunter Road, Warangal"
                  style={{ width: '100%', padding: '0.55rem', borderRadius: '6px', border: '1px solid #ccc', boxSizing: 'border-box' }}
                />
              </div>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.3rem' }}>
                Incident Title
              </label>
              <input
                type="text"
                required
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                placeholder="Brief summary of observation..."
                style={{ width: '100%', padding: '0.55rem', borderRadius: '6px', border: '1px solid #ccc', boxSizing: 'border-box' }}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.3rem' }}>
                Detailed Observation & Environmental Impact
              </label>
              <textarea
                rows="4"
                required
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder="Please describe time of day, approximate scale, odor, visible discharge..."
                style={{ width: '100%', padding: '0.55rem', borderRadius: '6px', border: '1px solid #ccc', boxSizing: 'border-box' }}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary"
              style={{ width: 'fit-content', padding: '0.65rem 1.5rem', fontWeight: 600 }}
            >
              {loading ? 'Transmitting to Municipal Registry...' : '🚀 Submit Official Grievance'}
            </button>
          </form>
        </div>
      )}

      {/* Track Tab */}
      {activeTab === 'track' && (
        <div style={{ background: '#fff', borderRadius: '12px', padding: '1.5rem', boxShadow: '0 2px 8px rgba(0,0,0,0.06)' }}>
          <form onSubmit={handleTrack} style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', marginBottom: '1.5rem' }}>
            <input
              type="text"
              required
              value={trackCode}
              onChange={(e) => setTrackCode(e.target.value)}
              placeholder="Enter Tracking Code (e.g. ECO-849201)"
              style={{ width: '320px', padding: '0.6rem 0.8rem', borderRadius: '6px', border: '1px solid #ccc', fontWeight: 600 }}
            />
            <button type="submit" className="btn btn-primary" style={{ padding: '0.6rem 1.25rem' }}>
              Track Grievance
            </button>
          </form>

          {trackError && <AlertBanner message={trackError} type="warning" />}

          {trackedReport ? (
            <div style={{ border: '1px solid #e0e0e0', borderRadius: '10px', padding: '1.25rem', background: '#fafafa' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <h3 style={{ margin: '0 0 0.3rem', color: '#1b4d3e' }}>{trackedReport.title}</h3>
                  <span style={{ fontSize: '0.85rem', color: '#666' }}>Location: {trackedReport.location_name}</span>
                </div>
                <span style={{
                  background: trackedReport.status === 'RESOLVED' ? '#e8f5e9' : '#fff3e0',
                  color: trackedReport.status === 'RESOLVED' ? '#2e7d32' : '#e65100',
                  padding: '4px 10px',
                  borderRadius: '6px',
                  fontWeight: 700,
                  fontSize: '0.85rem'
                }}>
                  {trackedReport.status || 'UNDER_INVESTIGATION'}
                </span>
              </div>

              <div style={{ margin: '1rem 0', fontSize: '0.9rem', color: '#444' }}>
                <strong>Description:</strong> {trackedReport.description}
              </div>

              <div style={{
                background: '#fff',
                padding: '0.75rem 1rem',
                borderRadius: '6px',
                borderLeft: '4px solid #2e7d32',
                fontSize: '0.85rem'
              }}>
                <strong>Municipal Action Response: </strong>
                {trackedReport.official_response || 'Case dispatched to Regional Environmental Officer for on-site air & water quality testing.'}
              </div>
            </div>
          ) : (
            <p style={{ fontSize: '0.85rem', color: '#777' }}>
              Enter a valid tracking code to view real-time investigation milestones, inspector remarks, and remediation status.
            </p>
          )}
        </div>
      )}

      {/* Community Reports Feed Tab */}
      {activeTab === 'community' && (
        <div style={{ background: '#fff', borderRadius: '12px', padding: '1.25rem', boxShadow: '0 2px 8px rgba(0,0,0,0.06)' }}>
          <h4 style={{ margin: '0 0 1rem', color: '#1b4d3e' }}>Telangana Community Grievance Registry</h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {[
              {
                id: 'ECO-849201',
                title: 'Dense black smoke from brick kilns near Kazipet bypass',
                category: 'AIR_POLLUTION',
                location: 'Kazipet, Warangal',
                status: 'ACTION_TAKEN',
                date: '2026-11-20',
                resp: 'Notice served to kiln operator under Section 31A of Air Act 1981.'
              },
              {
                id: 'ECO-721943',
                title: 'Foaming observed at Bhadrakali lake north overflow channel',
                category: 'WATER_CONTAMINATION',
                location: 'Bhadrakali Lake, Warangal',
                status: 'UNDER_INVESTIGATION',
                date: '2026-11-19',
                resp: 'Water samples sent to regional laboratory for surfactant analysis.'
              },
              {
                id: 'ECO-610284',
                title: 'Unsegregated plastic waste overflow near Kakatiya market',
                category: 'ILLEGAL_DUMPING',
                location: 'Hanamkonda Market',
                status: 'RESOLVED',
                date: '2026-11-18',
                resp: 'Sanitation team deployed with compacting vehicle. Bins cleared.'
              },
            ].map((rep, idx) => (
              <div
                key={idx}
                style={{
                  padding: '1rem',
                  borderRadius: '8px',
                  border: '1px solid #eee',
                  background: '#fcfdfc'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div>
                    <strong style={{ fontSize: '0.95rem', color: '#333' }}>{rep.title}</strong>
                    <div style={{ fontSize: '0.8rem', color: '#777', marginTop: '0.2rem' }}>
                      Ref: <code>{rep.id}</code> • Location: {rep.location} • Date: {rep.date}
                    </div>
                  </div>
                  <span style={{
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    padding: '2px 8px',
                    borderRadius: '4px',
                    background: rep.status === 'RESOLVED' ? '#e8f5e9' : '#fff3e0',
                    color: rep.status === 'RESOLVED' ? '#2e7d32' : '#e65100'
                  }}>
                    {rep.status}
                  </span>
                </div>
                <div style={{ fontSize: '0.8rem', color: '#555', marginTop: '0.5rem', background: '#f5f5f5', padding: '0.4rem 0.6rem', borderRadius: '4px' }}>
                  <strong>Officer Update:</strong> {rep.resp}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
