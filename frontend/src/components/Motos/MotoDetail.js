import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motosService } from '../../services/authService';
import './MotoDetail.css';

const MotoDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [moto, setMoto] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadMoto = async () => {
      try {
        setLoading(true);
        const response = await motosService.getMoto(id);
        if (response.success) {
          setMoto(response.data);
        } else {
          setError(response.message || 'Erro ao carregar moto');
        }
      } catch (err) {
        setError(err.message || 'Erro ao carregar moto');
      } finally {
        setLoading(false);
      }
    };

    loadMoto();
  }, [id]);

  const formatKm = (km) => {
    return new Intl.NumberFormat('pt-BR').format(km);
  };

  const formatDate = (dateString) => {
    if (!dateString) return null;
    return new Date(dateString).toLocaleDateString('pt-BR');
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

  if (error) {
    return (
      <div className="container-fluid py-4">
        <div className="alert alert-danger" role="alert">
          <i className="fas fa-exclamation-triangle me-2"></i>
          {error}
        </div>
      </div>
    );
  }

  if (!moto) {
    return (
      <div className="container-fluid py-4">
        <div className="alert alert-warning" role="alert">
          <i className="fas fa-info-circle me-2"></i>
          Moto não encontrada
        </div>
      </div>
    );
  }

  return (
    <div className="container-fluid py-4">
      <div className="row">
        <div className="col-lg-8">
          <div className="card border-0 shadow-lg">
            {/* Header da Moto */}
            <div className="card-header bg-gradient-primary text-white py-4">
              <div className="d-flex align-items-center justify-content-between">
                <div className="d-flex align-items-center">
                  {moto.imagem_url ? (
                    <img 
                      src={moto.imagem_url} 
                      alt={moto.modelo} 
                      className="rounded-circle me-3" 
                      style={{ width: '60px', height: '60px', objectFit: 'cover' }}
                    />
                  ) : (
                    <div className="rounded-circle bg-white bg-opacity-20 p-3 me-3">
                      <i className="fas fa-motorcycle fa-2x"></i>
                    </div>
                  )}
                  <div>
                    <h4 className="mb-0 fw-bold">{moto.marca} {moto.modelo}</h4>
                    <p className="mb-0 opacity-75">
                      {moto.ano_display} • {moto.cor || 'Cor não informada'}
                    </p>
                  </div>
                </div>
                <div className="text-end">
                  {moto.ativo ? (
                    <span className="badge bg-success bg-opacity-20 text-success border border-success">
                      <i className="fas fa-check-circle me-1"></i>Ativa
                    </span>
                  ) : (
                    <span className="badge bg-secondary bg-opacity-20 text-secondary border border-secondary">
                      <i className="fas fa-pause-circle me-1"></i>Inativa
                    </span>
                  )}
                </div>
              </div>
            </div>

            <div className="card-body p-4">
              {/* Informações Básicas */}
              <div className="row g-4 mb-4">
                <div className="col-md-6">
                  <h6 className="text-muted mb-2">
                    <i className="fas fa-tachometer-alt me-2"></i>Quilometragem Atual
                  </h6>
                  <p className="h5 mb-0">{formatKm(moto.km_atual)} km</p>
                </div>
                <div className="col-md-6">
                  <h6 className="text-muted mb-2">
                    <i className="fas fa-shopping-cart me-2"></i>KM na Compra
                  </h6>
                  <p className="h5 mb-0">{formatKm(moto.km_compra)} km</p>
                </div>
                <div className="col-md-6">
                  <h6 className="text-muted mb-2">
                    <i className="fas fa-cog me-2"></i>Cilindrada
                  </h6>
                  <p className="h5 mb-0">{moto.cilindrada}cc</p>
                </div>
                <div className="col-md-6">
                  <h6 className="text-muted mb-2">
                    <i className="fas fa-gas-pump me-2"></i>Combustível
                  </h6>
                  <p className="h5 mb-0">{moto.tipo_combustivel}</p>
                </div>
              </div>

              {/* Informações Técnicas */}
              {(moto.tipo_motor || moto.tipo_transmissao) && (
                <>
                  <hr className="my-4" />
                  <h6 className="text-primary mb-3">
                    <i className="fas fa-cogs me-2"></i>Especificações Técnicas
                  </h6>
                  <div className="row g-3">
                    {moto.tipo_motor && (
                      <div className="col-md-6">
                        <strong>Motor:</strong> {moto.tipo_motor}
                      </div>
                    )}
                    {moto.tipo_transmissao && (
                      <div className="col-md-6">
                        <strong>Transmissão:</strong> {moto.tipo_transmissao}
                      </div>
                    )}
                  </div>
                </>
              )}

              {/* Documentação */}
              {(moto.placa || moto.chassi || moto.renavam) && (
                <>
                  <hr className="my-4" />
                  <h6 className="text-primary mb-3">
                    <i className="fas fa-file-alt me-2"></i>Documentação
                  </h6>
                  <div className="row g-3">
                    {moto.placa && (
                      <div className="col-md-4">
                        <strong>Placa:</strong> {moto.placa}
                      </div>
                    )}
                    {moto.chassi && (
                      <div className="col-md-4">
                        <strong>Chassi:</strong> {moto.chassi}
                      </div>
                    )}
                    {moto.renavam && (
                      <div className="col-md-4">
                        <strong>RENAVAM:</strong> {moto.renavam}
                      </div>
                    )}
                  </div>
                </>
              )}

              {/* Datas */}
              {(moto.data_compra || moto.data_fabricacao) && (
                <>
                  <hr className="my-4" />
                  <h6 className="text-primary mb-3">
                    <i className="fas fa-calendar me-2"></i>Datas Importantes
                  </h6>
                  <div className="row g-3">
                    {moto.data_compra && (
                      <div className="col-md-6">
                        <strong>Data da Compra:</strong> {formatDate(moto.data_compra)}
                      </div>
                    )}
                    {moto.data_fabricacao && (
                      <div className="col-md-6">
                        <strong>Data de Fabricação:</strong> {formatDate(moto.data_fabricacao)}
                      </div>
                    )}
                  </div>
                </>
              )}

              {/* Observações */}
              {moto.observacoes && (
                <>
                  <hr className="my-4" />
                  <h6 className="text-primary mb-3">
                    <i className="fas fa-comment me-2"></i>Observações
                  </h6>
                  <p className="text-muted" style={{ whiteSpace: 'pre-line' }}>
                    {moto.observacoes}
                  </p>
                </>
              )}

              {/* Botões de Ação */}
              <hr className="my-4" />
              <div className="d-flex gap-2 flex-wrap">
                <button 
                  className="btn btn-outline-primary"
                  onClick={() => navigate(`/motos/${moto.id}/editar`)}
                >
                  <i className="fas fa-edit me-2"></i>Editar
                </button>
                <button 
                  className="btn btn-outline-secondary"
                  onClick={() => navigate('/motos')}
                >
                  <i className="fas fa-list me-2"></i>Ver Todas
                </button>
                <button className="btn btn-outline-success">
                  <i className="fas fa-plus me-2"></i>Nova Manutenção
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-4">
          {/* Card de Resumo Rápido */}
          <div className="card border-0 shadow-sm mb-4">
            <div className="card-header bg-light">
              <h6 className="mb-0">
                <i className="fas fa-info-circle me-2"></i>Resumo
              </h6>
            </div>
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center mb-2">
                <span className="text-muted">KM Rodados:</span>
                <strong>{formatKm(moto.km_total_percorridos)} km</strong>
              </div>
              <div className="d-flex justify-content-between align-items-center mb-2">
                <span className="text-muted">Criado em:</span>
                <strong>{formatDate(moto.criado_em)}</strong>
              </div>
              <div className="d-flex justify-content-between align-items-center">
                <span className="text-muted">Atualizado em:</span>
                <strong>{formatDate(moto.atualizado_em)}</strong>
              </div>
            </div>
          </div>

          {/* Card de Próximas Manutenções */}
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-light">
              <h6 className="mb-0">
                <i className="fas fa-wrench me-2"></i>Próximas Manutenções
              </h6>
            </div>
            <div className="card-body text-center text-muted">
              <i className="fas fa-tools fa-2x mb-3 opacity-50"></i>
              <p>Nenhuma manutenção agendada</p>
              <button className="btn btn-sm btn-outline-primary">
                <i className="fas fa-plus me-1"></i>Agendar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MotoDetail;
