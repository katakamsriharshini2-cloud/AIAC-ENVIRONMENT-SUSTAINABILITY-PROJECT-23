import React, { useEffect, useState } from 'react';
import { crudApi } from '../api/client';
import { useAuth } from '../hooks/useAuth';
import DataSourceTag from '../components/DataSourceTag';
import AlertBanner from '../components/AlertBanner';
import LoadingSpinner from '../components/LoadingSpinner';

export default function Incidents() {
  const { user } = useAuth();
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('');
  const [severityFilter, setSeverityFilter] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // New incident form
  const [form, setForm] = useState({
    title: '',
    category: 'AIR_POLLUTION',
    severity: 'HIGH',
    description: '',
    location_name: 'Warangal',
    latitude: 17.9689,
    longitude: 79.5941,
    status: 'OPEN',
  });

  const loadIncidents = async () => {
    setLoading(true);
    try {
      const res = await crudApi.incidents(statusFilter);
      setIncidents(Array.isArray(res) ? res : []);
    } catch (err) {
      setError('Unable to load real-time incident registry.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadIncidents();
  }, [statusFilter]);

  const handleCreate = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await crudApi.createIncident(form);
      setSuccess('Environmental incident recorded in state registry!');
      setShowModal(false);
      setForm({
        title: '',
        category: 'AIR_POLLUTION',
        severity: 'HIGH',
        description: '',
        location_name: 'Warangal',
        latitude: 17.9689,
        longitude: 79.5941,
        status: 'OPEN',
      });
      loadIncidents();
    } catch (err) {
      setError(err.message || 'Failed to file incident report.');
    }
  };

  const handleStatusUpdate = async (id, newStatus) => {
    try {
      await crudApi.updateIncident(id, { status: newStatus });
      setSuccess(`Incident #${id} transitioned to ${newStatus}`);
      loadIncidents();
    } catch (err) {
      setError('Failed to update incident status.');
    }
  };

  // Fallback sample incidents if database is fresh
  const displayList = incidents.length > 0 ? incidents : [
    {
      id: 1,
      title: 'Illegal Agricultural Stubble Burning Near Station Ghanpur',
      category: 'AIR_POLLUTION',
      severity: 'HIGH',
      status: 'OPEN',
      location_name: 'Station Ghanpur, Warangal Outer',
      description: 'Continuous particulate plume detected via MODIS thermal anomaly. CPCB PM2.5 elevated to 184 µg/m³.',
      created_at: '2026-11-20T14:30:00Z',
    },
    {
      id: 2,
      title: 'Industrial Chemical Effluent Ingress into Bhadrakali Lake Overflow',
      category: 'WATER_CONTAMINATION',
      severity: 'CRITICAL',
      status: 'UNDER_INVESTIGATION',
      location_name: 'Bhadrakali Lake Northern Embankment',
      description: 'Optical probe registered pH spike to 9.2 and Dissolved Oxygen crash to 2.1 mg/L.',
      created_at: '2026-11-19T09:15:00Z',
    },
    {
      id: 3,
      title: 'Major Medical & Plastic Waste Dump at Hunter Road Ravine',
      category: 'ILLEGAL_DUMPING',
      severity: 'MEDIUM',
      status: 'RESOLVED',
      location_name: 'Hunter Road, Hanamkonda',
      description: 'Unsegregated biomedical refuse accumulated over 48 hours.',
      created_at: '2026-11-18T11:00:00Z',
    },
  ];

  const filtered = displayList.filter((item) => {
    if (statusFilter && item.status !== statusFilter) return false;
    if (severityFilter && item.severity !== severityFilter) return false;
    return true;
  });

  const getSeverityStyle = (sev) => {
    switch (sev) {
      case 'CRITICAL':
        return { background: '#ffebee', color: '#c62828', border: '1px solid #ffcdd2', fontWeight: 700 };
      case 'HIGH':
        return { background: '#fff3e0', color: '#e65100', border: '1px solid #ffe0b2', fontWeight: 600 };
      case 'MEDIUM':
        return { background: '#fffde7', color: '#f57f17', border: '1px solid #fff9c4', fontWeight: 600 };
      default:
        return { background: '#e1f5fe', color: '#0288d1', border: '1px solid #b3e5fc', fontWeight: 600 };
    }
  };

  const getStatusStyle = (st) => {
    switch (st) {
      case 'RESOLVED':
        return { background: '#e8f5e9', color: '#2e7d32', fontWeight: 600 };
      case 'UNDER_INVESTIGATION':
        return { background: '#e0f7fa', color: '#006064', fontWeight: 600 };
      default:
        return { background: '#ffebee', color: '#c62828', fontWeight: 600 };
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Header and Actions */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ margin: '0 0 0.25rem', color: '#1b4d3e' }}>
            Environmental Incidents & Emergency Response Dispatch
          </h2>
          <p style={{ margin: 0, fontSize: '0.85rem', color: '#666' }}>
            Official registry of violations, hazardous discharges, and municipal mitigation workflows
          </p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="btn btn-primary"
          style={{ padding: '0.6rem 1.25rem', fontWeight: 600 }}
        >
          ➕ Report New Incident
        </button>
      </div>

      {success && <AlertBanner message={success} type="success" onDismiss={() => setSuccess(null)} />}
      {error && <AlertBanner message={error} type="warning" />}

      {/* Filter Controls */}
      <div style={{
        background: '#ffffff',
        borderRadius: '10px',
        padding: '0.8rem 1.25rem',
        boxShadow: '0 2px 6px rgba(0,0,0,0.05)',
        display: 'flex',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '1rem',
        fontSize: '0.85rem'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <strong>Filter Status:</strong>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            style={{ padding: '0.35rem 0.6rem', borderRadius: '6px', border: '1px solid #ccc' }}
          >
            <option value="">All Statuses</option>
            <option value="OPEN">OPEN</option>
            <option value="UNDER_INVESTIGATION">UNDER_INVESTIGATION</option>
            <option value="RESOLVED">RESOLVED</option>
          </select>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <strong>Filter Severity:</strong>
          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            style={{ padding: '0.35rem 0.6rem', borderRadius: '6px', border: '1px solid #ccc' }}
          >
            <option value="">All Severities</option>
            <option value="CRITICAL">CRITICAL</option>
            <option value="HIGH">HIGH</option>
            <option value="MEDIUM">MEDIUM</option>
            <option value="LOW">LOW</option>
          </select>
        </div>

        <span style={{ marginLeft: 'auto', color: '#666' }}>
          Showing <strong>{filtered.length}</strong> active entries
        </span>
      </div>

      {/* Incidents Table */}
      <div style={{ background: '#fff', borderRadius: '12px', padding: '1.25rem', boxShadow: '0 2px 8px rgba(0,0,0,0.06)' }}>
        <div style={{ overflowX: 'auto' }}>
          <table className="eco-table" style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
            <thead>
              <tr style={{ background: '#f5f5f5', textAlign: 'left' }}>
                <th style={{ padding: '0.65rem' }}>ID</th>
                <th style={{ padding: '0.65rem' }}>Title & Description</th>
                <th style={{ padding: '0.65rem' }}>Category</th>
                <th style={{ padding: '0.65rem' }}>Severity</th>
                <th style={{ padding: '0.65rem' }}>Status</th>
                <th style={{ padding: '0.65rem' }}>Location</th>
                <th style={{ padding: '0.65rem' }}>Officer Actions</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((inc) => (
                <tr key={inc.id} style={{ borderBottom: '1px solid #eee' }}>
                  <td style={{ padding: '0.65rem', fontWeight: 700 }}>#{inc.id}</td>
                  <td style={{ padding: '0.65rem', maxWidth: '320px' }}>
                    <div style={{ fontWeight: 600, color: '#333' }}>{inc.title}</div>
                    <div style={{ fontSize: '0.78rem', color: '#666', marginTop: '0.2rem' }}>{inc.description}</div>
                  </td>
                  <td style={{ padding: '0.65rem' }}>
                    <span style={{ fontSize: '0.75rem', background: '#f5f5f5', padding: '2px 6px', borderRadius: '4px' }}>
                      {inc.category}
                    </span>
                  </td>
                  <td style={{ padding: '0.65rem' }}>
                    <span style={{ ...getSeverityStyle(inc.severity), padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem' }}>
                      {inc.severity}
                    </span>
                  </td>
                  <td style={{ padding: '0.65rem' }}>
                    <span style={{ ...getStatusStyle(inc.status), padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem' }}>
                      {inc.status}
                    </span>
                  </td>
                  <td style={{ padding: '0.65rem', color: '#555' }}>{inc.location_name}</td>
                  <td style={{ padding: '0.65rem' }}>
                    <div style={{ display: 'flex', gap: '0.3rem' }}>
                      {inc.status !== 'RESOLVED' && (
                        <button
                          onClick={() => handleStatusUpdate(inc.id, 'RESOLVED')}
                          className="btn btn-secondary btn-sm"
                          style={{ padding: '0.2rem 0.5rem', fontSize: '0.72rem' }}
                        >
                          Resolve
                        </button>
                      )}
                      {inc.status === 'OPEN' && (
                        <button
                          onClick={() => handleStatusUpdate(inc.id, 'UNDER_INVESTIGATION')}
                          className="btn btn-secondary btn-sm"
                          style={{ padding: '0.2rem 0.5rem', fontSize: '0.72rem' }}
                        >
                          Investigate
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Create Modal */}
      {showModal && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 9999,
          padding: '1rem'
        }}>
          <div style={{
            background: '#fff',
            borderRadius: '12px',
            padding: '1.75rem',
            maxWidth: '540px',
            width: '100%',
            boxShadow: '0 10px 30px rgba(0,0,0,0.2)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ margin: 0, color: '#1b4d3e' }}>File Official Environmental Incident</h3>
              <button onClick={() => setShowModal(false)} style={{ background: 'none', border: 'none', fontSize: '1.2rem', cursor: 'pointer' }}>
                ✕
              </button>
            </div>

            <form onSubmit={handleCreate} style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.2rem' }}>Title</label>
                <input
                  type="text"
                  required
                  value={form.title}
                  onChange={(e) => setForm({ ...form, title: e.target.value })}
                  placeholder="e.g. Chemical plume discharged from industrial stack"
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #ccc', boxSizing: 'border-box' }}
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.8rem' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.2rem' }}>Category</label>
                  <select
                    value={form.category}
                    onChange={(e) => setForm({ ...form, category: e.target.value })}
                    style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #ccc' }}
                  >
                    <option value="AIR_POLLUTION">Air Pollution</option>
                    <option value="WATER_CONTAMINATION">Water Contamination</option>
                    <option value="ILLEGAL_DUMPING">Illegal Waste Dumping</option>
                    <option value="WILDLIFE_THREAT">Wildlife Threat</option>
                  </select>
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.2rem' }}>Severity</label>
                  <select
                    value={form.severity}
                    onChange={(e) => setForm({ ...form, severity: e.target.value })}
                    style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #ccc' }}
                  >
                    <option value="CRITICAL">CRITICAL</option>
                    <option value="HIGH">HIGH</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="LOW">LOW</option>
                  </select>
                </div>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.2rem' }}>Location Name</label>
                <input
                  type="text"
                  required
                  value={form.location_name}
                  onChange={(e) => setForm({ ...form, location_name: e.target.value })}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #ccc', boxSizing: 'border-box' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.2rem' }}>Detailed Description</label>
                <textarea
                  rows="3"
                  required
                  value={form.description}
                  onChange={(e) => setForm({ ...form, description: e.target.value })}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #ccc', boxSizing: 'border-box' }}
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem', marginTop: '0.5rem' }}>
                <button type="button" onClick={() => setShowModal(false)} className="btn btn-secondary">
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Save & Dispatch Incident
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
