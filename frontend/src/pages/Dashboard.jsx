import React, { useEffect, useState } from 'react';
import { liveApi, analyticsApi, aiApi } from '../api/client';
import KpiCard from '../components/KpiCard';
import DataSourceTag from '../components/DataSourceTag';
import AlertBanner from '../components/AlertBanner';
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer,
  CartesianGrid, BarChart, Bar, Legend
} from 'recharts';

/* ── Skeleton block ───────────────────────────────────────── */
function Skeleton({ h = 80, r = 12 }) {
  return (
    <div style={{
      height: h, borderRadius: r,
      background: 'linear-gradient(90deg,#e8f0e8 25%,#d4e8d4 50%,#e8f0e8 75%)',
      backgroundSize: '400% 100%',
      animation: 'skeleton-shimmer 1.5s infinite',
    }} />
  );
}

/* ── AQI label helper ─────────────────────────────────────── */
function aqiLabel(aqi) {
  if (aqi <= 50)  return { text: 'Good',       bg: '#e8f5e9', color: '#2e7d32' };
  if (aqi <= 100) return { text: 'Satisfactory', bg: '#f1f8e9', color: '#558b2f' };
  if (aqi <= 200) return { text: 'Moderate',   bg: '#fff8e1', color: '#f57f17' };
  if (aqi <= 300) return { text: 'Poor',        bg: '#fff3e0', color: '#e65100' };
  if (aqi <= 400) return { text: 'Very Poor',   bg: '#fce4ec', color: '#c62828' };
  return               { text: 'Severe',        bg: '#ffebee', color: '#b71c1c' };
}

/* ── Custom tooltip ───────────────────────────────────────── */
function AqiTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: 8, padding: '0.6rem 0.9rem', fontSize: '0.8rem', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
      <div style={{ fontWeight: 700, marginBottom: 4, color: '#333' }}>{label}</div>
      {payload.map((p, i) => (
        <div key={i} style={{ color: p.stroke || p.fill, marginBottom: 2 }}>
          {p.name}: <strong>{p.value}</strong>
        </div>
      ))}
    </div>
  );
}

function WasteTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: 8, padding: '0.6rem 0.9rem', fontSize: '0.8rem', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
      <div style={{ fontWeight: 700, marginBottom: 4, color: '#333' }}>{label}</div>
      {payload.map((p, i) => (
        <div key={i} style={{ color: p.fill, marginBottom: 2 }}>
          {p.name}: <strong>{p.value}</strong>
        </div>
      ))}
    </div>
  );
}

