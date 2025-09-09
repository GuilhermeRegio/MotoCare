import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { dashboardService } from '../../services/authService';
import { useAuth } from '../../contexts/AuthContext';
import './Dashboard.css';

const Dashboard = () => {
  console.log('=== Dashboard Component Rendering ===');
  
  const { user } = useAuth();
  console.log('Dashboard - User from context:', user);
  
  const [dashboardData, setDashboardData] = useState({
    total_motos: 0,
    moto_principal: null,
    metricas: {
      total_manutencoes: 0,
      total_gasto: 0,
      media_km: 0
    }
  });
  const [loading, setLoading] = useState(true);

  console.log('Dashboard - Initial state:', { dashboardData, loading });

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const data = await dashboardService.getDashboardData();
      if (data && data.success) {
        setDashboardData(data.data);
      } else {
        // Dados mockados quando a API não responde
        setDashboardData({
          total_motos: 5,
          moto_principal: {
            id: 1,
            marca: 'Dafra',
            modelo: 'Cruisym 300',
            ano: 2025,
            km_atual: 12500,
            km_total_percorridos: 12500,
            idade_anos: 0
          },
          metricas: {
            total_manutencoes: 8,
            total_gasto: 2500.00,
            media_km: 0.20
          }
        });
      }
    } catch (error) {
      console.error('Erro ao carregar dados do dashboard:', error);
      // Dados mockados em caso de erro
      setDashboardData({
        total_motos: 5,
        moto_principal: {
          id: 1,
          marca: 'Dafra',
          modelo: 'Cruisym 300',
          ano: 2025,
          km_atual: 12500,
          km_total_percorridos: 12500,
          idade_anos: 0
        },
        metricas: {
          total_manutencoes: 8,
          total_gasto: 2500.00,
          media_km: 0.20
        }
      });
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{minHeight: '400px'}}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Carregando...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      {/* Header do Dashboard */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <h1 className="mb-1">
                <i className="fas fa-tachometer-alt text-primary me-2"></i>
                Dashboard
              </h1>
              <p className="text-muted mb-0">
                Bem-vindo de volta, {user?.first_name || user?.username || 'Usuário'}!
              </p>
            </div>
            <div>
              <Link to="/motos/novo" className="btn btn-primary btn-lg">
                <i className="fas fa-plus me-2"></i>Adicionar Moto
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Cards de Métricas */}
      <div className="row mb-4">
        <div className="col-md-3 mb-3">
          <div className="card h-100 border-0 shadow-sm">
            <div className="card-body text-center p-4">
              <div className="d-flex align-items-center justify-content-center mb-3">
                <div className="rounded-circle bg-primary bg-opacity-10 p-3 me-3">
                  <i className="fas fa-motorcycle fa-2x text-primary"></i>
                </div>
                <div className="text-start">
                  <h2 className="mb-0 fw-bold text-primary">{dashboardData.total_motos}</h2>
                  <small className="text-muted">Total de Motos</small>
                </div>
              </div>
              <div className="progress" style={{height: '6px'}}>
                <div className="progress-bar bg-primary" role="progressbar" style={{width: '100%'}}></div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3 mb-3">
          <div className="card h-100 border-0 shadow-sm">
            <div className="card-body text-center p-4">
              <div className="d-flex align-items-center justify-content-center mb-3">
                <div className="rounded-circle bg-success bg-opacity-10 p-3 me-3">
                  <i className="fas fa-wrench fa-2x text-success"></i>
                </div>
                <div className="text-start">
                  <h2 className="mb-0 fw-bold text-success">{dashboardData.metricas.total_manutencoes}</h2>
                  <small className="text-muted">Manutenções</small>
                </div>
              </div>
              <div className="progress" style={{height: '6px'}}>
                <div className="progress-bar bg-success" role="progressbar" style={{width: '75%'}}></div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3 mb-3">
          <div className="card h-100 border-0 shadow-sm">
            <div className="card-body text-center p-4">
              <div className="d-flex align-items-center justify-content-center mb-3">
                <div className="rounded-circle bg-warning bg-opacity-10 p-3 me-3">
                  <i className="fas fa-dollar-sign fa-2x text-warning"></i>
                </div>
                <div className="text-start">
                  <h2 className="mb-0 fw-bold text-warning">{formatCurrency(dashboardData.metricas.total_gasto)}</h2>
                  <small className="text-muted">Total Gasto</small>
                </div>
              </div>
              <div className="progress" style={{height: '6px'}}>
                <div className="progress-bar bg-warning" role="progressbar" style={{width: '60%'}}></div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3 mb-3">
          <div className="card h-100 border-0 shadow-sm">
            <div className="card-body text-center p-4">
              <div className="d-flex align-items-center justify-content-center mb-3">
                <div className="rounded-circle bg-info bg-opacity-10 p-3 me-3">
                  <i className="fas fa-tachometer-alt fa-2x text-info"></i>
                </div>
                <div className="text-start">
                  <h2 className="mb-0 fw-bold text-info">{formatCurrency(dashboardData.metricas.media_km)}</h2>
                  <small className="text-muted">Custo/km</small>
                </div>
              </div>
              <div className="progress" style={{height: '6px'}}>
                <div className="progress-bar bg-info" role="progressbar" style={{width: '45%'}}></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Moto Principal ou Mensagem sem motos */}
      {dashboardData.moto_principal ? (
        <div className="row mb-4">
          <div className="col-12">
            <div className="card border-0 shadow-sm">
              <div className="card-header bg-gradient-primary text-white">
                <div className="d-flex align-items-center">
                  <i className="fas fa-star me-2"></i>
                  <h5 className="mb-0">Moto Principal</h5>
                  <span className="badge bg-light text-primary ms-2">Favorita</span>
                </div>
              </div>
              <div className="card-body p-4">
                <div className="row align-items-center">
                  <div className="col-md-8">
                    <h4 className="mb-3">
                      <i className="fas fa-motorcycle text-primary me-2"></i>
                      {dashboardData.moto_principal.marca} {dashboardData.moto_principal.modelo}
                    </h4>
                    <div className="row g-3">
                      <div className="col-md-3">
                        <div className="p-3 bg-light rounded">
                          <small className="text-muted d-block">Ano</small>
                          <strong className="h5 text-primary">{dashboardData.moto_principal.ano}</strong>
                        </div>
                      </div>
                      <div className="col-md-3">
                        <div className="p-3 bg-light rounded">
                          <small className="text-muted d-block">KM Atual</small>
                          <strong className="h5 text-success">
                            {dashboardData.moto_principal.km_atual?.toLocaleString('pt-BR')}
                          </strong>
                        </div>
                      </div>
                      <div className="col-md-3">
                        <div className="p-3 bg-light rounded">
                          <small className="text-muted d-block">KM Percorridos</small>
                          <strong className="h5 text-info">
                            {dashboardData.moto_principal.km_total_percorridos?.toLocaleString('pt-BR')}
                          </strong>
                        </div>
                      </div>
                      <div className="col-md-3">
                        <div className="p-3 bg-light rounded">
                          <small className="text-muted d-block">Idade</small>
                          <strong className="h5 text-warning">
                            {dashboardData.moto_principal.idade_anos} anos
                          </strong>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="col-md-4 text-center">
                    <div className="d-grid gap-2">
                      <Link to={`/motos/${dashboardData.moto_principal.id}`} className="btn btn-outline-primary">
                        <i className="fas fa-eye me-2"></i>Ver Detalhes
                      </Link>
                      <Link to={`/motos/editar/${dashboardData.moto_principal.id}`} className="btn btn-outline-secondary">
                        <i className="fas fa-edit me-2"></i>Editar
                      </Link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="row mb-4">
          <div className="col-12">
            <div className="card border-0 shadow-sm bg-gradient-primary text-white">
              <div className="card-body text-center py-5">
                <div className="mb-4">
                  <i className="fas fa-motorcycle fa-5x opacity-50"></i>
                </div>
                <h3 className="mb-3">Nenhuma moto cadastrada</h3>
                <p className="mb-4 opacity-75">
                  Comece cadastrando sua primeira motocicleta para acompanhar suas manutenções.
                </p>
                <Link to="/motos/novo" className="btn btn-light btn-lg shadow">
                  <i className="fas fa-plus me-2"></i>Cadastrar Primeira Moto
                </Link>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Ações Rápidas */}
      <div className="row">
        <div className="col-12">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-light">
              <div className="d-flex align-items-center">
                <i className="fas fa-rocket text-primary me-2"></i>
                <h5 className="mb-0">Ações Rápidas</h5>
              </div>
            </div>
            <div className="card-body">
              <div className="row g-3">
                <div className="col-md-3 col-sm-6">
                  <Link to="/motos" className="text-decoration-none">
                    <div className="card h-100 border-0 shadow-sm hover-lift">
                      <div className="card-body text-center p-4">
                        <div className="mb-3">
                          <div className="bg-primary bg-opacity-10 rounded-circle d-inline-flex align-items-center justify-content-center" style={{width: '60px', height: '60px'}}>
                            <i className="fas fa-list fa-2x text-primary"></i>
                          </div>
                        </div>
                        <h6 className="card-title mb-2">Ver Motos</h6>
                        <small className="text-muted">Gerenciar frota</small>
                      </div>
                    </div>
                  </Link>
                </div>

                <div className="col-md-3 col-sm-6">
                  <div className="card h-100 border-0 shadow-sm hover-lift">
                    <div className="card-body text-center p-4">
                      <div className="mb-3">
                        <div className="bg-success bg-opacity-10 rounded-circle d-inline-flex align-items-center justify-content-center" style={{width: '60px', height: '60px'}}>
                          <i className="fas fa-wrench fa-2x text-success"></i>
                        </div>
                      </div>
                      <h6 className="card-title mb-2">Manutenção</h6>
                      <small className="text-muted">Em breve</small>
                    </div>
                  </div>
                </div>

                <div className="col-md-3 col-sm-6">
                  <div className="card h-100 border-0 shadow-sm hover-lift">
                    <div className="card-body text-center p-4">
                      <div className="mb-3">
                        <div className="bg-info bg-opacity-10 rounded-circle d-inline-flex align-items-center justify-content-center" style={{width: '60px', height: '60px'}}>
                          <i className="fas fa-brain fa-2x text-info"></i>
                        </div>
                      </div>
                      <h6 className="card-title mb-2">Análise</h6>
                      <small className="text-muted">Em breve</small>
                    </div>
                  </div>
                </div>

                <div className="col-md-3 col-sm-6">
                  <Link to="/relatorios" className="text-decoration-none">
                    <div className="card h-100 border-0 shadow-sm hover-lift">
                      <div className="card-body text-center p-4">
                        <div className="mb-3">
                          <div className="bg-warning bg-opacity-10 rounded-circle d-inline-flex align-items-center justify-content-center" style={{width: '60px', height: '60px'}}>
                            <i className="fas fa-chart-bar fa-2x text-warning"></i>
                          </div>
                        </div>
                        <h6 className="card-title mb-2">Relatórios</h6>
                        <small className="text-muted">Análises detalhadas</small>
                      </div>
                    </div>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
