import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motosService } from '../../services/authService';

const MotosForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEdit = !!id;
  
  const [formData, setFormData] = useState({
    marca: '',
    modelo: '',
    ano: '',
    cor: '',
    km_atual: '',
    observacoes: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isEdit) {
      loadMoto();
    }
  }, [id, isEdit]);

  const loadMoto = async () => {
    try {
      setLoading(true);
      const moto = await motosService.getMoto(id);
      setFormData(moto);
    } catch (error) {
      setError('Erro ao carregar dados da moto');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (isEdit) {
        await motosService.updateMoto(id, formData);
      } else {
        await motosService.createMoto(formData);
      }
      navigate('/motos');
    } catch (error) {
      setError(error.message || 'Erro ao salvar moto');
    } finally {
      setLoading(false);
    }
  };

  if (loading && isEdit) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{minHeight: '400px'}}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Carregando...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="motos-form-page">
      <div className="row mb-4">
        <div className="col-12">
          <h1 className="mb-1">
            <i className="fas fa-motorcycle text-primary me-2"></i>
            {isEdit ? 'Editar Moto' : 'Nova Moto'}
          </h1>
          <p className="text-muted mb-0">
            {isEdit ? 'Atualize os dados da sua motocicleta.' : 'Cadastre uma nova motocicleta.'}
          </p>
        </div>
      </div>

      <div className="row">
        <div className="col-lg-8">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-light">
              <h5 className="mb-0">
                <i className="fas fa-edit me-2"></i>
                Dados da Motocicleta
              </h5>
            </div>
            <div className="card-body">
              {error && (
                <div className="alert alert-danger">
                  <i className="fas fa-exclamation-triangle me-2"></i>
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div className="row">
                  <div className="col-md-6 mb-3">
                    <label htmlFor="marca" className="form-label">Marca *</label>
                    <input
                      type="text"
                      className="form-control form-control-modern"
                      id="marca"
                      name="marca"
                      value={formData.marca}
                      onChange={handleChange}
                      required
                      disabled={loading}
                    />
                  </div>
                  <div className="col-md-6 mb-3">
                    <label htmlFor="modelo" className="form-label">Modelo *</label>
                    <input
                      type="text"
                      className="form-control form-control-modern"
                      id="modelo"
                      name="modelo"
                      value={formData.modelo}
                      onChange={handleChange}
                      required
                      disabled={loading}
                    />
                  </div>
                </div>

                <div className="row">
                  <div className="col-md-4 mb-3">
                    <label htmlFor="ano" className="form-label">Ano *</label>
                    <input
                      type="number"
                      className="form-control form-control-modern"
                      id="ano"
                      name="ano"
                      value={formData.ano}
                      onChange={handleChange}
                      required
                      min="1900"
                      max={new Date().getFullYear()}
                      disabled={loading}
                    />
                  </div>
                  <div className="col-md-4 mb-3">
                    <label htmlFor="cor" className="form-label">Cor *</label>
                    <input
                      type="text"
                      className="form-control form-control-modern"
                      id="cor"
                      name="cor"
                      value={formData.cor}
                      onChange={handleChange}
                      required
                      disabled={loading}
                    />
                  </div>
                  <div className="col-md-4 mb-3">
                    <label htmlFor="km_atual" className="form-label">Quilometragem Atual *</label>
                    <input
                      type="number"
                      className="form-control form-control-modern"
                      id="km_atual"
                      name="km_atual"
                      value={formData.km_atual}
                      onChange={handleChange}
                      required
                      min="0"
                      disabled={loading}
                    />
                  </div>
                </div>

                <div className="mb-4">
                  <label htmlFor="observacoes" className="form-label">Observações</label>
                  <textarea
                    className="form-control form-control-modern"
                    id="observacoes"
                    name="observacoes"
                    rows="3"
                    value={formData.observacoes}
                    onChange={handleChange}
                    placeholder="Informações adicionais sobre a motocicleta..."
                    disabled={loading}
                  />
                </div>

                <div className="d-flex gap-2">
                  <button 
                    type="submit" 
                    className="btn btn-primary-modern btn-lg"
                    disabled={loading}
                  >
                    <i className="fas fa-save me-2"></i>
                    {loading ? 'Salvando...' : (isEdit ? 'Atualizar' : 'Cadastrar')}
                  </button>
                  <button 
                    type="button" 
                    className="btn btn-outline-secondary btn-lg"
                    onClick={() => navigate('/motos')}
                    disabled={loading}
                  >
                    <i className="fas fa-times me-2"></i>
                    Cancelar
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <div className="col-lg-4">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-light">
              <h6 className="mb-0">
                <i className="fas fa-info-circle me-2"></i>
                Dicas
              </h6>
            </div>
            <div className="card-body">
              <div className="alert alert-info">
                <i className="fas fa-lightbulb me-2"></i>
                <strong>Dica:</strong> Mantenha os dados sempre atualizados para um melhor controle de manutenções.
              </div>
              <ul className="list-unstyled">
                <li className="mb-2">
                  <i className="fas fa-check text-success me-2"></i>
                  Informe a quilometragem atual
                </li>
                <li className="mb-2">
                  <i className="fas fa-check text-success me-2"></i>
                  Adicione observações relevantes
                </li>
                <li className="mb-2">
                  <i className="fas fa-check text-success me-2"></i>
                  Verifique os dados antes de salvar
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MotosForm;