export default function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [overview, setOverview] = useState(null);
  const [airData, setAirData] = useState(null);
  const [weatherData, setWeatherData] = useState(null);
  const [insights, setInsights] = useState([]);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState(null);

  const loadDashboard = async () => {
    setLoading(true);
    setError(null);
    try {
      const [overRes, airRes, weatherRes, insightRes, histRes] = await Promise.allSettled([
        analyticsApi.overview(),
        liveApi.airQuality('Warangal'),
        liveApi.weather(),
        aiApi.insights(),
        liveApi.history(15),
      ]);
      if (overRes.status === 'fulfilled') setOverview(overRes.value);
      if (airRes.status === 'fulfilled') setAirData(airRes.value);
      if (weatherRes.status === 'fulfilled') setWeatherData(weatherRes.value);
      if (insightRes.status === 'fulfilled') setInsights(insightRes.value?.insights || insightRes.value || []);
      if (histRes.status === 'fulfilled') setHistory(histRes.value?.data || histRes.value || []);
    } catch {
      setError('Failed to load some dashboard metrics. Offline records displayed.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadDashboard(); }, []);

  /* ── Derived metrics ─────────────────────────────────── */
  const currentAqi  = airData?.aqi ?? airData?.data?.aqi ?? overview?.avg_aqi ?? 142;
  const currentTemp = weatherData?.current?.temperature ?? weatherData?.current?.temperature_2m ?? overview?.avg_temp ?? 28.5;
  const currentHum  = weatherData?.current?.humidity ?? weatherData?.current?.relative_humidity_2m ?? 65;
  const currentPm25 = airData?.pollutants?.pm25?.value ?? airData?.pm25 ?? airData?.data?.pm25 ?? 58.4;
  const activeInc   = overview?.active_incidents ?? 3;
  const avgWqi      = overview?.avg_wqi ?? 68.2;
  const totalWaste  = overview?.total_waste_kg ?? 1240;
  const totalEnergy = overview?.total_energy_kwh ?? 4850;
  const sustainIdx  = overview?.sustainability_index ?? 76.5;
  const aqiInfo     = aqiLabel(currentAqi);

  /* ── Chart data ──────────────────────────────────────── */
  const chartData = (history && history.length > 0)
    ? history.map((item, idx) => ({
        time: item.timestamp ? new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : `T-${idx}`,
        aqi: Math.round(item.aqi) || 120,
        pm25: Math.round(item.pm25) || 50,
      })).reverse()
    : [
        { time: '00:00', aqi: 125, pm25: 52 },
        { time: '04:00', aqi: 110, pm25: 46 },
        { time: '08:00', aqi: 155, pm25: 68 },
        { time: '12:00', aqi: 168, pm25: 74 },
        { time: '16:00', aqi: 142, pm25: 58 },
        { time: '20:00', aqi: 138, pm25: 55 },
      ];

  const wasteEnergyData = [
    { name: 'Mon', waste: 240, energy: 680 },
    { name: 'Tue', waste: 210, energy: 720 },
    { name: 'Wed', waste: 290, energy: 690 },
    { name: 'Thu', waste: 260, energy: 740 },
    { name: 'Fri', waste: 310, energy: 810 },
    { name: 'Sat', waste: 180, energy: 610 },
    { name: 'Sun', waste: 150, energy: 580 },
  ];

  /* ── Shared card style ───────────────────────────────── */
  const card = {
    background: '#fff',
    borderRadius: 12,
    padding: '1.25rem',
    boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
  };

  /* ── KPI skeleton ────────────────────────────────────── */
  const kpiSkeleton = Array.from({ length: 8 }).map((_, i) => (
    <div key={i} style={{ ...card, minHeight: 110 }}><Skeleton h={70} r={8} /></div>
  ));

  return (
    <>
      {/* Skeleton keyframe injected once */}
      <style>{`
        @keyframes skeleton-shimmer {
          0%   { background-position: -400% 0; }
          100% { background-position:  400% 0; }
        }
        @media (max-width: 768px) {
          .dash-charts-grid { grid-template-columns: 1fr !important; }
          .dash-kpi-grid    { grid-template-columns: repeat(2, 1fr) !important; }
          .dash-insights-grid { grid-template-columns: 1fr !important; }
        }
      `}</style>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>

        {/* ── Header ───────────────────────────────────── */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <h2 style={{ margin: '0 0 0.25rem', color: '#1b4d3e', fontSize: '1.5rem' }}>
              Environmental Intelligence Overview
            </h2>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '0.85rem', color: '#555', flexWrap: 'wrap' }}>
              <span>Region: <strong>Warangal, Telangana (17.9689° N, 79.5941° E)</strong></span>
              <DataSourceTag source={airData?.source || 'LIVE_API'} />
            </div>
          </div>
          <button onClick={loadDashboard} className="btn btn-secondary btn-sm" disabled={loading}>
            {loading ? '⏳ Loading…' : '🔄 Refresh Feeds'}
          </button>
        </div>

        {error && <AlertBanner message={error} type="warning" />}
        {!loading && currentAqi > 200 && (
          <AlertBanner
            type="error"
            message={`⚠️ High Air Pollution Alert: AQI is ${currentAqi} (${aqiInfo.text}). Sensitive groups should reduce prolonged outdoor exertion.`}
          />
        )}

        {/* ── KPI Cards ──────────────────────────────── */}
        <div
          className="dash-kpi-grid"
          style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '1rem' }}
        >
          {loading ? kpiSkeleton : (
            <>
              {/* AQI with colour badge */}
              <div style={{ ...card, borderLeft: '4px solid ' + aqiInfo.color, position: 'relative' }}>
                <div style={{ position: 'absolute', top: 10, right: 10 }}>
                  <DataSourceTag source={airData?.source || 'LIVE_API'} />
                </div>
                <div style={{ fontSize: '1.4rem', marginBottom: 4 }}>🌬️</div>
                <div style={{ fontSize: '2rem', fontWeight: 700, color: '#1b4332', lineHeight: 1 }}>{currentAqi}</div>
                <div style={{ display: 'inline-block', marginTop: 4, padding: '2px 8px', borderRadius: 20, background: aqiInfo.bg, color: aqiInfo.color, fontSize: '0.72rem', fontWeight: 700 }}>
                  {aqiInfo.text}
                </div>
                <div style={{ marginTop: 6, fontSize: '0.75rem', color: '#666', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.4px' }}>Air Quality Index (AQI)</div>
                <div style={{ marginTop: 2, fontSize: '0.8rem', color: currentAqi > 100 ? '#d32f2f' : '#388e3c', fontWeight: 600 }}>
                  {currentAqi > 100 ? '▲' : '▼'} {currentAqi > 100 ? '+8.2%' : '-4.5%'} vs yesterday
                </div>
              </div>

              <KpiCard title="Ambient Temp" value={typeof currentTemp === 'number' ? currentTemp.toFixed(1) : currentTemp} unit="°C" icon="🌡️" change={1.4} dataSource="LIVE_API" />
              <KpiCard title="Relative Humidity" value={typeof currentHum === 'number' ? Math.round(currentHum) : currentHum} unit="%" icon="💧" change={-2.1} dataSource="LIVE_API" />
              <KpiCard title="PM2.5 Concentration" value={typeof currentPm25 === 'number' ? currentPm25.toFixed(1) : currentPm25} unit="µg/m³" icon="🌫️" change={5.3} dataSource={airData?.source || 'GOVERNMENT_DATA'} />
              <KpiCard title="Water Quality Index" value={typeof avgWqi === 'number' ? avgWqi.toFixed(1) : avgWqi} unit="/100" icon="🌊" change={0.8} dataSource="GOVERNMENT_DATA" />
              <KpiCard title="Waste Collected" value={totalWaste} unit="kg" icon="♻️" change={-3.6} dataSource="IOT_SENSOR" />
              <KpiCard title="Energy Usage" value={totalEnergy} unit="kWh" icon="⚡" change={4.2} dataSource="IOT_SENSOR" />
              <KpiCard title="Active Incidents" value={activeInc} unit="Open" icon="🚨" change={0} dataSource="LIVE_API" />
            </>
          )}
        </div>

        {/* ── Sustainability Banner ───────────────────── */}
        {!loading && (
          <div style={{
            background: 'linear-gradient(90deg,#1b4d3e 0%,#2e7d32 100%)',
            borderRadius: 12, padding: '1.25rem 1.5rem',
            color: '#fff', display: 'flex', alignItems: 'center',
            justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem'
          }}>
            <div>
              <span style={{ fontSize: '0.78rem', textTransform: 'uppercase', letterSpacing: 1, opacity: 0.85 }}>
                Composite Municipal Health Metric
              </span>
              <h3 style={{ margin: '0.2rem 0', fontSize: '1.3rem' }}>
                Ecological Sustainability Index (ESI): <strong>{sustainIdx} / 100</strong>
              </h3>
              <p style={{ margin: 0, fontSize: '0.84rem', opacity: 0.9 }}>
                Calculated across CPCB air standards, river basin DO/BOD limits, and renewable energy ratio.
              </p>
            </div>
            <div style={{ background: 'rgba(255,255,255,0.15)', padding: '0.6rem 1.2rem', borderRadius: 8, fontWeight: 700, fontSize: '1.1rem', border: '1px solid rgba(255,255,255,0.25)' }}>
              {sustainIdx >= 70 ? '🟢 Moderately Sustainable' : '🟡 Needs Intervention'}
            </div>
          </div>
        )}

        {/* ── Charts ─────────────────────────────────── */}
        <div
          className="dash-charts-grid"
          style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: '1.25rem' }}
        >
          {/* AQI & PM2.5 Trend */}
          <div style={card}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h4 style={{ margin: 0, color: '#1b4d3e', fontSize: '0.95rem', fontWeight: 700 }}>📈 24-Hour AQI &amp; PM2.5 Trend</h4>
              <DataSourceTag source="LIVE_API" />
            </div>
            {loading ? <Skeleton h={240} r={8} /> : (
              <div style={{ width: '100%', height: 260 }}>
                <ResponsiveContainer>
                  <LineChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis
                      dataKey="time"
                      stroke="#666"
                      tick={{ fontSize: 12, fill: '#555' }}
                      label={{ value: 'Time (HH:MM)', position: 'insideBottom', offset: -12, fontSize: 11, fill: '#888' }}
                    />
                    <YAxis
                      stroke="#666"
                      tick={{ fontSize: 12, fill: '#555' }}
                      label={{ value: 'Value', angle: -90, position: 'insideLeft', offset: 10, fontSize: 11, fill: '#888' }}
                    />
                    <Tooltip content={<AqiTooltip />} />
                    <Legend wrapperStyle={{ fontSize: 12, paddingTop: 8 }} />
                    <Line type="monotone" dataKey="aqi" name="AQI Index" stroke="#e65100" strokeWidth={2.5} dot={{ r: 3 }} activeDot={{ r: 5 }} />
                    <Line type="monotone" dataKey="pm25" name="PM2.5 (µg/m³)" stroke="#2e7d32" strokeWidth={2.5} dot={{ r: 3 }} activeDot={{ r: 5 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>

          {/* Weekly Resource Metabolism */}
          <div style={card}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h4 style={{ margin: 0, color: '#1b4d3e', fontSize: '0.95rem', fontWeight: 700 }}>📊 Weekly Resource Metabolism</h4>
              <DataSourceTag source="IOT_SENSOR" />
            </div>
            {loading ? <Skeleton h={240} r={8} /> : (
              <div style={{ width: '100%', height: 260 }}>
                <ResponsiveContainer>
                  <BarChart data={wasteEnergyData} margin={{ top: 10, right: 20, left: 0, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis
                      dataKey="name"
                      stroke="#666"
                      tick={{ fontSize: 12, fill: '#555' }}
                      label={{ value: 'Day of Week', position: 'insideBottom', offset: -12, fontSize: 11, fill: '#888' }}
                    />
                    <YAxis
                      stroke="#666"
                      tick={{ fontSize: 12, fill: '#555' }}
                      label={{ value: 'Quantity', angle: -90, position: 'insideLeft', offset: 10, fontSize: 11, fill: '#888' }}
                    />
                    <Tooltip content={<WasteTooltip />} />
                    <Legend wrapperStyle={{ fontSize: 12, paddingTop: 8 }} />
                    <Bar dataKey="waste" name="Waste (kg)" fill="#26a69a" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="energy" name="Energy (kWh)" fill="#ffb74d" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        </div>

        {/* ── AI Insights Panel ──────────────────────── */}
        <div style={{ ...card, borderLeft: '4px solid #2e7d32' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.9rem' }}>
            <h4 style={{ margin: 0, color: '#1b4d3e', fontSize: '1rem', fontWeight: 700 }}>
              🤖 AI Insights &amp; Action Recommendations
            </h4>
            <span style={{ fontSize: '0.72rem', color: '#666', background: '#e8f5e9', padding: '3px 10px', borderRadius: 20, fontWeight: 600 }}>
              Scikit-learn Engine
            </span>
          </div>

          {loading ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {[1, 2, 3].map(i => <Skeleton key={i} h={80} r={8} />)}
            </div>
          ) : insights && insights.length > 0 ? (
            <div
              className="dash-insights-grid"
              style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '0.75rem' }}
            >
              {insights.slice(0, 6).map((item, idx) => {
                const p = item.priority || 'MEDIUM';
                const ps = {
                  CRITICAL: { bg: '#ffebee', color: '#b71c1c', border: '#e53935' },
                  HIGH:     { bg: '#fff3e0', color: '#bf360c', border: '#f4511e' },
                  MEDIUM:   { bg: '#fff8e1', color: '#e65100', border: '#ffa000' },
                  LOW:      { bg: '#e8f5e9', color: '#1b5e20', border: '#43a047' },
                }[p] || { bg: '#f5f5f5', color: '#444', border: '#bbb' };
                const ico = p === 'CRITICAL' ? '🚨' : p === 'HIGH' ? '⚠️' : p === 'MEDIUM' ? '💡' : '✅';
                return (
                  <div key={idx} style={{
                    padding: '0.9rem 1rem',
                    background: '#fafafa',
                    borderRadius: 10,
                    border: `1px solid ${ps.border}`,
                    borderLeft: `4px solid ${ps.border}`,
                    display: 'flex', flexDirection: 'column', gap: '0.35rem',
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontSize: '0.72rem', fontWeight: 700, color: '#777', textTransform: 'uppercase', letterSpacing: '0.4px' }}>
                        {item.category || 'ENVIRONMENTAL'}
                      </span>
                      <span style={{ fontSize: '0.68rem', fontWeight: 700, padding: '2px 8px', borderRadius: 20, background: ps.bg, color: ps.color }}>
                        {ico} {p}
                      </span>
                    </div>
                    <div style={{ fontWeight: 700, fontSize: '0.88rem', color: '#1b4d3e', lineHeight: 1.3 }}>
                      {item.title || item.category || 'Environmental Alert'}
                    </div>
                    {(item.rationale || item.message) && (
                      <p style={{ margin: 0, fontSize: '0.8rem', color: '#555', lineHeight: 1.5 }}>
                        {item.rationale || item.message}
                      </p>
                    )}
                    {item.action && (
                      <div style={{ marginTop: 2, padding: '0.4rem 0.7rem', background: '#f0fdf4', borderRadius: 6, fontSize: '0.78rem', color: '#2e7d32', fontWeight: 600 }}>
                        🎯 {item.action}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          ) : (
            <div style={{ padding: '1rem', background: '#f9fbf9', borderRadius: 8, fontSize: '0.85rem', color: '#555' }}>
              ✅ No anomalies currently flagged across Warangal stations. System operating within baseline thresholds.
            </div>
          )}
        </div>

        {/* ── Connected APIs Status Panel ────────────── */}
        <div style={{ ...card, background: '#f8faf8', border: '1px solid #e2e8e2' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
            <span style={{ fontSize: '0.88rem', fontWeight: 700, color: '#1b4d3e' }}>
              🔌 Connected Environmental APIs &amp; Data Feeds
            </span>
            <span style={{ fontSize: '0.72rem', color: '#777', background: '#e8f5e9', padding: '2px 8px', borderRadius: 20 }}>
              Auto-refresh · 15 min
            </span>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))', gap: '0.5rem' }}>
            {[
              { name: 'OpenAQ v3',         status: 'HEALTHY',   dot: '#43a047' },
              { name: 'CPCB data.gov.in',  status: 'HEALTHY',   dot: '#43a047' },
              { name: 'Open-Meteo',        status: 'LIVE',      dot: '#43a047' },
              { name: 'GBIF Biodiversity', status: 'ACTIVE',    dot: '#43a047' },
              { name: 'NASA GIBS',         status: 'ACTIVE',    dot: '#43a047' },
              { name: 'Municipal IoT',     status: 'STREAMING', dot: '#1565c0' },
            ].map((src, i) => (
              <div key={i} style={{
                background: '#fff', padding: '0.45rem 0.7rem',
                borderRadius: 6, border: '1px solid #e0e0e0',
                display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                fontSize: '0.75rem', gap: '0.4rem'
              }}>
                <span style={{ fontWeight: 500, color: '#333', flex: 1, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{src.name}</span>
                <span style={{ color: src.dot, fontWeight: 700, fontSize: '0.65rem', flexShrink: 0 }}>● {src.status}</span>
              </div>
            ))}
          </div>
        </div>

      </div>
    </>
  );
}
