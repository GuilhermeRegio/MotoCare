import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import './Navbar.css';

const Navbar = () => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const [searchQuery, setSearchQuery] = useState('');

  const handleLogout = () => {
    logout();
  };

  const isActive = (path) => {
    return location.pathname.includes(path);
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark modern-navbar">
      <div className="container-fluid">
        {/* Brand */}
        <Link className="navbar-brand" to="/dashboard">
          <div className="brand-icon">
            <i className="fas fa-motorcycle"></i>
          </div>
          <span className="fw-bold">MotoCare</span>
          <small className="ms-2 opacity-75" style={{fontSize: '0.7rem'}}>v2.0</small>
        </Link>

        {/* Mobile toggle */}
        <button 
          className="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarNav">
          {/* Main Navigation */}
          <ul className="navbar-nav me-auto">
            <li className="nav-item">
              <Link 
                className={`nav-link ${isActive('/dashboard') ? 'active' : ''}`} 
                to="/dashboard"
              >
                <i className="fas fa-tachometer-alt"></i>Dashboard
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                className={`nav-link ${isActive('/motos') ? 'active' : ''}`} 
                to="/motos"
              >
                <i className="fas fa-motorcycle"></i>Motos
              </Link>
            </li>
            <li className="nav-item">
              <span className="nav-link disabled" title="Em breve">
                <i className="fas fa-wrench"></i>Manutenções
                <span className="badge bg-warning text-dark ms-1" style={{fontSize: '0.6rem'}}>Em breve</span>
              </span>
            </li>
            <li className="nav-item">
              <span className="nav-link disabled" title="Em breve">
                <i className="fas fa-brain"></i>Análises
                <span className="badge bg-info text-dark ms-1" style={{fontSize: '0.6rem'}}>IA</span>
              </span>
            </li>
            <li className="nav-item">
              <Link 
                className={`nav-link ${isActive('/relatorios') ? 'active' : ''}`} 
                to="/relatorios"
              >
                <i className="fas fa-chart-bar"></i>Relatórios
              </Link>
            </li>
          </ul>
          
          {/* Search Bar */}
          <div className="navbar-nav navbar-search d-none d-lg-flex">
            <div className="nav-item">
              <form className="d-flex position-relative">
                <input 
                  className="form-control" 
                  type="search" 
                  placeholder="Buscar moto..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
                <i className="fas fa-search search-icon"></i>
              </form>
            </div>
          </div>
          
          {/* Right side - Status + Notifications + User */}
          <div className="navbar-end">
            {/* Status do Sistema */}
            <div className="status-indicator d-none d-lg-flex">
              <span>Sistema Online</span>
            </div>
            
            {/* Notificações */}
            <div className="nav-item dropdown">
              <a 
                className="nav-link notification-link" 
                href="#" 
                id="notificationDropdown" 
                role="button" 
                data-bs-toggle="dropdown"
              >
                <i className="fas fa-bell fa-lg"></i>
                <span className="badge bg-danger notification-badge rounded-pill">3</span>
              </a>
              <ul className="dropdown-menu dropdown-menu-end notification-dropdown">
                <li className="dropdown-header">
                  <i className="fas fa-bell me-2"></i>Notificações
                </li>
                <li><hr className="dropdown-divider" /></li>
                <li>
                  <a className="dropdown-item" href="#">
                    <div className="d-flex">
                      <i className="fas fa-wrench text-warning me-3 mt-1"></i>
                      <div>
                        <strong>Manutenção pendente</strong><br />
                        <small className="text-muted">Honda CB 600 - Troca de óleo</small>
                      </div>
                    </div>
                  </a>
                </li>
                <li>
                  <a className="dropdown-item" href="#">
                    <div className="d-flex">
                      <i className="fas fa-calendar text-info me-3 mt-1"></i>
                      <div>
                        <strong>Revisão agendada</strong><br />
                        <small className="text-muted">Yamaha XJ6 - 15/09/2025</small>
                      </div>
                    </div>
                  </a>
                </li>
                <li><hr className="dropdown-divider" /></li>
                <li>
                  <a className="dropdown-item text-center" href="#">
                    Ver todas as notificações
                  </a>
                </li>
              </ul>
            </div>
            
            {/* Perfil do Usuário */}
            <div className="nav-item dropdown">
              <a 
                className="nav-link dropdown-toggle user-profile-area" 
                href="#" 
                id="userDropdown" 
                role="button" 
                data-bs-toggle="dropdown"
              >
                <div className="rounded-circle user-avatar">
                  <i className="fas fa-user"></i>
                </div>
                <div className="user-info d-none d-lg-block">
                  <div className="user-name">
                    {user?.first_name || user?.username || 'Usuário'}
                  </div>
                </div>
              </a>
              <ul className="dropdown-menu dropdown-menu-end">
                <li className="dropdown-header">
                  <i className="fas fa-user-circle me-2"></i>
                  {user?.email || 'usuário@email.com'}
                </li>
                <li><hr className="dropdown-divider" /></li>
                <li>
                  <Link className="dropdown-item" to="/configuracoes">
                    <i className="fas fa-cog me-2"></i>Configurações
                  </Link>
                </li>
                <li>
                  <a className="dropdown-item" href="#">
                    <i className="fas fa-user-edit me-2"></i>Editar Perfil
                  </a>
                </li>
                <li>
                  <a className="dropdown-item" href="#">
                    <i className="fas fa-moon me-2"></i>Modo Escuro
                  </a>
                </li>
                <li><hr className="dropdown-divider" /></li>
                <li>
                  <button 
                    type="button" 
                    className="dropdown-item text-danger border-0 bg-transparent w-100 text-start"
                    onClick={handleLogout}
                  >
                    <i className="fas fa-sign-out-alt me-2"></i>Sair
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
