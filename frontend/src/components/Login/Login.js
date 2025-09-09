import React, { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import './Login.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, isAuthenticated } = useAuth();

  useEffect(() => {
    // Animação de entrada
    const card = document.querySelector('.card');
    if (card) {
      card.style.opacity = '0';
      card.style.transform = 'translateY(30px)';

      setTimeout(() => {
        card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
      }, 100);
    }

    // Foco automático no primeiro campo
    const usernameField = document.getElementById('id_username');
    if (usernameField) {
      usernameField.focus();
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!username || !password) {
      setError('Por favor, preencha todos os campos!');
      return;
    }
    
    setLoading(true);
    
    try {
      await login(username, password);
    } catch (error) {
      setError(error.message || 'Usuário ou senha incorretos.');
    } finally {
      setLoading(false);
    }
  };

  // Se já estiver autenticado, redirecionar para dashboard
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div className="login-page">
      <div className="row justify-content-center align-items-center min-vh-100 py-5">
        <div className="col-md-6 col-lg-4">
          <div className="card shadow-lg border-0">
            <div className="card-header text-center py-4" style={{background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', border: 'none'}}>
              <div className="mb-3">
                <i className="fas fa-motorcycle fa-3x text-white"></i>
              </div>
              <h3 className="text-white mb-0 fw-bold">MotoCare</h3>
              <p className="text-white-50 mb-0">Sistema de Manutenção Inteligente</p>
            </div>
            
            <div className="card-body p-4">
              {error && (
                <div className="alert alert-danger border-0 shadow-sm">
                  <i className="fas fa-exclamation-triangle me-2"></i>
                  <strong>Erro de Login!</strong>
                  <br />{error}
                </div>
              )}
              
              <form className="user" onSubmit={handleSubmit}>
                <div className="form-floating mb-3">
                  <input
                    type="text"
                    className="form-control"
                    id="id_username"
                    name="username"
                    placeholder="Nome de usuário"
                    required
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                    disabled={loading}
                  />
                  <label htmlFor="id_username">
                    <i className="fas fa-user me-2"></i>Usuário
                  </label>
                </div>
                
                <div className="form-floating mb-4">
                  <input
                    type="password"
                    className="form-control"
                    id="id_password"
                    name="password"
                    placeholder="Senha"
                    required
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    disabled={loading}
                  />
                  <label htmlFor="id_password">
                    <i className="fas fa-lock me-2"></i>Senha
                  </label>
                </div>
                
                <div className="d-grid">
                  <button type="submit" className="btn btn-primary btn-lg" disabled={loading}>
                    <i className="fas fa-sign-in-alt me-2"></i>
                    {loading ? 'Entrando...' : 'Entrar no Sistema'}
                  </button>
                </div>
              </form>
              
              <div className="text-center mt-4">
                <hr className="my-4" />
                <small className="text-muted">
                  <i className="fas fa-shield-alt me-1"></i>
                  Acesso seguro e protegido
                </small>
              </div>
            </div>
            
            <div className="card-footer text-center py-3 bg-light">
              <small className="text-muted">
                <i className="fas fa-copyright me-1"></i>
                2025 MotoCare - Todos os direitos reservados
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
