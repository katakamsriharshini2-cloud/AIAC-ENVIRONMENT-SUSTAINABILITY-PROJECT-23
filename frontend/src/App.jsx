import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { AuthProvider, useAuth } from './hooks/useAuth';
import Sidebar from './components/Sidebar';
import TopBar from './components/TopBar';
import ErrorBoundary from './components/ErrorBoundary';

// Page imports
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AirQuality from './pages/AirQuality';
import WaterQuality from './pages/WaterQuality';
import Weather from './pages/Weather';
import Analytics from './pages/Analytics';
import AIForecasting from './pages/AIForecasting';
import Optimization from './pages/Optimization';
import PublicPortal from './pages/PublicPortal';
import MapView from './pages/MapView';
import DataSources from './pages/DataSources';
import Incidents from './pages/Incidents';
import Biodiversity from './pages/Biodiversity';

function ProtectedLayout() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="app-layout">
      <Sidebar />
      <div className="main-content">
        <TopBar title="Dashboard" />
        <div className="page-content">
          <Outlet />
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <ErrorBoundary>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route element={<ProtectedLayout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/air-quality" element={<AirQuality />} />
            <Route path="/water-quality" element={<WaterQuality />} />
            <Route path="/weather" element={<Weather />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/ai-forecasting" element={<AIForecasting />} />
            <Route path="/optimization" element={<Optimization />} />
            <Route path="/portal" element={<PublicPortal />} />
            <Route path="/map" element={<MapView />} />
            <Route path="/data-sources" element={<DataSources />} />
            <Route path="/incidents" element={<Incidents />} />
            <Route path="/biodiversity" element={<Biodiversity />} />
          </Route>
        </Routes>
        </ErrorBoundary>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
