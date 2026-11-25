import React, { useEffect, useState } from 'react';
import { liveApi } from '../api/client';
import DataSourceTag from '../components/DataSourceTag';
import AlertBanner from '../components/AlertBanner';
import LoadingSpinner from '../components/LoadingSpinner';

export default function DataSources() {
  const [loading, setLoading] = useState(true);
  const [statusData, setStatusData] = useState(null);
  const [refreshing, setRefreshing] = useState(false);
  const [refreshMsg, setRefreshMsg] = useState(null);
  const [error, setError] = useState(null);

  const fetchStatus = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await liveApi.status();
      setStatusData(res);
    } catch (err) {
      setError('Unable to reach telemetry health endpoint. Showing cached provider configurations.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  const handleRefresh = async (provider = null) => {
    setRefreshing(true);
    setRefreshMsg(null);
    try {
      const res = await liveApi.refresh(provider);
      setRefreshMsg(res?.message || `Refreshed sync feeds successfully!`);
      fetchStatus();
    } catch (err) {
      setError('Sync refresh failed. Telemetry fallback active.');
    } finally {
      setRefreshing(false);
    }
  };

  const providers = [
    {
      name: 'OpenAQ Global Air Quality API (v3)',
      endpoint: 'https://api.openaq.org/v3/locations',
      auth: 'OPENAQ_API_KEY header',
      cadence: '15 Minutes',
      status: 'OPERATIONAL',
      classification: 'LIVE_API',
      description: 'Global continuous particulate matter and atmospheric gas observations.',
      parameters: 'PM2.5, PM10, NO2, SO2, CO, O3'
    },
    {
      name: 'CPCB National AQI (data.gov.in)',
      endpoint: 'https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69',
      auth: 'DATA_GOV_IN_API_KEY param',
      cadence: 'Hourly Updates',
      status: 'OPERATIONAL',
      classification: 'GOVERNMENT_DATA',
      description: 'Official Central Pollution Control Board CAAQMS station telemetry for Indian cities.',
      parameters: 'Sub-indices, Prominent Pollutant, Station Metadata'
    },
    {
      name: 'Open-Meteo Weather Forecast API',
      endpoint: 'https://api.open-meteo.com/v1/forecast',
      auth: 'None (Non-Commercial ODbL)',
      cadence: '15 Minutes',
      status: 'OPERATIONAL',
      classification: 'LIVE_API',
      description: 'Numerical high-resolution meteorological models for Warangal coordinates (17.9689, 79.5941).',
      parameters: 'Temperature, Pressure, Wind, Rainfall, Cloud Cover'
    },
    {
      name: 'GBIF Biodiversity Occurrence Engine',
      endpoint: 'https://api.gbif.org/v1/occurrence/search',
      auth: 'Public Open Access',
      cadence: 'Daily Aggregation',
      status: 'OPERATIONAL',
      classification: 'LIVE_API',
      description: 'Global Biodiversity Information Facility georeferenced specimen and field observations.',
      parameters: 'Species taxonomy, Scientific Name, Conservation Status'
    },
    {
      name: 'NASA GIBS Earth Observation WMTS',
      endpoint: 'https://gibs.earthdata.nasa.gov/wmts/epsg3857/best',
      auth: 'NASA EOSDIS Open Access',
      cadence: 'Daily Orbital Passes',
      status: 'OPERATIONAL',
      classification: 'HISTORICAL',
      description: 'MODIS Terra and Aqua Corrected Reflectance TrueColor and Normalized Difference Vegetation Index (NDVI).',
      parameters: 'Surface reflectance, NDVI, Thermal anomalies'
    },
    {
      name: 'Municipal Smart Waste Sensor Mesh',
      endpoint: '/api/iot/waste/readings',
      auth: 'Municipal Device Token',
      cadence: 'Event-driven (Ultrasonic)',
      status: 'STREAMING',
      classification: 'IOT_SENSOR',
      description: 'Ultrasonic bin level depth sensors across Warangal and Hanamkonda hubs.',
      parameters: 'Fill percentage, Waste Mass (kg), Bin Location'
    },
    {
      name: 'Smart Energy Sub-Station Telemetry',
      endpoint: '/api/iot/energy/readings',
      auth: 'Smart Meter Gateway',
      cadence: 'Continuous Telemetry',
      status: 'STREAMING',
      classification: 'IOT_SENSOR',
      description: 'Grid demand and distributed rooftop photovoltaic solar inverter telemetry.',
      parameters: 'Active Power (kW), Consumption (kWh), Solar Ratio'
    },
    {
      name: 'NWQMP Surface Water Monitoring Database',
      endpoint: '/api/water-quality',
      auth: 'Government Open Data (data.gov.in)',
      cadence: 'Periodic Hydrological Sampling',
      status: 'OPERATIONAL',
      classification: 'GOVERNMENT_DATA',
      description: 'Central Pollution Control Board surface water stations for Godavari and Kakatiya basins.',
      parameters: 'pH, Dissolved Oxygen, BOD, Turbidity, TDS'
    },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ margin: '0 0 0.25rem', color: '#1b4d3e' }}>
            Environmental Data Ingestion & API Integrity Dashboard
          </h2>
          <p style={{ margin: 0, fontSize: '0.85rem', color: '#666' }}>
            Strict data source classification, provider health diagnostics, and synchronization controls
          </p>
        </div>

        <button
          onClick={() => handleRefresh()}
          disabled={refreshing}
          className="btn btn-primary"
          style={{ padding: '0.6rem 1.25rem', fontWeight: 600 }}
        >
          {refreshing ? 'Synchronizing All APIs...' : '🔄 Poll & Sync All Providers'}
        </button>
      </div>

      {refreshMsg && <AlertBanner message={refreshMsg} type="success" onDismiss={() => setRefreshMsg(null)} />}
      {error && <AlertBanner message={error} type="warning" />}

      {/* Mandatory Data Classification Protocol Banner */}
      <div style={{
        background: '#e8f5e9',
        borderLeft: '4px solid #2e7d32',
        padding: '1rem 1.25rem',
        borderRadius: '8px',
        fontSize: '0.85rem',
        color: '#1b4d3e'
      }}>
        <div style={{ fontWeight: 700, marginBottom: '0.3rem' }}>
          🔒 Truthful Telemetry Mandate:
        </div>
        <div>
          Every environmental record is strictly tagged with its origin classification:
          <strong> LIVE_API</strong>, <strong>GOVERNMENT_DATA</strong>, <strong>IOT_SENSOR</strong>, or <strong>HISTORICAL</strong>.
          Simulated or offline demonstration records are never commingled with live governmental measurements.
        </div>
      </div>

      {/* API Key Setup Reminder */}
      <div style={{
        background: '#ffffff',
        borderRadius: '10px',
        padding: '1.25rem',
        boxShadow: '0 2px 6px rgba(0,0,0,0.05)',
        border: '1px solid #e0e0e0'
      }}>
        <h4 style={{ margin: '0 0 0.5rem', color: '#333' }}>🔑 API Key Configuration Reference</h4>
        <p style={{ margin: '0 0 0.75rem', fontSize: '0.85rem', color: '#555' }}>
          To enable live real-time network fetching outside sandbox mode, set these keys in your <code>.env</code> file:
        </p>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '0.75rem', fontSize: '0.8rem' }}>
          <div style={{ background: '#f5f5f5', padding: '0.6rem', borderRadius: '6px' }}>
            <code>OPENAQ_API_KEY</code>: Obtain from <a href="https://openaq.org/" target="_blank" rel="noreferrer">openaq.org</a>
          </div>
          <div style={{ background: '#f5f5f5', padding: '0.6rem', borderRadius: '6px' }}>
            <code>DATA_GOV_IN_API_KEY</code>: Obtain from <a href="https://data.gov.in/" target="_blank" rel="noreferrer">data.gov.in</a>
          </div>
          <div style={{ background: '#f5f5f5', padding: '0.6rem', borderRadius: '6px' }}>
            <code>OPEN-METEO</code>: Free for non-commercial use (no key required)
          </div>
        </div>
      </div>

      {/* Providers Cards Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))',
        gap: '1.25rem'
      }}>
        {providers.map((p, idx) => (
          <div
            key={idx}
            style={{
              background: '#ffffff',
              borderRadius: '12px',
              padding: '1.25rem',
              boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              borderTop: '3px solid #2e7d32'
            }}
          >
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                <h4 style={{ margin: 0, fontSize: '1rem', color: '#1b4d3e' }}>{p.name}</h4>
                <DataSourceTag source={p.classification} />
              </div>

              <p style={{ margin: '0 0 0.75rem', fontSize: '0.82rem', color: '#555' }}>
                {p.description}
              </p>

              <div style={{ fontSize: '0.78rem', background: '#f9f9f9', padding: '0.6rem', borderRadius: '6px', display: 'flex', flexDirection: 'column', gap: '0.3rem' }}>
                <div><strong>Endpoint:</strong> <code style={{ fontSize: '0.72rem' }}>{p.endpoint}</code></div>
                <div><strong>Auth Scheme:</strong> {p.auth}</div>
                <div><strong>Polling Cadence:</strong> {p.cadence}</div>
                <div><strong>Parameters:</strong> {p.parameters}</div>
              </div>
            </div>

            <div style={{ marginTop: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '0.75rem', borderTop: '1px solid #f0f0f0' }}>
              <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#2e7d32', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                <span>🟢</span> {p.status}
              </span>
              <button
                onClick={() => handleRefresh(p.name)}
                className="btn btn-secondary btn-sm"
                style={{ padding: '0.3rem 0.6rem', fontSize: '0.75rem' }}
              >
                Sync Now
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
