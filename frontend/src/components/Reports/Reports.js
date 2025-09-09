import React, { useState, useEffect } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Title, Tooltip, Legend } from 'chart.js';
import { Line, Doughnut } from 'react-chartjs-2';
import './Reports.css';

// Registrar componentes do Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const Reports = () => {
  const [loading, setLoading] = useState(true);
  const [filtersCollapsed, setFiltersCollapsed] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPeriod, setSelectedPeriod] = useState('mensal');
  
  const [filters, setFilters] = useState({
    data_inicio: '',
    data_fim: '',
    moto: '',
    tipo_relatorio: 'geral'
  });

  const [metrics, setMetrics] = useState({
    totalManutencoes: 0,
    totalGasto: 0,
    mediaMensal: 0,
    kmPercorridos: 0
  });

  const [chartData] = useState({
    gastosPorTipo: {
      labels: ['Óleo e Filtros', 'Bateria', 'Peças', 'Mão de Obra', 'Combustível', 'Outros'],
      datasets: [{
        data: [450, 320, 280, 200, 150, 100],
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
        ],
        borderWidth: 2,
        borderColor: '#fff'
      }]
    },
    gastosPorMes: {
      labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
      datasets: [{
        label: 'Gastos (R$)',
        data: [1200, 800, 1500, 900, 1100, 1300, 1000, 1400, 1200, 1600, 1100, 1300],
        borderColor: '#36A2EB',
        backgroundColor: 'rgba(54, 162, 235, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#36A2EB',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 6,
        pointHoverRadius: 8
      }]
    }
  });

  const [topGastos] = useState([
    { icon: 'fas fa-oil-can', label: 'Óleo e Filtros', valor: 450, color: 'primary' },
    { icon: 'fas fa-bolt', label: 'Bateria', valor: 320, color: 'warning' },
    { icon: 'fas fa-cog', label: 'Peças', valor: 280, color: 'success' },
    { icon: 'fas fa-tools', label: 'Mão de Obra', valor: 200, color: 'info' },
    { icon: 'fas fa-gas-pump', label: 'Combustível', valor: 150, color: 'danger' }
  ]);

  const [manutencoes] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      // Por enquanto, usando dados mockados
      // const response = await dashboardService.getDashboardData();
      
      setMetrics({
        totalManutencoes: 12,
        totalGasto: 2500.00,
        mediaMensal: 208.33,
        kmPercorridos: 15000
      });

      setLoading(false);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      setLoading(false);
    }
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatNumber = (value) => {
    return new Intl.NumberFormat('pt-BR').format(value);
  };

  const handleFilterSubmit = (e) => {
    e.preventDefault();
    aplicarFiltros();
  };

  const aplicarFiltros = () => {
    console.log('Aplicando filtros:', filters);
    // Aqui seria implementada a lógica de filtros
  };

  const limparFiltros = () => {
    setFilters({
      data_inicio: '',
      data_fim: '',
      moto: '',
      tipo_relatorio: 'geral'
    });
  };

  const alterarPeriodo = (periodo) => {
    setSelectedPeriod(periodo);
    // Implementar mudança de período no gráfico
  };

  const exportarPDF = () => {
    alert('Funcionalidade de exportação PDF será implementada em breve.');
  };

  const handlePrint = () => {
    window.print();
  };

  const chartOptions = {
    doughnut: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            padding: 20,
            usePointStyle: true
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const total = context.dataset.data.reduce((a, b) => a + b, 0);
              const percentage = ((context.parsed / total) * 100).toFixed(1);
              return context.label + ': ' + formatCurrency(context.parsed) + ' (' + percentage + '%)';
            }
          }
        }
      }
    },
    line: {
      responsive: true,
      interaction: {
        intersect: false,
        mode: 'index'
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function(context) {
              return formatCurrency(context.parsed.y);
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function(value) {
              return formatCurrency(value);
            }
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          }
        },
        x: {
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          }
        }
      }
    }
  };

  if (loading) {
    return (
      <div className="container-fluid py-4">
        <div className="d-flex justify-content-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Carregando...</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container-fluid py-4">
      {/* Header da Página */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <h1 className="mb-1">
                <i className="fas fa-chart-bar text-primary me-2"></i>Relatórios
              </h1>
              <p className="text-muted mb-0">Análises detalhadas e relatórios da sua frota</p>
            </div>
            <div>
              <button className="btn btn-outline-primary me-2" onClick={handlePrint}>
                <i className="fas fa-print me-2"></i>Imprimir
              </button>
              <button className="btn btn-outline-success" onClick={exportarPDF}>
                <i className="fas fa-file-pdf me-2"></i>Exportar PDF
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Filtros Avançados */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-light">
              <div className="d-flex align-items-center">
                <i className="fas fa-filter text-primary me-2"></i>
                <h5 className="mb-0">Filtros Avançados</h5>
                <button 
                  className="btn btn-sm btn-outline-secondary ms-auto"
                  onClick={() => setFiltersCollapsed(!filtersCollapsed)}
                >
                  <i className={`fas fa-chevron-${filtersCollapsed ? 'down' : 'up'}`}></i>
                </button>
              </div>
            </div>
            <div className={`collapse ${!filtersCollapsed ? 'show' : ''}`}>
              <div className="card-body">
                <form className="row g-3" onSubmit={handleFilterSubmit}>
                  <div className="col-md-3">
                    <div className="form-floating">
                      <input 
                        type="date" 
                        className="form-control" 
                        id="data_inicio"
                        value={filters.data_inicio}
                        onChange={(e) => setFilters(prev => ({ ...prev, data_inicio: e.target.value }))}
                      />
                      <label htmlFor="data_inicio">
                        <i className="fas fa-calendar-alt me-1"></i>Data Inicial
                      </label>
                    </div>
                  </div>
                  <div className="col-md-3">
                    <div className="form-floating">
                      <input 
                        type="date" 
                        className="form-control" 
                        id="data_fim"
                        value={filters.data_fim}
                        onChange={(e) => setFilters(prev => ({ ...prev, data_fim: e.target.value }))}
                      />
                      <label htmlFor="data_fim">
                        <i className="fas fa-calendar-alt me-1"></i>Data Final
                      </label>
                    </div>
                  </div>
                  <div className="col-md-3">
                    <div className="form-floating">
                      <select 
                        className="form-select" 
                        id="moto"
                        value={filters.moto}
                        onChange={(e) => setFilters(prev => ({ ...prev, moto: e.target.value }))}
                      >
                        <option value="">Todas as motos</option>
                        <option value="1">Dafra Cruisym 300</option>
                      </select>
                      <label htmlFor="moto">
                        <i className="fas fa-motorcycle me-1"></i>Moto Específica
                      </label>
                    </div>
                  </div>
                  <div className="col-md-3">
                    <div className="form-floating">
                      <select 
                        className="form-select" 
                        id="tipo_relatorio"
                        value={filters.tipo_relatorio}
                        onChange={(e) => setFilters(prev => ({ ...prev, tipo_relatorio: e.target.value }))}
                      >
                        <option value="geral">Relatório Geral</option>
                        <option value="manutencoes">Manutenções</option>
                        <option value="custos">Custos</option>
                        <option value="performance">Performance</option>
                      </select>
                      <label htmlFor="tipo_relatorio">
                        <i className="fas fa-chart-line me-1"></i>Tipo de Relatório
                      </label>
                    </div>
                  </div>
                  <div className="col-12">
                    <div className="d-flex gap-2">
                      <button type="submit" className="btn btn-primary">
                        <i className="fas fa-search me-2"></i>Aplicar Filtros
                      </button>
                      <button type="button" className="btn btn-outline-secondary" onClick={limparFiltros}>
                        <i className="fas fa-eraser me-2"></i>Limpar
                      </button>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Cards de Métricas */}
      <div className="row mb-4">
        <div className="col-md-3 mb-3">
          <div className="card h-100 border-0 shadow-sm metric-card">
            <div className="card-body text-center p-4">
              <div className="metric-icon mb-3">
                <i className="fas fa-wrench fa-3x text-primary"></i>
              </div>
              <h2 className="metric-value mb-2">{formatNumber(metrics.totalManutencoes)}</h2>
              <p className="metric-label mb-0">Total de Manutenções</p>
              <small className="text-muted">Período selecionado</small>
            </div>
          </div>
        </div>

        <div className="col-md-3 mb-3">
          <div className="card h-100 border-0 shadow-sm metric-card">
            <div className="card-body text-center p-4">
              <div className="metric-icon mb-3">
                <i className="fas fa-dollar-sign fa-3x text-success"></i>
              </div>
              <h2 className="metric-value mb-2">{formatCurrency(metrics.totalGasto)}</h2>
              <p className="metric-label mb-0">Valor Total Gasto</p>
              <small className="text-muted">Em manutenções</small>
            </div>
          </div>
        </div>

        <div className="col-md-3 mb-3">
          <div className="card h-100 border-0 shadow-sm metric-card">
            <div className="card-body text-center p-4">
              <div className="metric-icon mb-3">
                <i className="fas fa-chart-line fa-3x text-warning"></i>
              </div>
              <h2 className="metric-value mb-2">{formatCurrency(metrics.mediaMensal)}</h2>
              <p className="metric-label mb-0">Média Mensal</p>
              <small className="text-muted">Gastos por mês</small>
            </div>
          </div>
        </div>

        <div className="col-md-3 mb-3">
          <div className="card h-100 border-0 shadow-sm metric-card">
            <div className="card-body text-center p-4">
              <div className="metric-icon mb-3">
                <i className="fas fa-tachometer-alt fa-3x text-info"></i>
              </div>
              <h2 className="metric-value mb-2">{formatNumber(metrics.kmPercorridos)} km</h2>
              <p className="metric-label mb-0">Km Percorridos</p>
              <small className="text-muted">No período</small>
            </div>
          </div>
        </div>
      </div>

      {/* Gráficos Interativos */}
      <div className="row mb-4">
        <div className="col-lg-8 mb-4">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-light">
              <div className="d-flex align-items-center justify-content-between">
                <h5 className="mb-0">
                  <i className="fas fa-chart-pie text-primary me-2"></i>Gastos por Tipo
                </h5>
                <div className="dropdown">
                  <button className="btn btn-sm btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                    <i className="fas fa-cog me-1"></i>Opções
                  </button>
                  <ul className="dropdown-menu">
                    <li><button className="dropdown-item" onClick={() => console.log('Exportar PNG')}>
                      <i className="fas fa-download me-1"></i>Exportar PNG
                    </button></li>
                    <li><button className="dropdown-item" onClick={() => console.log('Expandir')}>
                      <i className="fas fa-expand me-1"></i>Expandir
                    </button></li>
                  </ul>
                </div>
              </div>
            </div>
            <div className="card-body">
              <Doughnut data={chartData.gastosPorTipo} options={chartOptions.doughnut} />
            </div>
          </div>
        </div>

        <div className="col-lg-4 mb-4">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-light">
              <h5 className="mb-0">
                <i className="fas fa-trophy text-warning me-2"></i>Top 5 Gastos
              </h5>
            </div>
            <div className="card-body">
              <div className="list-group list-group-flush">
                {topGastos.map((item, index) => (
                  <div key={index} className="list-group-item d-flex justify-content-between align-items-center px-0">
                    <div>
                      <i className={`${item.icon} text-${item.color} me-2`}></i>
                      <span>{item.label}</span>
                    </div>
                    <span className={`badge bg-${item.color} rounded-pill`}>
                      {formatCurrency(item.valor)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Gráfico de Tendência */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-light">
              <div className="d-flex align-items-center justify-content-between">
                <h5 className="mb-0">
                  <i className="fas fa-chart-line text-success me-2"></i>Tendência de Gastos
                </h5>
                <div className="btn-group" role="group">
                  {['mensal', 'trimestral', 'anual'].map(periodo => (
                    <button 
                      key={periodo}
                      type="button" 
                      className={`btn btn-sm btn-outline-secondary ${selectedPeriod === periodo ? 'active' : ''}`}
                      onClick={() => alterarPeriodo(periodo)}
                    >
                      <i className={`fas fa-calendar${periodo === 'mensal' ? '-week' : periodo === 'trimestral' ? '-alt' : ''} me-1`}></i>
                      {periodo.charAt(0).toUpperCase() + periodo.slice(1)}
                    </button>
                  ))}
                </div>
              </div>
            </div>
            <div className="card-body">
              <Line data={chartData.gastosPorMes} options={chartOptions.line} />
            </div>
          </div>
        </div>
      </div>

      {/* Tabela Detalhada */}
      <div className="row">
        <div className="col-12">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-light">
              <div className="d-flex align-items-center justify-content-between">
                <h5 className="mb-0">
                  <i className="fas fa-table text-info me-2"></i>Detalhes das Manutenções
                </h5>
                <div className="input-group" style={{ width: '300px' }}>
                  <span className="input-group-text">
                    <i className="fas fa-search"></i>
                  </span>
                  <input 
                    type="text" 
                    className="form-control" 
                    placeholder="Buscar..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
              </div>
            </div>
            <div className="card-body p-0">
              <div className="table-responsive">
                <table className="table table-hover mb-0">
                  <thead className="table-light">
                    <tr>
                      <th>
                        <i className="fas fa-calendar me-1"></i>Data
                      </th>
                      <th>
                        <i className="fas fa-motorcycle me-1"></i>Moto
                      </th>
                      <th>
                        <i className="fas fa-wrench me-1"></i>Tipo
                      </th>
                      <th>
                        <i className="fas fa-sticky-note me-1"></i>Descrição
                      </th>
                      <th>
                        <i className="fas fa-dollar-sign me-1"></i>Valor
                      </th>
                      <th>
                        <i className="fas fa-info-circle me-1"></i>Status
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {manutencoes.length === 0 ? (
                      <tr>
                        <td colSpan="6" className="text-center py-5">
                          <div className="empty-state">
                            <i className="fas fa-info-circle fa-3x text-muted mb-3"></i>
                            <h5 className="text-muted">Nenhum dado encontrado</h5>
                            <p className="text-muted">Selecione um período para visualizar os dados</p>
                          </div>
                        </td>
                      </tr>
                    ) : (
                      manutencoes.map((manutencao, index) => (
                        <tr key={index}>
                          <td>{manutencao.data}</td>
                          <td>{manutencao.moto}</td>
                          <td>{manutencao.tipo}</td>
                          <td>{manutencao.descricao}</td>
                          <td>{formatCurrency(manutencao.valor)}</td>
                          <td>
                            <span className={`badge bg-${manutencao.status === 'Concluída' ? 'success' : 'warning'}`}>
                              {manutencao.status}
                            </span>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
            <div className="card-footer bg-light">
              <div className="d-flex justify-content-between align-items-center">
                <small className="text-muted">
                  Mostrando {manutencoes.length} de {manutencoes.length} registros
                </small>
                <nav>
                  <ul className="pagination pagination-sm mb-0">
                    <li className="page-item disabled">
                      <button className="page-link">
                        <i className="fas fa-chevron-left"></i>
                      </button>
                    </li>
                    <li className="page-item active">
                      <button className="page-link">1</button>
                    </li>
                    <li className="page-item disabled">
                      <button className="page-link">
                        <i className="fas fa-chevron-right"></i>
                      </button>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Reports;
