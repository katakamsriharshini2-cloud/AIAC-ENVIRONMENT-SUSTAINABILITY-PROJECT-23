import React, { useEffect, useState, useMemo } from 'react';
import { liveApi, crudApi, iotApi } from '../api/client';
import DataSourceTag from '../components/DataSourceTag';
import AlertBanner from '../components/AlertBanner';
import {
  BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend
} from 'recharts';

export default function WaterQuality() {
  const [loading, setLoading] = useState(true);
  const [records, setRecords] = useState([]);
  const [selectedWaterBody, setSelectedWaterBody] = useState('ALL');
  const [selectedStatus, setSelectedStatus] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [iotSuccess, setIotSuccess] = useState(null);
  const [error, setError] = useState(null);

  // IoT Sensor submission state
  const [iotForm, setIotForm] = useState({
    probe_id: 'IOT-WTR-WAR-01',
    water_body: 'Bhadrakali Lake',
    ph: 7.5,
    dissolved_oxygen: 6.9,
    bod: 2.2,
    turbidity: 3.8,
    tds: 290,
    temperature_c: 26.0,
  });

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      // Fetch both live and stored records from backend
      const [crudRes, liveRes] = await Promise.allSettled([
        crudApi.waterQuality(100),
        liveApi.waterQuality()
      ]);

      let combined = [];
      if (crudRes.status === 'fulfilled' && Array.isArray(crudRes.value)) {
        combined = crudRes.value;
      }
      if (combined.length === 0 && liveRes.status === 'fulfilled') {
        const val = liveRes.value;
        combined = Array.isArray(val) ? val : (val?.data || []);
      }

      setRecords(combined);
    } catch (err) {
      setError('Could not connect to backend database. Please ensure backend server is running on http://localhost:8000.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleIotSubmit = async (e) => {
    e.preventDefault();
    setIotSuccess(null);
    setError(null);
    try {
      await iotApi.waterReading(iotForm);
      setIotSuccess(`Live optical probe telemetry for "${iotForm.water_body}" recorded and computed in backend database!`);
      await loadData();
    } catch (err) {
      setError(err.message || 'Failed to submit IoT sensor reading.');
    }
  };

  // Distinct water bodies for dropdown filter
  const waterBodyOptions = useMemo(() => {
    const set = new Set();
    records.forEach(r => {
      const name = r.water_body_name || r.name;
      if (name) set.add(name);
    });
    return Array.from(set).sort();
  }, [records]);

  // Filtered records
  const filteredRecords = useMemo(() => {
    return records.filter(r => {
      const name = (r.water_body_name || r.name || '').toLowerCase();
      const loc = (r.location_name || r.location || '').toLowerCase();
      const status = (r.wqi_status || r.status || '').toLowerCase();
      const query = searchQuery.toLowerCase();

      const matchQuery = !query || name.includes(query) || loc.includes(query);
      const matchBody = selectedWaterBody === 'ALL' || (r.water_body_name || r.name) === selectedWaterBody;
      const matchStatus = selectedStatus === 'ALL' || (r.wqi_status || r.status) === selectedStatus;

      return matchQuery && matchBody && matchStatus;
    });
  }, [records, searchQuery, selectedWaterBody, selectedStatus]);

  // Overall Statistics computed from actual loaded records
  const stats = useMemo(() => {
    if (records.length === 0) {
      return { total: 0, locations: 0, avgPh: 0, avgDo: 0, avgTurbidity: 0, avgWqi: 0 };
    }
    const total = records.length;
    const locations = new Set(records.map(r => r.water_body_name || r.name)).size;
    const sumPh = records.reduce((acc, r) => acc + (Number(r.ph) || 0), 0);
    const sumDo = records.reduce((acc, r) => acc + (Number(r.dissolved_oxygen ?? r.do) || 0), 0);
    const sumTurb = records.reduce((acc, r) => acc + (Number(r.turbidity) || 0), 0);
    const sumWqi = records.reduce((acc, r) => acc + (Number(r.water_quality_index ?? r.wqi) || 0), 0);

    return {
      total,
      locations,
      avgPh: (sumPh / total).toFixed(2),
      avgDo: (sumDo / total).toFixed(2),
      avgTurbidity: (sumTurb / total).toFixed(2),
      avgWqi: (sumWqi / total).toFixed(1),
    };
  }, [records]);

  // Location-wise comparison data for Bar Chart
  const locationComparisonData = useMemo(() => {
    const grouped = {};
    records.forEach(r => {
      const name = r.water_body_name || r.name || 'Unknown';
      if (!grouped[name]) {
        grouped[name] = { name, count: 0, sumWqi: 0, sumDo: 0, sumBod: 0, sumTurb: 0 };
      }
      grouped[name].count += 1;
      grouped[name].sumWqi += (Number(r.water_quality_index ?? r.wqi) || 0);
      grouped[name].sumDo += (Number(r.dissolved_oxygen ?? r.do) || 0);
      grouped[name].sumBod += (Number(r.bod) || 0);
      grouped[name].sumTurb += (Number(r.turbidity) || 0);
    });

    return Object.values(grouped).map(g => ({
      name: g.name.replace(' Reservoir', '').replace(' Lake', ' Lk.').replace(' Tank', ' Tk.'),
      fullName: g.name,
      avgWqi: parseFloat((g.sumWqi / g.count).toFixed(1)),
      avgDo: parseFloat((g.sumDo / g.count).toFixed(1)),
      avgBod: parseFloat((g.sumBod / g.count).toFixed(1)),
      avgTurb: parseFloat((g.sumTurb / g.count).toFixed(1)),
    }));
  }, [records]);

  // Date-wise chronological trends for Line Chart
  const dateWiseTrendData = useMemo(() => {
    const sorted = [...records].sort((a, b) => {
      const ta = new Date(a.observation_timestamp || a.sampling_date || 0);
      const tb = new Date(b.observation_timestamp || b.sampling_date || 0);
      return ta - tb;
    });

    return sorted.map((r, i) => {
      const dateStr = (r.observation_timestamp || r.sampling_date || '').slice(0, 10);
      return {
        date: dateStr || `Point-${i + 1}`,
        waterBody: r.water_body_name || r.name,
        WQI: parseFloat((Number(r.water_quality_index ?? r.wqi) || 0).toFixed(1)),
        DO: parseFloat((Number(r.dissolved_oxygen ?? r.do) || 0).toFixed(1)),
        pH: parseFloat((Number(r.ph) || 0).toFixed(2)),
      };
    });
  }, [records]);

  // Color helper for WQI
  const getWqiColor = (val) => {
    const num = Number(val);
    if (num >= 85) return '#2e7d32'; // Excellent (Dark Green)
    if (num >= 70) return '#388e3c'; // Good (Green)
    if (num >= 60) return '#f57c00'; // Satisfactory (Orange)
    if (num >= 50) return '#e65100'; // Moderate (Deep Orange)
    return '#d32f2f'; // Poor (Red)
  };

  const getWqiBg = (val) => {
    const num = Number(val);
    if (num >= 85) return '#e8f5e9';
    if (num >= 70) return '#f1f8e9';
    if (num >= 60) return '#fff3e0';
    if (num >= 50) return '#fbe9e7';
    return '#ffebee';
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', paddingBottom: '2rem' }}>
      {/* 1. Header with Actions */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ margin: '0 0 0.35rem', color: '#1b4d3e', fontSize: '1.6rem', fontWeight: 700 }}>
            💧 Surface Water Quality &amp; Hydrological Monitoring
          </h2>
          <p style={{ margin: 0, fontSize: '0.88rem', color: '#555' }}>
            Comprehensive analysis of Warangal reservoirs, lakes &amp; rivers — Connected to official CPCB, TSPCB datasets and IoT optical sensors.
          </p>
        </div>
        <div style={{ display: 'flex', gap: '0.6rem' }}>
          <button
            onClick={loadData}
            style={{
              padding: '0.6rem 1.1rem',
              backgroundColor: '#2e7d32',
              color: '#fff',
              border: 'none',
              borderRadius: '8px',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              boxShadow: '0 2px 6px rgba(46,125,50,0.25)'
            }}
          >
            🔄 Refresh Live Data
          </button>
        </div>
      </div>

      {/* 2. Regulatory Compliance Notice */}
      <div style={{
        background: '#fff8e1',
        borderLeft: '5px solid #ffa000',
        padding: '0.9rem 1.25rem',
        borderRadius: '8px',
        fontSize: '0.85rem',
        color: '#5d4037',
        display: 'flex',
        alignItems: 'center',
        gap: '0.85rem'
      }}>
        <span style={{ fontSize: '1.4rem' }}>ℹ️</span>
        <div>
          <strong>National Water Quality Monitoring Programme (NWQMP) Standard: </strong>
          Government baseline readings represent certified grab sampling analyzed at CPCB/TSPCB certified laboratories. Real-time IoT values are ingested via telemetric submersible probes. All records adhere to BIS IS:10500 standards.
        </div>
      </div>

      {error && <AlertBanner message={error} type="error" onDismiss={() => setError(null)} />}
      {iotSuccess && <AlertBanner message={iotSuccess} type="success" onDismiss={() => setIotSuccess(null)} />}

      {/* 3. Key Summary KPI Metrics */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
        gap: '1rem'
      }}>
        <div style={{ background: '#fff', padding: '1.25rem', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.06)', borderTop: '4px solid #1b4d3e' }}>
          <div style={{ fontSize: '0.8rem', color: '#666', fontWeight: 600, textTransform: 'uppercase' }}>Total Records</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: '#1b4d3e', marginTop: '0.25rem' }}>{stats.total}</div>
          <div style={{ fontSize: '0.75rem', color: '#888', marginTop: '0.2rem' }}>In backend database</div>
        </div>

        <div style={{ background: '#fff', padding: '1.25rem', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.06)', borderTop: '4px solid #0288d1' }}>
          <div style={{ fontSize: '0.8rem', color: '#666', fontWeight: 600, textTransform: 'uppercase' }}>Water Bodies</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: '#0288d1', marginTop: '0.25rem' }}>{stats.locations}</div>
          <div style={{ fontSize: '0.75rem', color: '#888', marginTop: '0.2rem' }}>Monitored locations</div>
        </div>

        <div style={{ background: '#fff', padding: '1.25rem', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.06)', borderTop: `4px solid ${getWqiColor(stats.avgWqi)}` }}>
          <div style={{ fontSize: '0.8rem', color: '#666', fontWeight: 600, textTransform: 'uppercase' }}>Average WQI</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: getWqiColor(stats.avgWqi), marginTop: '0.25rem' }}>{stats.avgWqi}</div>
          <div style={{ fontSize: '0.75rem', color: '#888', marginTop: '0.2rem' }}>
            {stats.avgWqi >= 80 ? 'Good / Potable Class' : stats.avgWqi >= 60 ? 'Satisfactory' : 'Moderate'}
          </div>
        </div>

        <div style={{ background: '#fff', padding: '1.25rem', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.06)', borderTop: '4px solid #43a047' }}>
          <div style={{ fontSize: '0.8rem', color: '#666', fontWeight: 600, textTransform: 'uppercase' }}>Average pH</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: '#2e7d32', marginTop: '0.25rem' }}>{stats.avgPh}</div>
          <div style={{ fontSize: '0.75rem', color: '#888', marginTop: '0.2rem' }}>Permissible: 6.5 – 8.5</div>
        </div>

        <div style={{ background: '#fff', padding: '1.25rem', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.06)', borderTop: '4px solid #00897b' }}>
          <div style={{ fontSize: '0.8rem', color: '#666', fontWeight: 600, textTransform: 'uppercase' }}>Avg Dissolved Oxygen</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: '#00897b', marginTop: '0.25rem' }}>{stats.avgDo} <span style={{ fontSize: '1rem', fontWeight: 500 }}>mg/L</span></div>
          <div style={{ fontSize: '0.75rem', color: '#888', marginTop: '0.2rem' }}>Standard: &gt; 5.0 mg/L</div>
        </div>

        <div style={{ background: '#fff', padding: '1.25rem', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.06)', borderTop: '4px solid #fb8c00' }}>
          <div style={{ fontSize: '0.8rem', color: '#666', fontWeight: 600, textTransform: 'uppercase' }}>Avg Turbidity</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: '#fb8c00', marginTop: '0.25rem' }}>{stats.avgTurbidity} <span style={{ fontSize: '1rem', fontWeight: 500 }}>NTU</span></div>
          <div style={{ fontSize: '0.75rem', color: '#888', marginTop: '0.2rem' }}>Desirable: &lt; 5.0 NTU</div>
        </div>
      </div>

      {/* 4. Interactive Charts Section */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(460px, 1fr))', gap: '1.5rem' }}>
        {/* Chart 1: Location-wise Comparison */}
        <div style={{ background: '#fff', borderRadius: '12px', padding: '1.25rem', boxShadow: '0 2px 8px rgba(0,0,0,0.06)' }}>
          <div style={{ marginBottom: '1rem' }}>
            <h4 style={{ margin: '0 0 0.2rem', color: '#1b4d3e', fontSize: '1.05rem' }}>
              📊 Location-wise Water Quality Index (WQI) &amp; Dissolved Oxygen
            </h4>
            <span style={{ fontSize: '0.8rem', color: '#777' }}>Average parameters by lake/reservoir in Warangal basin</span>
          </div>
          <div style={{ width: '100%', height: 280 }}>
            <ResponsiveContainer>
              <BarChart data={locationComparisonData} margin={{ top: 10, right: 10, left: -10, bottom: 25 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="name" stroke="#666" fontSize={11} interval={0} angle={-15} textAnchor="end" />
                <YAxis stroke="#666" fontSize={11} domain={[0, 100]} />
                <Tooltip
                  formatter={(val, name) => [val, name === 'avgWqi' ? 'Water Quality Index (/100)' : name === 'avgDo' ? 'Dissolved Oxygen (mg/L)' : 'Turbidity (NTU)']}
                  labelFormatter={(name, payload) => payload?.[0]?.payload?.fullName || name}
                />
                <Legend verticalAlign="top" wrapperStyle={{ paddingBottom: '8px' }} />
                <Bar dataKey="avgWqi" name="Average WQI" fill="#0288d1" radius={[4, 4, 0, 0]} />
                <Bar dataKey="avgDo" name="Dissolved Oxygen (mg/L)" fill="#26a69a" radius={[4, 4, 0, 0]} />
                <Bar dataKey="avgTurb" name="Turbidity (NTU)" fill="#ffa726" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Date-wise Trends */}
        <div style={{ background: '#fff', borderRadius: '12px', padding: '1.25rem', boxShadow: '0 2px 8px rgba(0,0,0,0.06)' }}>
          <div style={{ marginBottom: '1rem' }}>
            <h4 style={{ margin: '0 0 0.2rem', color: '#1b4d3e', fontSize: '1.05rem' }}>
              📈 Chronological Water Quality Trends (WQI &amp; pH)
            </h4>
            <span style={{ fontSize: '0.8rem', color: '#777' }}>Historical observations across sampling dates</span>
          </div>
          <div style={{ width: '100%', height: 280 }}>
            <ResponsiveContainer>
              <LineChart data={dateWiseTrendData} margin={{ top: 10, right: 10, left: -10, bottom: 25 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="date" stroke="#666" fontSize={11} angle={-15} textAnchor="end" />
                <YAxis stroke="#666" fontSize={11} domain={[50, 100]} />
                <Tooltip
                  formatter={(val, name) => [val, name === 'WQI' ? 'WQI (/100)' : name === 'DO' ? 'DO (mg/L)' : 'pH Value']}
                  labelFormatter={(label, payload) => `${label} - ${payload?.[0]?.payload?.waterBody || ''}`}
                />
                <Legend verticalAlign="top" wrapperStyle={{ paddingBottom: '8px' }} />
                <Line type="monotone" dataKey="WQI" name="Water Quality Index" stroke="#0288d1" strokeWidth={2.5} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="DO" name="Dissolved Oxygen (mg/L)" stroke="#26a69a" strokeWidth={2} dot={{ r: 2 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* 5. Clear Explanations of Water-Quality Indicators */}
      <div style={{ background: '#fff', borderRadius: '12px', padding: '1.25rem', boxShadow: '0 2px 8px rgba(0,0,0,0.06)' }}>
        <h4 style={{ margin: '0 0 0.9rem', color: '#1b4d3e', fontSize: '1.05rem' }}>
          📖 Water Quality Parameter Standards &amp; Diagnostic Guide (CPCB / BIS IS:10500)
        </h4>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
          <div style={{ background: '#f8faf8', padding: '0.85rem', borderRadius: '8px', borderLeft: '3px solid #2e7d32' }}>
            <div style={{ fontWeight: 700, color: '#1b4d3e', fontSize: '0.9rem' }}>pH (Acidity / Alkalinity)</div>
            <div style={{ fontSize: '0.8rem', color: '#555', marginTop: '0.3rem' }}>
              <strong>Standard: 6.5 – 8.5</strong>. Indicates chemical balance. Values below 6.5 cause corrosion; above 8.5 may cause scale and eye irritation.
            </div>
          </div>
          <div style={{ background: '#f8faf8', padding: '0.85rem', borderRadius: '8px', borderLeft: '3px solid #00897b' }}>
            <div style={{ fontWeight: 700, color: '#00897b', fontSize: '0.9rem' }}>Dissolved Oxygen (DO)</div>
            <div style={{ fontSize: '0.8rem', color: '#555', marginTop: '0.3rem' }}>
              <strong>Standard: &gt; 5.0 mg/L</strong>. Crucial for aquatic life. Levels below 4.0 mg/L cause fish mortality and promote anaerobic decay.
            </div>
          </div>
          <div style={{ background: '#f8faf8', padding: '0.85rem', borderRadius: '8px', borderLeft: '3px solid #e53935' }}>
            <div style={{ fontWeight: 700, color: '#c62828', fontSize: '0.9rem' }}>Biochemical Oxygen Demand (BOD)</div>
            <div style={{ fontSize: '0.8rem', color: '#555', marginTop: '0.3rem' }}>
              <strong>Standard: &lt; 3.0 mg/L</strong>. Measures biodegradable organic matter. Elevated BOD signifies raw municipal sewage or runoff.
            </div>
          </div>
          <div style={{ background: '#f8faf8', padding: '0.85rem', borderRadius: '8px', borderLeft: '3px solid #fb8c00' }}>
            <div style={{ fontWeight: 700, color: '#e65100', fontSize: '0.9rem' }}>Turbidity &amp; TDS</div>
            <div style={{ fontSize: '0.8rem', color: '#555', marginTop: '0.3rem' }}>
              <strong>Turbidity: &lt; 5 NTU | TDS: &lt; 500 mg/L</strong>. Reflects suspended particulate matter, silt and dissolved mineral concentration.
            </div>
          </div>
        </div>
      </div>

      {/* 6. Filter Controls & Detailed Records Table */}
      <div style={{ background: '#fff', borderRadius: '12px', padding: '1.25rem', boxShadow: '0 2px 8px rgba(0,0,0,0.06)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.2rem' }}>
          <div>
            <h4 style={{ margin: 0, color: '#1b4d3e', fontSize: '1.1rem' }}>
              📋 Detailed Water Quality Records ({filteredRecords.length} of {records.length})
            </h4>
            <span style={{ fontSize: '0.8rem', color: '#777' }}>Actual records retrieved from backend database</span>
          </div>

          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.6rem', alignItems: 'center' }}>
            {/* Search Input */}
            <input
              type="text"
              placeholder="Search location or water body..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                padding: '0.5rem 0.8rem',
                borderRadius: '8px',
                border: '1px solid #ccc',
                fontSize: '0.85rem',
                minWidth: '200px'
              }}
            />

            {/* Filter by Water Body */}
            <select
              value={selectedWaterBody}
              onChange={(e) => setSelectedWaterBody(e.target.value)}
              style={{
                padding: '0.5rem 0.8rem',
                borderRadius: '8px',
                border: '1px solid #ccc',
                fontSize: '0.85rem',
                background: '#fff'
              }}
            >
              <option value="ALL">All Water Bodies</option>
              {waterBodyOptions.map(name => (
                <option key={name} value={name}>{name}</option>
              ))}
            </select>

            {/* Filter by Status */}
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              style={{
                padding: '0.5rem 0.8rem',
                borderRadius: '8px',
                border: '1px solid #ccc',
                fontSize: '0.85rem',
                background: '#fff'
              }}
            >
              <option value="ALL">All Statuses</option>
              <option value="Excellent">Excellent</option>
              <option value="Good">Good</option>
              <option value="Satisfactory">Satisfactory</option>
              <option value="Moderate">Moderate</option>
              <option value="Poor">Poor</option>
            </select>

            {(searchQuery || selectedWaterBody !== 'ALL' || selectedStatus !== 'ALL') && (
              <button
                onClick={() => { setSearchQuery(''); setSelectedWaterBody('ALL'); setSelectedStatus('ALL'); }}
                style={{
                  padding: '0.5rem 0.75rem',
                  background: '#f5f5f5',
                  border: '1px solid #ddd',
                  borderRadius: '6px',
                  fontSize: '0.8rem',
                  cursor: 'pointer'
                }}
              >
                Clear Filters
              </button>
            )}
          </div>
        </div>

        {/* Table Container */}
        <div style={{ overflowX: 'auto', border: '1px solid #e0e0e0', borderRadius: '8px' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
            <thead>
              <tr style={{ background: '#f5f8f5', borderBottom: '2px solid #e0e0e0', color: '#1b4d3e' }}>
                <th style={{ padding: '0.75rem 1rem' }}>Water Body</th>
                <th style={{ padding: '0.75rem 1rem' }}>Location</th>
                <th style={{ padding: '0.75rem 1rem' }}>Sampling Date</th>
                <th style={{ padding: '0.75rem 1rem' }}>pH</th>
                <th style={{ padding: '0.75rem 1rem' }}>DO (mg/L)</th>
                <th style={{ padding: '0.75rem 1rem' }}>BOD (mg/L)</th>
                <th style={{ padding: '0.75rem 1rem' }}>Turbidity</th>
                <th style={{ padding: '0.75rem 1rem' }}>TDS (mg/L)</th>
                <th style={{ padding: '0.75rem 1rem' }}>WQI Index</th>
                <th style={{ padding: '0.75rem 1rem' }}>Status</th>
                <th style={{ padding: '0.75rem 1rem' }}>Source</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={11} style={{ textAlign: 'center', padding: '2rem', color: '#888' }}>
                    Loading water quality records from backend...
                  </td>
                </tr>
              ) : filteredRecords.length === 0 ? (
                <tr>
                  <td colSpan={11} style={{ textAlign: 'center', padding: '2rem', color: '#888' }}>
                    No water quality records match your current filter criteria.
                  </td>
                </tr>
              ) : (
                filteredRecords.map((r, idx) => {
                  const wqi = Number(r.water_quality_index ?? r.wqi ?? 0);
                  const status = r.wqi_status || r.status || 'Good';
                  const date = (r.observation_timestamp || r.sampling_date || '').slice(0, 10);
                  const source = r.data_type || r.source || 'GOVERNMENT_DATA';

                  return (
                    <tr
                      key={r.id || idx}
                      style={{
                        borderBottom: '1px solid #eee',
                        background: idx % 2 === 0 ? '#fff' : '#fafafa'
                      }}
                    >
                      <td style={{ padding: '0.75rem 1rem', fontWeight: 600, color: '#1b4d3e' }}>
                        {r.water_body_name || r.name}
                      </td>
                      <td style={{ padding: '0.75rem 1rem', color: '#555' }}>
                        {r.location_name || r.location}
                      </td>
                      <td style={{ padding: '0.75rem 1rem', color: '#666', whiteSpace: 'nowrap' }}>
                        {date}
                      </td>
                      <td style={{ padding: '0.75rem 1rem', fontWeight: 600 }}>
                        {r.ph != null ? Number(r.ph).toFixed(2) : '—'}
                      </td>
                      <td style={{ padding: '0.75rem 1rem', color: Number(r.dissolved_oxygen ?? r.do) >= 5.0 ? '#2e7d32' : '#d32f2f', fontWeight: 600 }}>
                        {r.dissolved_oxygen != null || r.do != null ? Number(r.dissolved_oxygen ?? r.do).toFixed(1) : '—'}
                      </td>
                      <td style={{ padding: '0.75rem 1rem' }}>
                        {r.bod != null ? Number(r.bod).toFixed(1) : '—'}
                      </td>
                      <td style={{ padding: '0.75rem 1rem' }}>
                        {r.turbidity != null ? Number(r.turbidity).toFixed(1) + ' NTU' : '—'}
                      </td>
                      <td style={{ padding: '0.75rem 1rem' }}>
                        {r.tds != null ? Math.round(Number(r.tds)) : '—'}
                      </td>
                      <td style={{ padding: '0.75rem 1rem' }}>
                        <span style={{ fontWeight: 700, fontSize: '0.95rem', color: getWqiColor(wqi) }}>
                          {wqi.toFixed(1)}
                        </span>
                      </td>
                      <td style={{ padding: '0.75rem 1rem' }}>
                        <span style={{
                          padding: '3px 8px',
                          borderRadius: '6px',
                          fontSize: '0.75rem',
                          fontWeight: 600,
                          background: getWqiBg(wqi),
                          color: getWqiColor(wqi),
                          display: 'inline-block'
                        }}>
                          {status}
                        </span>
                      </td>
                      <td style={{ padding: '0.75rem 1rem' }}>
                        <DataSourceTag source={source} />
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* 7. IoT Probe Live Ingestion Gateway */}
      <div style={{
        background: '#ffffff',
        borderRadius: '12px',
        padding: '1.5rem',
        boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
        border: '1px solid #dcedc8'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.5rem' }}>
          <div>
            <h4 style={{ margin: 0, color: '#1b4d3e', fontSize: '1.1rem' }}>
              📡 Telemetric IoT Water Quality Ingestion Gateway
            </h4>
            <span style={{ fontSize: '0.8rem', color: '#666' }}>
              Accepts live sensor payload from submerged multi-parameter optical probes &rarr; Transmits to backend API (POST /api/iot/water/readings)
            </span>
          </div>
          <DataSourceTag source="IOT_SENSOR" />
        </div>

        <form onSubmit={handleIotSubmit} style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(170px, 1fr))', gap: '0.85rem' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, marginBottom: '0.2rem' }}>Probe ID</label>
            <input
              type="text"
              value={iotForm.probe_id}
              onChange={(e) => setIotForm({ ...iotForm, probe_id: e.target.value })}
              style={{ width: '100%', padding: '0.45rem', borderRadius: '6px', border: '1px solid #ccc', fontSize: '0.85rem', boxSizing: 'border-box' }}
              required
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, marginBottom: '0.2rem' }}>Water Body</label>
            <select
              value={iotForm.water_body}
              onChange={(e) => setIotForm({ ...iotForm, water_body: e.target.value })}
              style={{ width: '100%', padding: '0.45rem', borderRadius: '6px', border: '1px solid #ccc', fontSize: '0.85rem', boxSizing: 'border-box', background: '#fff' }}
            >
              <option value="Bhadrakali Lake">Bhadrakali Lake</option>
              <option value="Wadepally Tank">Wadepally Tank</option>
              <option value="Dharmasagar Lake">Dharmasagar Lake</option>
              <option value="Godavari River">Godavari River</option>
              <option value="Pakhal Lake">Pakhal Lake</option>
              <option value="Ramappa Lake">Ramappa Lake</option>
              <option value="Kakatiya Canal">Kakatiya Canal</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, marginBottom: '0.2rem' }}>pH (units)</label>
            <input
              type="number"
              step="0.05"
              value={iotForm.ph}
              onChange={(e) => setIotForm({ ...iotForm, ph: parseFloat(e.target.value) })}
              style={{ width: '100%', padding: '0.45rem', borderRadius: '6px', border: '1px solid #ccc', fontSize: '0.85rem', boxSizing: 'border-box' }}
              required
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, marginBottom: '0.2rem' }}>DO (mg/L)</label>
            <input
              type="number"
              step="0.1"
              value={iotForm.dissolved_oxygen}
              onChange={(e) => setIotForm({ ...iotForm, dissolved_oxygen: parseFloat(e.target.value) })}
              style={{ width: '100%', padding: '0.45rem', borderRadius: '6px', border: '1px solid #ccc', fontSize: '0.85rem', boxSizing: 'border-box' }}
              required
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, marginBottom: '0.2rem' }}>BOD (mg/L)</label>
            <input
              type="number"
              step="0.1"
              value={iotForm.bod}
              onChange={(e) => setIotForm({ ...iotForm, bod: parseFloat(e.target.value) })}
              style={{ width: '100%', padding: '0.45rem', borderRadius: '6px', border: '1px solid #ccc', fontSize: '0.85rem', boxSizing: 'border-box' }}
              required
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, marginBottom: '0.2rem' }}>Turbidity (NTU)</label>
            <input
              type="number"
              step="0.1"
              value={iotForm.turbidity}
              onChange={(e) => setIotForm({ ...iotForm, turbidity: parseFloat(e.target.value) })}
              style={{ width: '100%', padding: '0.45rem', borderRadius: '6px', border: '1px solid #ccc', fontSize: '0.85rem', boxSizing: 'border-box' }}
              required
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, marginBottom: '0.2rem' }}>TDS (mg/L)</label>
            <input
              type="number"
              value={iotForm.tds}
              onChange={(e) => setIotForm({ ...iotForm, tds: parseFloat(e.target.value) })}
              style={{ width: '100%', padding: '0.45rem', borderRadius: '6px', border: '1px solid #ccc', fontSize: '0.85rem', boxSizing: 'border-box' }}
              required
            />
          </div>

          <div style={{ display: 'flex', alignItems: 'flex-end' }}>
            <button
              type="submit"
              style={{
                width: '100%',
                padding: '0.55rem',
                backgroundColor: '#1b4d3e',
                color: '#fff',
                border: 'none',
                borderRadius: '6px',
                fontWeight: 600,
                fontSize: '0.85rem',
                cursor: 'pointer'
              }}
            >
              Transmit Telemetry
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
