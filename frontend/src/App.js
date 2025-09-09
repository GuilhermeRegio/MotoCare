import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Login from './components/Login/Login';
import Dashboard from './components/Dashboard/DashboardSimple';
import MotosList from './components/Motos/MotosList';
import MotosForm from './components/Motos/MotosForm';
import MotoDetail from './components/Motos/MotoDetail';
import Reports from './components/Reports/Reports';
import Settings from './components/Settings/Settings';
import Layout from './components/Layout/Layout';
import ProtectedRoute from './components/Auth/ProtectedRoute';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/*" element={
              <ProtectedRoute>
                <Layout>
                  <Routes>
                    <Route path="/" element={<Navigate to="/dashboard" replace />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/motos" element={<MotosList />} />
                    <Route path="/motos/novo" element={<MotosForm />} />
                    <Route path="/motos/:id" element={<MotoDetail />} />
                    <Route path="/motos/:id/editar" element={<MotosForm />} />
                    <Route path="/relatorios" element={<Reports />} />
                    <Route path="/configuracoes" element={<Settings />} />
                  </Routes>
                </Layout>
              </ProtectedRoute>
            } />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
