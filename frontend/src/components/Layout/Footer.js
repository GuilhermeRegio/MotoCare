import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="modern-footer">
      <div className="container">
        <div className="row align-items-center">
          <div className="col-md-6">
            <p className="mb-0">
              <i className="fas fa-copyright me-1"></i>
              2025 MotoCare - Sistema de Manutenção de Motocicletas
            </p>
          </div>
          <div className="col-md-6 text-md-end">
            <p className="mb-0">
              Desenvolvido com <i className="fas fa-heart text-danger me-1"></i>
              usando React & Django
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
