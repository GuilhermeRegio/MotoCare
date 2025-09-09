import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import './Settings.css';

const Settings = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({
    totalMotos: 0,
    totalManutencoes: 0,
    totalGasto: 0
  });

  const [userProfile, setUserProfile] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    email: user?.email || '',
    telefone: ''
  });

  const [passwordForm, setPasswordForm] = useState({
    senha_atual: '',
    nova_senha: '',
    confirmar_senha: ''
  });

  const [preferences, setPreferences] = useState({
    tema: 'light',
    idioma: 'pt-br',
    moeda: 'BRL',
    formato_data: 'dd/mm/yyyy',
    notificacoes_email: true,
    notificacoes_manutencao: true,
    notificacoes_browser: false,
    notificacoes_relatorios: false
  });

  const [twoFactorEnabled, setTwoFactorEnabled] = useState(false);

  useEffect(() => {
    loadSavedSettings();
    loadStats();
  }, []);

  const loadSavedSettings = () => {
    const savedConfig = localStorage.getItem('motoCare_config');
    if (savedConfig) {
      try {
        const config = JSON.parse(savedConfig);
        setPreferences(prev => ({ ...prev, ...config }));
      } catch (error) {
        console.error('Erro ao carregar configurações:', error);
      }
    }
  };

  const loadStats = async () => {
    try {
      // Aqui seria feita a chamada para a API de estatísticas
      // Por enquanto, dados mockados
      setStats({
        totalMotos: 5,
        totalManutencoes: 12,
        totalGasto: 2500.00
      });
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error);
    }
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Aqui seria feita a chamada para a API de atualização do perfil
      setTimeout(() => {
        showNotification('Perfil atualizado com sucesso!', 'success');
        setLoading(false);
      }, 1500);
    } catch (error) {
      showNotification('Erro ao atualizar perfil', 'danger');
      setLoading(false);
    }
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    
    if (passwordForm.nova_senha !== passwordForm.confirmar_senha) {
      showNotification('As senhas não coincidem', 'danger');
      return;
    }

    setLoading(true);

    try {
      // Aqui seria feita a chamada para a API de alteração de senha
      setTimeout(() => {
        showNotification('Senha alterada com sucesso!', 'success');
        setPasswordForm({
          senha_atual: '',
          nova_senha: '',
          confirmar_senha: ''
        });
        setLoading(false);
      }, 1500);
    } catch (error) {
      showNotification('Erro ao alterar senha', 'danger');
      setLoading(false);
    }
  };

  const handlePreferencesSubmit = (e) => {
    e.preventDefault();
    saveSettings();
    showNotification('Preferências salvas com sucesso!', 'success');
  };

  const saveSettings = () => {
    localStorage.setItem('motoCare_config', JSON.stringify(preferences));
    applyTheme(preferences.tema);
  };

  const saveAllSettings = () => {
    saveSettings();
    showNotification('Todas as configurações foram salvas!', 'success');
  };

  const restoreDefaults = () => {
    if (window.confirm('Tem certeza que deseja restaurar todas as configurações para os valores padrão?')) {
      localStorage.removeItem('motoCare_config');
      setPreferences({
        tema: 'light',
        idioma: 'pt-br',
        moeda: 'BRL',
        formato_data: 'dd/mm/yyyy',
        notificacoes_email: true,
        notificacoes_manutencao: true,
        notificacoes_browser: false,
        notificacoes_relatorios: false
      });
      applyTheme('light');
      showNotification('Configurações restauradas para os valores padrão!', 'success');
    }
  };

  const applyTheme = (theme) => {
    const body = document.body;
    body.classList.remove('tema-light', 'tema-dark', 'tema-auto');
    body.classList.add(`tema-${theme}`);
  };

  const handleThemeChange = (theme) => {
    setPreferences(prev => ({ ...prev, tema: theme }));
    applyTheme(theme);
  };

  const showNotification = (message, type = 'info') => {
    // Sistema de notificação seria implementado aqui
    console.log(`${type.toUpperCase()}: ${message}`);
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  return (
    <div className="container-fluid py-4">
      {/* Header da Página */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <h1 className="mb-1">
                <i className="fas fa-cog text-primary me-2"></i>Configurações
              </h1>
              <p className="text-muted mb-0">Gerencie suas preferências e configurações do sistema</p>
            </div>
            <div>
              <button 
                className="btn btn-outline-success me-2"
                onClick={saveAllSettings}
              >
                <i className="fas fa-save me-2"></i>Salvar Tudo
              </button>
              <button 
                className="btn btn-outline-secondary"
                onClick={restoreDefaults}
              >
                <i className="fas fa-undo me-2"></i>Restaurar Padrões
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="row">
        {/* Configurações Principais */}
        <div className="col-lg-8 mb-4">
          {/* Perfil do Usuário */}
          <div className="card border-0 shadow-sm mb-4">
            <div className="card-header bg-light">
              <div className="d-flex align-items-center">
                <div className="avatar-circle me-3">
                  <i className="fas fa-user fa-2x text-primary"></i>
                </div>
                <div>
                  <h5 className="mb-0">Perfil do Usuário</h5>
                  <small className="text-muted">Atualize suas informações pessoais</small>
                </div>
              </div>
            </div>
            <div className="card-body">
              <form onSubmit={handleProfileSubmit}>
                <div className="row">
                  <div className="col-md-6 mb-3">
                    <div className="form-floating">
                      <input
                        type="text"
                        className="form-control"
                        id="first_name"
                        placeholder="Nome"
                        value={userProfile.first_name}
                        onChange={(e) => setUserProfile(prev => ({ ...prev, first_name: e.target.value }))}
                        required
                      />
                      <label htmlFor="first_name">
                        <i className="fas fa-user me-1"></i>Nome
                      </label>
                    </div>
                  </div>
                  <div className="col-md-6 mb-3">
                    <div className="form-floating">
                      <input
                        type="text"
                        className="form-control"
                        id="last_name"
                        placeholder="Sobrenome"
                        value={userProfile.last_name}
                        onChange={(e) => setUserProfile(prev => ({ ...prev, last_name: e.target.value }))}
                        required
                      />
                      <label htmlFor="last_name">
                        <i className="fas fa-user-tag me-1"></i>Sobrenome
                      </label>
                    </div>
                  </div>
                </div>

                <div className="mb-3">
                  <div className="form-floating">
                    <input
                      type="email"
                      className="form-control"
                      id="email"
                      placeholder="E-mail"
                      value={userProfile.email}
                      onChange={(e) => setUserProfile(prev => ({ ...prev, email: e.target.value }))}
                      required
                    />
                    <label htmlFor="email">
                      <i className="fas fa-envelope me-1"></i>E-mail
                    </label>
                  </div>
                </div>

                <div className="mb-3">
                  <div className="form-floating">
                    <input
                      type="tel"
                      className="form-control"
                      id="telefone"
                      placeholder="Telefone"
                      value={userProfile.telefone}
                      onChange={(e) => setUserProfile(prev => ({ ...prev, telefone: e.target.value }))}
                    />
                    <label htmlFor="telefone">
                      <i className="fas fa-phone me-1"></i>Telefone (Opcional)
                    </label>
                  </div>
                </div>

                <div className="d-flex gap-2">
                  <button type="submit" className="btn btn-primary" disabled={loading}>
                    {loading ? (
                      <><i className="fas fa-spinner fa-spin me-2"></i>Salvando...</>
                    ) : (
                      <><i className="fas fa-save me-2"></i>Salvar Perfil</>
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>

          {/* Segurança */}
          <div className="card border-0 shadow-sm mb-4">
            <div className="card-header bg-light">
              <div className="d-flex align-items-center">
                <div className="avatar-circle me-3">
                  <i className="fas fa-shield-alt fa-2x text-success"></i>
                </div>
                <div>
                  <h5 className="mb-0">Segurança</h5>
                  <small className="text-muted">Gerencie sua senha e configurações de segurança</small>
                </div>
              </div>
            </div>
            <div className="card-body">
              {/* Alterar Senha */}
              <div className="mb-4">
                <h6 className="mb-3">
                  <i className="fas fa-key me-2"></i>Alterar Senha
                </h6>
                <form onSubmit={handlePasswordSubmit}>
                  <div className="row">
                    <div className="col-md-4 mb-3">
                      <div className="form-floating">
                        <input
                          type="password"
                          className="form-control"
                          id="senha_atual"
                          placeholder="Senha atual"
                          value={passwordForm.senha_atual}
                          onChange={(e) => setPasswordForm(prev => ({ ...prev, senha_atual: e.target.value }))}
                          required
                        />
                        <label htmlFor="senha_atual">Senha Atual</label>
                      </div>
                    </div>
                    <div className="col-md-4 mb-3">
                      <div className="form-floating">
                        <input
                          type="password"
                          className="form-control"
                          id="nova_senha"
                          placeholder="Nova senha"
                          minLength="8"
                          value={passwordForm.nova_senha}
                          onChange={(e) => setPasswordForm(prev => ({ ...prev, nova_senha: e.target.value }))}
                          required
                        />
                        <label htmlFor="nova_senha">Nova Senha</label>
                      </div>
                    </div>
                    <div className="col-md-4 mb-3">
                      <div className="form-floating">
                        <input
                          type="password"
                          className="form-control"
                          id="confirmar_senha"
                          placeholder="Confirmar senha"
                          value={passwordForm.confirmar_senha}
                          onChange={(e) => setPasswordForm(prev => ({ ...prev, confirmar_senha: e.target.value }))}
                          required
                        />
                        <label htmlFor="confirmar_senha">Confirmar Senha</label>
                      </div>
                    </div>
                  </div>
                  <button type="submit" className="btn btn-warning" disabled={loading}>
                    {loading ? (
                      <><i className="fas fa-spinner fa-spin me-2"></i>Alterando...</>
                    ) : (
                      <><i className="fas fa-key me-2"></i>Alterar Senha</>
                    )}
                  </button>
                </form>
              </div>

              {/* Autenticação de Dois Fatores */}
              <div className="border-top pt-4">
                <div className="d-flex justify-content-between align-items-center">
                  <div>
                    <h6 className="mb-1">
                      <i className="fas fa-mobile-alt me-2"></i>Autenticação de Dois Fatores
                    </h6>
                    <small className="text-muted">Adicione uma camada extra de segurança</small>
                  </div>
                  <div className="form-check form-switch">
                    <input
                      className="form-check-input"
                      type="checkbox"
                      id="2fa-toggle"
                      checked={twoFactorEnabled}
                      onChange={(e) => setTwoFactorEnabled(e.target.checked)}
                    />
                    <label className="form-check-label" htmlFor="2fa-toggle">
                      <span className={`badge ${twoFactorEnabled ? 'bg-success' : 'bg-danger'}`}>
                        {twoFactorEnabled ? 'Ativado' : 'Desativado'}
                      </span>
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Preferências do Sistema */}
          <div className="card border-0 shadow-sm mb-4">
            <div className="card-header bg-light">
              <div className="d-flex align-items-center">
                <div className="avatar-circle me-3">
                  <i className="fas fa-palette fa-2x text-info"></i>
                </div>
                <div>
                  <h5 className="mb-0">Preferências do Sistema</h5>
                  <small className="text-muted">Personalize sua experiência</small>
                </div>
              </div>
            </div>
            <div className="card-body">
              <form onSubmit={handlePreferencesSubmit}>
                <div className="row">
                  <div className="col-md-6 mb-3">
                    <div className="form-floating">
                      <select
                        className="form-select"
                        id="tema"
                        value={preferences.tema}
                        onChange={(e) => handleThemeChange(e.target.value)}
                      >
                        <option value="light">🌞 Claro</option>
                        <option value="dark">🌙 Escuro</option>
                        <option value="auto">🔄 Automático</option>
                      </select>
                      <label htmlFor="tema">
                        <i className="fas fa-palette me-1"></i>Tema
                      </label>
                    </div>
                  </div>
                  <div className="col-md-6 mb-3">
                    <div className="form-floating">
                      <select
                        className="form-select"
                        id="idioma"
                        value={preferences.idioma}
                        onChange={(e) => setPreferences(prev => ({ ...prev, idioma: e.target.value }))}
                      >
                        <option value="pt-br">🇧🇷 Português (Brasil)</option>
                        <option value="en">🇺🇸 English</option>
                        <option value="es">🇪🇸 Español</option>
                      </select>
                      <label htmlFor="idioma">
                        <i className="fas fa-language me-1"></i>Idioma
                      </label>
                    </div>
                  </div>
                </div>

                <div className="row">
                  <div className="col-md-6 mb-3">
                    <div className="form-floating">
                      <select
                        className="form-select"
                        id="moeda"
                        value={preferences.moeda}
                        onChange={(e) => setPreferences(prev => ({ ...prev, moeda: e.target.value }))}
                      >
                        <option value="BRL">🇧🇷 Real (R$)</option>
                        <option value="USD">🇺🇸 Dólar ($)</option>
                        <option value="EUR">🇪🇺 Euro (€)</option>
                      </select>
                      <label htmlFor="moeda">
                        <i className="fas fa-money-bill me-1"></i>Moeda
                      </label>
                    </div>
                  </div>
                  <div className="col-md-6 mb-3">
                    <div className="form-floating">
                      <select
                        className="form-select"
                        id="formato_data"
                        value={preferences.formato_data}
                        onChange={(e) => setPreferences(prev => ({ ...prev, formato_data: e.target.value }))}
                      >
                        <option value="dd/mm/yyyy">DD/MM/YYYY</option>
                        <option value="mm/dd/yyyy">MM/DD/YYYY</option>
                        <option value="yyyy-mm-dd">YYYY-MM-DD</option>
                      </select>
                      <label htmlFor="formato_data">
                        <i className="fas fa-calendar me-1"></i>Formato de Data
                      </label>
                    </div>
                  </div>
                </div>

                {/* Notificações */}
                <div className="border-top pt-3">
                  <h6 className="mb-3">
                    <i className="fas fa-bell me-2"></i>Notificações
                  </h6>
                  <div className="row">
                    <div className="col-md-6">
                      <div className="form-check mb-2">
                        <input
                          className="form-check-input"
                          type="checkbox"
                          id="notificacoes_email"
                          checked={preferences.notificacoes_email}
                          onChange={(e) => setPreferences(prev => ({ ...prev, notificacoes_email: e.target.checked }))}
                        />
                        <label className="form-check-label" htmlFor="notificacoes_email">
                          <i className="fas fa-envelope me-1"></i>E-mail
                        </label>
                      </div>
                      <div className="form-check mb-2">
                        <input
                          className="form-check-input"
                          type="checkbox"
                          id="notificacoes_manutencao"
                          checked={preferences.notificacoes_manutencao}
                          onChange={(e) => setPreferences(prev => ({ ...prev, notificacoes_manutencao: e.target.checked }))}
                        />
                        <label className="form-check-label" htmlFor="notificacoes_manutencao">
                          <i className="fas fa-wrench me-1"></i>Lembretes de Manutenção
                        </label>
                      </div>
                    </div>
                    <div className="col-md-6">
                      <div className="form-check mb-2">
                        <input
                          className="form-check-input"
                          type="checkbox"
                          id="notificacoes_browser"
                          checked={preferences.notificacoes_browser}
                          onChange={(e) => setPreferences(prev => ({ ...prev, notificacoes_browser: e.target.checked }))}
                        />
                        <label className="form-check-label" htmlFor="notificacoes_browser">
                          <i className="fas fa-globe me-1"></i>Navegador
                        </label>
                      </div>
                      <div className="form-check mb-2">
                        <input
                          className="form-check-input"
                          type="checkbox"
                          id="notificacoes_relatorios"
                          checked={preferences.notificacoes_relatorios}
                          onChange={(e) => setPreferences(prev => ({ ...prev, notificacoes_relatorios: e.target.checked }))}
                        />
                        <label className="form-check-label" htmlFor="notificacoes_relatorios">
                          <i className="fas fa-chart-bar me-1"></i>Relatórios Semanais
                        </label>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="d-flex gap-2 mt-3">
                  <button type="submit" className="btn btn-success">
                    <i className="fas fa-save me-2"></i>Salvar Preferências
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>

        {/* Sidebar com Informações */}
        <div className="col-lg-4">
          {/* Informações da Conta */}
          <div className="card border-0 shadow-sm mb-4">
            <div className="card-header bg-light">
              <h5 className="mb-0">
                <i className="fas fa-user-circle text-primary me-2"></i>Minha Conta
              </h5>
            </div>
            <div className="card-body">
              <div className="text-center mb-3">
                <div className="avatar-large mb-3">
                  <i className="fas fa-user fa-3x text-primary"></i>
                </div>
                <h6 className="mb-1">
                  {user?.first_name && user?.last_name 
                    ? `${user.first_name} ${user.last_name}` 
                    : user?.username}
                </h6>
                <small className="text-muted">{user?.email}</small>
              </div>

              <hr />

              <div className="account-info">
                <div className="d-flex justify-content-between mb-2">
                  <span className="text-muted">Usuário:</span>
                  <span className="fw-semibold">{user?.username}</span>
                </div>
                <div className="d-flex justify-content-between mb-2">
                  <span className="text-muted">Membro desde:</span>
                  <span className="fw-semibold">01/01/2024</span>
                </div>
                <div className="d-flex justify-content-between mb-2">
                  <span className="text-muted">Último acesso:</span>
                  <span className="fw-semibold">Hoje</span>
                </div>
                <div className="d-flex justify-content-between mb-2">
                  <span className="text-muted">Status:</span>
                  <span className="badge bg-success">Ativo</span>
                </div>
              </div>
            </div>
          </div>

          {/* Estatísticas Rápidas */}
          <div className="card border-0 shadow-sm mb-4">
            <div className="card-header bg-light">
              <h5 className="mb-0">
                <i className="fas fa-chart-line text-success me-2"></i>Estatísticas
              </h5>
            </div>
            <div className="card-body">
              <div className="stat-item mb-3">
                <div className="d-flex align-items-center">
                  <div className="stat-icon me-3">
                    <i className="fas fa-motorcycle fa-2x text-primary"></i>
                  </div>
                  <div>
                    <div className="stat-value">{stats.totalMotos}</div>
                    <div className="stat-label">Total de Motos</div>
                  </div>
                </div>
              </div>

              <div className="stat-item mb-3">
                <div className="d-flex align-items-center">
                  <div className="stat-icon me-3">
                    <i className="fas fa-wrench fa-2x text-success"></i>
                  </div>
                  <div>
                    <div className="stat-value">{stats.totalManutencoes}</div>
                    <div className="stat-label">Manutenções</div>
                  </div>
                </div>
              </div>

              <div className="stat-item">
                <div className="d-flex align-items-center">
                  <div className="stat-icon me-3">
                    <i className="fas fa-dollar-sign fa-2x text-warning"></i>
                  </div>
                  <div>
                    <div className="stat-value">{formatCurrency(stats.totalGasto)}</div>
                    <div className="stat-label">Total Gasto</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Ações Rápidas */}
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-light">
              <h5 className="mb-0">
                <i className="fas fa-bolt text-warning me-2"></i>Ações Rápidas
              </h5>
            </div>
            <div className="card-body">
              <div className="d-grid gap-2">
                <button className="btn btn-outline-primary">
                  <i className="fas fa-download me-2"></i>Exportar Dados
                </button>
                <button className="btn btn-outline-danger">
                  <i className="fas fa-trash me-2"></i>Excluir Conta
                </button>
                <button className="btn btn-outline-info">
                  <i className="fas fa-headset me-2"></i>Suporte
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
