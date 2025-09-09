import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motosService } from '../../services/authService';

const MotosList = () => {
  const [motos, setMotos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadMotos();
  }, []);

  const loadMotos = async () => {
    try {
      const data = await motosService.getMotos();
      // A API retorna um objeto com paginação, precisamos acessar a propriedade 'results'
      setMotos(data.results || []);
    } catch (error) {
      setError('Erro ao carregar motos');
      console.error('Erro ao carregar motos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir esta moto?')) {
      try {
        await motosService.deleteMoto(id);
        setMotos(motos.filter(moto => moto.id !== id));
      } catch (error) {
        setError('Erro ao excluir moto');
      }
    }
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
    <div className="motos-list-page">
      <div className="row mb-4">
        <div className="col-12">
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <h1 className="mb-1">
                <i className="fas fa-motorcycle text-primary me-2"></i>
                Suas Motos
              </h1>
              <p className="text-muted mb-0">Gerencie sua frota de motocicletas.</p>
            </div>
            <div>
              <Link to="/motos/novo" className="btn btn-primary btn-lg">
                <i className="fas fa-plus me-2"></i>Nova Moto
              </Link>
            </div>
          </div>
        </div>
      </div>

      {error && (
        <div className="alert alert-danger">
          <i className="fas fa-exclamation-triangle me-2"></i>
          {error}
        </div>
      )}

      {motos.length === 0 ? (
        <div className="row">
          <div className="col-12">
            <div className="card border-0 shadow-sm">
              <div className="card-body text-center py-5">
                <div className="mb-4">
                  <i className="fas fa-motorcycle fa-5x text-muted"></i>
                </div>
                <h3 className="mb-3">Nenhuma moto cadastrada</h3>
                <p className="mb-4 text-muted">
                  Comece cadastrando sua primeira motocicleta.
                </p>
                <Link to="/motos/novo" className="btn btn-primary btn-lg">
                  <i className="fas fa-plus me-2"></i>Cadastrar Primeira Moto
                </Link>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="row">
          {motos.map((moto) => (
            <div key={moto.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100 border-0 shadow-sm hover-lift">
                <div className="card-body">
                  <div className="d-flex align-items-center mb-3">
                    <div className="rounded-circle bg-primary bg-opacity-10 p-3 me-3">
                      <i className="fas fa-motorcycle fa-2x text-primary"></i>
                    </div>
                    <div>
                      <h5 className="mb-0">{moto.marca} {moto.modelo}</h5>
                      <small className="text-muted">Ano {moto.ano}</small>
                    </div>
                  </div>
                  
                  <div className="row g-2 mb-3">
                    <div className="col-6">
                      <div className="p-2 bg-light rounded text-center">
                        <small className="text-muted d-block">KM Atual</small>
                        <strong className="text-success">
                          {moto.km_atual?.toLocaleString('pt-BR')}
                        </strong>
                      </div>
                    </div>
                    <div className="col-6">
                      <div className="p-2 bg-light rounded text-center">
                        <small className="text-muted d-block">Cor</small>
                        <strong className="text-info">{moto.cor}</strong>
                      </div>
                    </div>
                  </div>
                  
                  <div className="d-grid gap-2">
                    <Link to={`/motos/${moto.id}`} className="btn btn-outline-primary btn-sm">
                      <i className="fas fa-eye me-2"></i>Detalhes
                    </Link>
                    <div className="btn-group">
                      <Link to={`/motos/editar/${moto.id}`} className="btn btn-outline-secondary btn-sm">
                        <i className="fas fa-edit me-1"></i>Editar
                      </Link>
                      <button 
                        onClick={() => handleDelete(moto.id)}
                        className="btn btn-outline-danger btn-sm"
                      >
                        <i className="fas fa-trash me-1"></i>Excluir
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MotosList;
