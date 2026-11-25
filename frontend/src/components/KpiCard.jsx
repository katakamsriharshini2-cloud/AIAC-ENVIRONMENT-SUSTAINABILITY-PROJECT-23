import React from 'react';
import DataSourceTag from './DataSourceTag';

export default function KpiCard({ title, value, unit, change, icon, dataSource, loading }) {
  if (loading) {
    return (
      <div className="kpi-card">
        <div style={{ height: 70, background: '#e8f0e8', borderRadius: 8, animation: 'skeleton-shimmer 1.5s infinite' }} />
      </div>
    );
  }

  const displayValue = (value === null || value === undefined) ? 'N/A' : value;

  let changeEl = null;
  if (change !== null && change !== undefined && !isNaN(change)) {
    if (change > 0) {
      changeEl = <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#d32f2f' }}>▲ +{change}%</span>;
    } else if (change < 0) {
      changeEl = <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#388e3c' }}>▼ {change}%</span>;
    } else {
      changeEl = <span style={{ fontSize: '0.78rem', fontWeight: 600, color: '#888' }}>— 0%</span>;
    }
  }

  return (
    <div className="kpi-card" style={{ position: 'relative', minHeight: 110 }}>
      {dataSource && (
        <div style={{ position: 'absolute', top: '0.6rem', right: '0.6rem' }}>
          <DataSourceTag source={dataSource} />
        </div>
      )}

      {icon && (
        <div style={{
          display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
          width: '2.2rem', height: '2.2rem', borderRadius: '50%',
          background: 'rgba(46,125,50,0.12)', fontSize: '1.2rem', marginBottom: '0.4rem',
        }}>
          {icon}
        </div>
      )}

      <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.2rem', marginTop: '0.1rem' }}>
        <span className="kpi-value" style={{ fontSize: '2rem', fontWeight: 700, color: '#1b4332', lineHeight: 1 }}>
          {displayValue}
        </span>
        {unit && <span className="kpi-unit" style={{ fontSize: '0.8rem', color: '#666', fontWeight: 600 }}>{unit}</span>}
      </div>

      <div className="kpi-label" style={{ marginTop: '0.3rem', fontSize: '0.74rem', color: '#5a7a62', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.4px' }}>
        {title}
      </div>

      {changeEl && <div style={{ marginTop: '0.25rem' }}>{changeEl}</div>}
    </div>
  );
}
