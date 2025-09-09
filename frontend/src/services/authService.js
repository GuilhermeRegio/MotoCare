import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Configure axios
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for session-based auth
});

// Request interceptor for authentication
api.interceptors.request.use(
  (config) => {
    // Get CSRF token if available
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login on unauthorized
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authService = {
  login: async (username, password) => {
    try {
      const response = await api.post('/auth/login/', {
        username,
        password,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Erro de conexão' };
    }
  },

  logout: async () => {
    try {
      await api.post('/auth/logout/');
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
    }
  },

  getCurrentUser: async () => {
    try {
      const response = await api.get('/auth/user/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao obter usuário' };
    }
  },

  getCSRFToken: async () => {
    try {
      const response = await api.get('/auth/csrf/');
      return response.data;
    } catch (error) {
      console.error('Erro ao obter CSRF token:', error);
      return null;
    }
  },
};

export const motosService = {
  getMotos: async () => {
    try {
      const response = await api.get('/motos/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao carregar motos' };
    }
  },

  getMoto: async (id) => {
    try {
      const response = await api.get(`/motos/${id}/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao carregar moto' };
    }
  },

  createMoto: async (motoData) => {
    try {
      const response = await api.post('/motos/', motoData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao criar moto' };
    }
  },

  updateMoto: async (id, motoData) => {
    try {
      const response = await api.put(`/motos/${id}/`, motoData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao atualizar moto' };
    }
  },

  deleteMoto: async (id) => {
    try {
      await api.delete(`/motos/${id}/`);
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao excluir moto' };
    }
  },

  getEstatisticas: async () => {
    try {
      const response = await api.get('/motos/estatisticas/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao carregar estatísticas' };
    }
  },
};

export const dashboardService = {
  getDashboardData: async () => {
    try {
      const response = await api.get('/dashboard/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao carregar dashboard' };
    }
  },
};

export const manutencaoService = {
  getManutencoes: async () => {
    try {
      const response = await api.get('/manutencoes/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao carregar manutenções' };
    }
  },

  getManutencoesPorMoto: async (motoId) => {
    try {
      const response = await api.get(`/manutencoes/por_moto/?moto_id=${motoId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao carregar manutenções da moto' };
    }
  },

  createManutencao: async (manutencaoData) => {
    try {
      const response = await api.post('/manutencoes/', manutencaoData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao criar manutenção' };
    }
  },

  updateManutencao: async (id, manutencaoData) => {
    try {
      const response = await api.put(`/manutencoes/${id}/`, manutencaoData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao atualizar manutenção' };
    }
  },

  deleteManutencao: async (id) => {
    try {
      await api.delete(`/manutencoes/${id}/`);
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao excluir manutenção' };
    }
  },

  getEstatisticas: async () => {
    try {
      const response = await api.get('/manutencoes/estatisticas/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao carregar estatísticas' };
    }
  },
};

export const analiseService = {
  getGastosMensais: async () => {
    try {
      const response = await api.get('/analises/gastos_mensais/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao carregar gastos mensais' };
    }
  },

  getGastosPorMoto: async () => {
    try {
      const response = await api.get('/analises/gastos_por_moto/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao carregar gastos por moto' };
    }
  },

  getTiposManutencao: async () => {
    try {
      const response = await api.get('/analises/tipos_manutencao/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao carregar tipos de manutenção' };
    }
  },

  getEficienciaCombustivel: async () => {
    try {
      const response = await api.get('/analises/eficiencia_combustivel/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Erro ao carregar eficiência de combustível' };
    }
  },
};

export default api;
