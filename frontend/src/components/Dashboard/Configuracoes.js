import React from 'react';

const Configuracoes = () => {
  return (
    <div className="configuracoes-page">
      <div className="row mb-4">
        <div className="col-12">
          <h1 className="mb-1">
            <i className="fas fa-cog text-primary me-2"></i>
            Configurações
          </h1>
          <p className="text-muted mb-0">Personalize sua experiência no MotoCare.</p>
        </div>
      </div>

      <div className="row">
        <div className="col-12">
          <div className="card border-0 shadow-sm">
            <div className="card-body text-center py-5">
              <div className="mb-4">
                <i className="fas fa-tools fa-5x text-muted"></i>
              </div>
              <h3 className="mb-3">Configurações em Desenvolvimento</h3>
              <p className="mb-4 text-muted">
                Esta funcionalidade está sendo desenvolvida e estará disponível em breve.
              </p>
              <div className="alert alert-info">
                <i className="fas fa-info-circle me-2"></i>
                <strong>Em breve:</strong> Configurações de perfil, notificações, preferências e muito mais!
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Configuracoes;
