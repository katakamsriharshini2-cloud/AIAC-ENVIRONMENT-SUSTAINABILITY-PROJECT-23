import React from 'react';

const SOURCE_MAP = {
  LIVE_API: { className: 'source-tag source-live', text: '● LIVE' },
  HISTORICAL: { className: 'source-tag source-historical', text: '📁 HIST' },
  GOVERNMENT_DATA: { className: 'source-tag source-government', text: '🏛️ GOVT' },
  IOT_SENSOR: { className: 'source-tag source-iot', text: '📡 IoT' },
  SIMULATED: { className: 'source-tag source-simulated', text: '◉ DEMO' },
  OFFLINE: { className: 'source-tag source-offline', text: '⭕ OFFLINE' },
  STALE: { className: 'source-tag source-offline', text: '⭕ OFFLINE' },
};

export default function DataSourceTag({ source }) {
  const mapping = SOURCE_MAP[source];
  if (mapping) {
    return <span className={mapping.className}>{mapping.text}</span>;
  }
  return <span className="source-tag">{source}</span>;
}
