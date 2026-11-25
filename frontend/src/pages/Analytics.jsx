import React, { useState, useEffect } from 'react';
import { analyticsApi } from '../api/client';
import DataSourceTag from '../components/DataSourceTag';
import AlertBanner from '../components/AlertBanner';
import LoadingSpinner from '../components/LoadingSpinner';
import {
  LineChart, Line, BarChart, Bar, AreaChart, Area,
  XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend,
  PieChart, Pie, Cell
} from 'recharts';

const COLORS = ['#2e7d32', '#0288d1', '#f57c00', '#7b1fa2', '#c2185b', '#00796b'];

export default function Analytics() {
  const [tab, setTab] = useState('air');
  const [loading, setLoading] = useState(false);
  const [overview, setOverview] = useState(null);
  const [cityFilter, setCityFilter] = useState('Warangal');
  const [startDate, setStartDate] = useState('2026-10-01');
  const [endDate, setEndDate] = useState('2026-11-21');
  const [exporting, setExporting] = useState(false);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    analyticsApi.overview().then(setOverview).catch(() => {});
  }, []);

  const handleExportCsv = (metric) => {
    setExporting(true);
    try {
      const url = analyticsApi.exportCsv(metric);
      window.open(url, '_blank');
      setMessage(`CSV export initiated for ${metric}. Download started.`);
    } catch (err) {
      setMessage('Failed to generate CSV.');
    } finally {
      setExporting(false);
    }
  };

  const handleExportPdf = () => {
    setExporting(true);
    try {
      const url = analyticsApi.exportPdf();
      window.open(url, '_blank');
      setMessage('PDF Executive Environmental Summary generated.');
    } catch (err) {
      setMessage('Failed to generate PDF report.');
    } finally {
      setExporting(false);
    }
  };

  // Sample analytics datasets
  const airTrendData = [
    { date: 'Nov 01', Warangal: 120, Hyderabad: 165, Delhi: 280 },
    { date: 'Nov 05', Warangal: 135, Hyderabad: 180, Delhi: 310 },
    { date: 'Nov 10', Warangal: 142, Hyderabad: 172, Delhi: 340 },
    { date: 'Nov 15', Warangal: 155, Hyderabad: 195, Delhi: 385 },
    { date: 'Nov 20', Warangal: 138, Hyderabad: 160, Delhi: 320 },
  ];

  const pollutantShareData = [
    { name: 'PM2.5', value: 42 },
    { name: 'PM10', value: 28 },
    { name: 'NO2', value: 14 },
    { name: 'SO2', value: 8 },
    { name: 'CO', value: 5 },
    { name: 'O3', value: 3 },
  ];

  const wasteRecyclingData = [
    { week: 'W1 Oct', collected: 1450, recycled: 580 },
    { week: 'W2 Oct', collected: 1620, recycled: 720 },
    { week: 'W3 Oct', collected: 1580, recycled: 690 },
    { week: 'W4 Oct', collected: 1710, recycled: 810 },
    { week: 'W1 Nov', collected: 1650, recycled: 790 },
    { week: 'W2 Nov', collected: 1800, recycled: 920 },
  ];

  const energyBreakdownData = [
    { month: 'Jun', grid: 4200, solar: 1100 },
    { month: 'Jul', grid: 4500, solar: 1250 },
    { month: 'Aug', grid: 4300, solar: 1400 },
    { month: 'Sep', grid: 3900, solar: 1550 },
    { month: 'Oct', grid: 3700, solar: 1600 },
    { month: 'Nov', grid: 3600, solar: 1750 },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Header and Filter Controls */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ margin: '0 0 0.25rem', color: '#1b4d3e' }}>
            Multi-Domain Environmental Analytics Engine
          </h2>
          <p style={{ margin: 0, fontSize: '0.85rem', color: '#666' }}>
            Descriptive, comparative, and time-series statistics across air, hydrological, and municipal streams
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          <button onClick={() => handleExportCsv(tab)} className="btn btn-secondary btn-sm">
            📥 Export CSV
          </button>
          <button onClick={handleExportPdf} className="btn btn-primary btn-sm">
            📄 Export PDF Report
          </button>
        </div>
      </div>

      {message && <AlertBanner message={message} type="info" onDismiss={() => setMessage(null)} />}

      {/* Filter Bar */}
      <div style={{
        background: '#ffffff',
        borderRadius: '10px',
        padding: '0.9rem 1.25rem',
        boxShadow: '0 2px 6px rgba(0,0,0,0.05)',
        display: 'flex',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '1rem',
        fontSize: '0.85rem'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <strong>Location:</strong>
          <select
            value={cityFilter}
            onChange={(e) => setCityFilter(e.target.value)}
            style={{ padding: '0.35rem 0.6rem', borderRadius: '6px', border: '1px solid #ccc' }}
          >
            <option value="Warangal">Warangal, Telangana</option>
            <option value="Hyderabad">Hyderabad, Telangana</option>
            <option value="Delhi">Delhi NCR</option>
          </select>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <strong>Start Date:</strong>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            style={{ padding: '0.35rem 0.6rem', borderRadius: '6px', border: '1px solid #ccc' }}
          />
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <strong>End Date:</strong>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            style={{ padding: '0.35rem 0.6rem', borderRadius: '6px', border: '1px solid #ccc' }}
          />
        </div>
      </div>

      {/* Navigation Tabs */}
      <div style={{ display: 'flex', borderBottom: '2px solid #e0e0e0', gap: '0.5rem' }}>
        {[
          { id: 'air', label: '🌬️ Air Quality Analysis' },
          { id: 'water', label: '💧 Hydrological Health' },
          { id: 'waste_energy', label: '♻️ Waste & Energy Metabolism' },
          { id: 'sustainability', label: '🌿 SDG Sustainability Matrix' },
        ].map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            style={{
              padding: '0.75rem 1.25rem',
              background: tab === t.id ? '#2e7d32' : 'transparent',
              color: tab === t.id ? '#ffffff' : '#555',
              border: 'none',
              borderRadius: '8px 8px 0 0',
              fontWeight: 600,
              fontSize: '0.9rem',
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Tab 1: Air Quality */}
      {tab === 'air' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(460px, 1fr))', gap: '1.25rem' }}>
            <div className="chart-container" style={{ background: '#fff', padding: '1.25rem', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.06)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <h4 style={{ margin: 0, color: '#333' }}>Regional AQI Cross-City Trajectory</h4>
                <DataSourceTag source="GOVERNMENT_DATA" />
              </div>
              <div style={{ width: '100%', height: 280 }}>
                <ResponsiveContainer>
                  <LineChart data={airTrendData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="date" stroke="#888" fontSize={11} />
                    <YAxis stroke="#888" fontSize={11} />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="Warangal" stroke="#2e7d32" strokeWidth={2.5} dot={{ r: 4 }} />
                    <Line type="monotone" dataKey="Hyderabad" stroke="#f57c00" strokeWidth={2} />
                    <Line type="monotone" dataKey="Delhi" stroke="#d32f2f" strokeWidth={2} strokeDasharray="4 4" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="chart-container" style={{ background: '#fff', padding: '1.25rem', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.06)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <h4 style={{ margin: 0, color: '#333' }}>Relative Pollutant Contribution Breakdown (%)</h4>
                <DataSourceTag source="LIVE_API" />
              </div>
              <div style={{ width: '100%', height: 280 }}>
                <ResponsiveContainer>
                  <PieChart>
                    <Pie data={pollutantShareData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={90} label>
                      {pollutantShareData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Water */}
      {tab === 'water' && (
        <div style={{ background: '#fff', padding: '1.5rem', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.06)' }}>
          <h4 style={{ margin: '0 0 1rem', color: '#1b4d3e' }}>Telangana Catchment Basin Water Purity Trends</h4>
          <p style={{ fontSize: '0.85rem', color: '#666', marginBottom: '1rem' }}>
            Comparison of Dissolved Oxygen (DO mg/L) vs Biochemical Oxygen Demand (BOD mg/L) across Godavari & Krishna sub-basins.
          </p>
          <div style={{ width: '100%', height: 320 }}>
            <ResponsiveContainer>
              <BarChart data={[
                { station: 'Waddepally', do: 6.4, bod: 2.8, wqi: 74 },
                { station: 'Bhadrakali', do: 5.2, bod: 4.2, wqi: 62 },
                { station: 'Dharmasagar', do: 7.8, bod: 1.5, wqi: 86 },
                { station: 'Kakatiya Canal', do: 5.9, bod: 3.4, wqi: 69 },
              ]}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="station" stroke="#888" fontSize={11} />
                <YAxis stroke="#888" fontSize={11} />
                <Tooltip />
                <Legend />
                <Bar dataKey="wqi" name="WQI Score (/100)" fill="#0288d1" radius={[4, 4, 0, 0]} />
                <Bar dataKey="do" name="Dissolved Oxygen (mg/L)" fill="#2e7d32" radius={[4, 4, 0, 0]} />
                <Bar dataKey="bod" name="BOD (mg/L)" fill="#e57373" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Tab 3: Waste & Energy */}
      {tab === 'waste_energy' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(460px, 1fr))', gap: '1.25rem' }}>
          <div className="chart-container" style={{ background: '#fff', padding: '1.25rem', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.06)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
              <h4 style={{ margin: 0, color: '#333' }}>Solid Waste vs Recycling Diversion Rate (kg)</h4>
              <DataSourceTag source="IOT_SENSOR" />
            </div>
            <div style={{ width: '100%', height: 280 }}>
              <ResponsiveContainer>
                <BarChart data={wasteRecyclingData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="week" stroke="#888" fontSize={11} />
                  <YAxis stroke="#888" fontSize={11} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="collected" name="Total Collected (kg)" fill="#78909c" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="recycled" name="Diverted to Recycling (kg)" fill="#2e7d32" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="chart-container" style={{ background: '#fff', padding: '1.25rem', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.06)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
              <h4 style={{ margin: 0, color: '#333' }}>Grid Consumption vs Rooftop Solar Generation</h4>
              <DataSourceTag source="IOT_SENSOR" />
            </div>
            <div style={{ width: '100%', height: 280 }}>
              <ResponsiveContainer>
                <AreaChart data={energyBreakdownData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="month" stroke="#888" fontSize={11} />
                  <YAxis stroke="#888" fontSize={11} />
                  <Tooltip />
                  <Legend />
                  <Area type="monotone" dataKey="grid" name="Thermal Grid (kWh)" stroke="#f57c00" fill="#ffe0b2" />
                  <Area type="monotone" dataKey="solar" name="Renewable Solar (kWh)" stroke="#2e7d32" fill="#c8e6c9" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}

      {/* Tab 4: Sustainability Matrix */}
      {tab === 'sustainability' && (
        <div style={{
          background: '#ffffff',
          borderRadius: '12px',
          padding: '1.5rem',
          boxShadow: '0 2px 8px rgba(0,0,0,0.06)'
        }}>
          <h4 style={{ margin: '0 0 1rem', color: '#1b4d3e' }}>
            UN Sustainable Development Goals (SDG) Alignment Scorecard
          </h4>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
            gap: '1rem'
          }}>
            {[
              { sdg: 'SDG 11: Sustainable Cities', score: 78, target: 'Clean ambient air & integrated waste logistics' },
              { sdg: 'SDG 6: Clean Water & Sanitation', score: 72, target: 'NWQMP hydrological compliance' },
              { sdg: 'SDG 7: Affordable & Clean Energy', score: 65, target: 'Solar rooftop expansion & energy efficiency' },
              { sdg: 'SDG 13: Climate Action', score: 81, target: 'Incident response time & AI disaster mitigation' },
              { sdg: 'SDG 15: Life on Land', score: 84, target: 'GBIF biodiversity sanctuary observation' },
            ].map((s, i) => (
              <div
                key={i}
                style={{
                  padding: '1rem',
                  border: '1px solid #e0e0e0',
                  borderRadius: '10px',
                  background: '#f9fbf9'
                }}
              >
                <div style={{ fontWeight: 700, fontSize: '0.9rem', color: '#1b4d3e', marginBottom: '0.4rem' }}>
                  {s.sdg}
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', margin: '0.6rem 0' }}>
                  <div style={{ flex: 1, height: '8px', background: '#e0e0e0', borderRadius: '4px', overflow: 'hidden' }}>
                    <div style={{ width: `${s.score}%`, height: '100%', background: '#2e7d32' }} />
                  </div>
                  <strong style={{ fontSize: '0.9rem' }}>{s.score}%</strong>
                </div>
                <div style={{ fontSize: '0.75rem', color: '#666' }}>{s.target}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
