import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const Dashboard = () => {
  console.log('=== Dashboard Component Rendering ===');
  
  const { user } = useAuth();
  console.log('Dashboard - User from context:', user);
  
  const [stats] = useState({
    totalMotos: 5,
    manutencoesPendentes: 2,
    proximasRevisoes: 3,
    gastosUltimoMes: 450.00
  });
  const [loading, setLoading] = useState(false);

  console.log('Dashboard - Initial state:', { stats, loading });

  useEffect(() => {
    console.log('Dashboard useEffect running...');
    // Mock data - no API calls for now
    setLoading(false);
  }, []);

  if (loading) {
    console.log('Dashboard still loading...');
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '400px' }}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Carregando...</span>
        </div>
      </div>
    );
  }

  console.log('Dashboard rendering main content...');

  return (
    <div className="container-fluid p-4">
      <div className="row mb-4">
        <div className="col-12">
          <h1 className="h3 mb-0">Dashboard</h1>
          <p className="mb-0 text-muted">
            Bem-vindo, {user?.first_name || user?.username || 'Usuário'}!
          </p>
        </div>
      </div>

      {/* Cards de Estatísticas */}
      <div className="row mb-4">
        <div className="col-lg-3 col-md-6 mb-3">
          <div className="card bg-primary text-white">
            <div className="card-body">
              <h5 className="card-title">Total de Motos</h5>
              <h2 className="display-4">{stats.totalMotos}</h2>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6 mb-3">
          <div className="card bg-warning text-white">
            <div className="card-body">
              <h5 className="card-title">Manutenções Pendentes</h5>
              <h2 className="display-4">{stats.manutencoesPendentes}</h2>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6 mb-3">
          <div className="card bg-info text-white">
            <div className="card-body">
              <h5 className="card-title">Próximas Revisões</h5>
              <h2 className="display-4">{stats.proximasRevisoes}</h2>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6 mb-3">
          <div className="card bg-success text-white">
            <div className="card-body">
              <h5 className="card-title">Gastos Último Mês</h5>
              <h2 className="display-4">R$ {stats.gastosUltimoMes.toFixed(0)}</h2>
            </div>
          </div>
        </div>
      </div>

      {/* Ações Rápidas */}
      <div className="row">
        <div className="col-lg-6 mb-4">
          <div className="card">
            <div className="card-header">
              <h5 className="card-title mb-0">Ações Rápidas</h5>
            </div>
            <div className="card-body">
              <div className="row">
                <div className="col-md-6 mb-3">
                  <Link to="/motos/novo" className="btn btn-primary w-100">
                    <i className="fas fa-plus me-2"></i>
                    Cadastrar Moto
                  </Link>
                </div>
                <div className="col-md-6 mb-3">
                  <Link to="/relatorios" className="btn btn-info w-100">
                    <i className="fas fa-chart-bar me-2"></i>
                    Ver Relatórios
                  </Link>
                </div>
                <div className="col-md-6 mb-3">
                  <Link to="/motos" className="btn btn-secondary w-100">
                    <i className="fas fa-list me-2"></i>
                    Listar Motos
                  </Link>
                </div>
                <div className="col-md-6 mb-3">
                  <Link to="/configuracoes" className="btn btn-dark w-100">
                    <i className="fas fa-cog me-2"></i>
                    Configurações
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-6 mb-4">
          <div className="card">
            <div className="card-header">
              <h5 className="card-title mb-0">Status do Sistema</h5>
            </div>
            <div className="card-body">
              <div className="alert alert-success">
                <i className="fas fa-check-circle me-2"></i>
                Sistema funcionando normalmente
              </div>
              <p>Dashboard carregado com sucesso!</p>
              <p>Todas as funcionalidades estão operacionais.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
