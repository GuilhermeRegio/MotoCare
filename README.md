# MotoCare - Sistema de Gestão de Motocicletas

Sistema completo para gerenciamento de motocicletas, manutenções e custos, desenvolvido com **Django REST API** + **React**.

## 🏗️ Arquitetura

### Backend (Django REST API)
- **Django 5.2.6** com Django REST Framework
- **SQLite** para desenvolvimento
- **CORS** configurado para comunicação com React
- **Autenticação** por sessão Django

### Frontend (React)
- **React 18** com React Router
- **Bootstrap 5** para UI
- **Axios** para consumo de APIs
- **Componentes reutilizáveis**

## 📁 Estrutura do Projeto

```
MotoCare/
├── backend/                    # Django API REST
│   ├── moto_maintenance/       # Configurações principais + auth
│   ├── motos/                  # API de motos
│   ├── manutencoes/           # API de manutenções  
│   ├── dashboard/             # API de dashboard
│   ├── analises/              # API de análises
│   ├── media/                 # Uploads de arquivos
│   └── manage.py
├── frontend/                   # React App
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   ├── services/          # Serviços de API
│   │   ├── contexts/          # Contextos React
│   │   └── ...
│   ├── public/
│   └── package.json
├── venv/                      # Ambiente virtual Python
└── requirements.txt           # Dependências Python
```

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.12+
- Node.js 18+
- npm ou yarn

### Backend (Django API)

1. **Ativar ambiente virtual:**
```bash
source venv/bin/activate
```

2. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

3. **Executar migrações:**
```bash
cd backend
python manage.py migrate
```

4. **Criar superusuário (opcional):**
```bash
python manage.py createsuperuser
```

5. **Iniciar servidor:**
```bash
python manage.py runserver 8000
```

### Frontend (React)

1. **Instalar dependências:**
```bash
cd frontend
npm install
```

2. **Iniciar servidor de desenvolvimento:**
```bash
npm start
```

## 🔌 APIs Disponíveis

### Autenticação (`/api/auth/`)
- `POST /api/auth/login/` - Login com sessão Django
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/user/` - Dados do usuário autenticado
- `GET /api/auth/csrf/` - Token CSRF
- `GET /api/auth/health/` - Health check

### Motos (`/api/motos/`)
- `GET /api/motos/` - Listar motos
- `POST /api/motos/` - Criar moto
- `GET /api/motos/{id}/` - Detalhes da moto
- `PUT /api/motos/{id}/` - Atualizar moto
- `DELETE /api/motos/{id}/` - Excluir moto
- `GET /api/motos/estatisticas/` - Estatísticas das motos

### Manutenções (`/api/manutencoes/`)
- `GET /api/manutencoes/` - Listar manutenções
- `POST /api/manutencoes/` - Criar manutenção
- `GET /api/manutencoes/{id}/` - Detalhes da manutenção
- `PUT /api/manutencoes/{id}/` - Atualizar manutenção
- `DELETE /api/manutencoes/{id}/` - Excluir manutenção
- `GET /api/manutencoes/por_moto/` - Manutenções por moto
- `GET /api/manutencoes/estatisticas/` - Estatísticas

### Dashboard (`/api/dashboard/`)
- `GET /api/dashboard/` - Dados completos do dashboard

### Análises (`/api/analises/`)
- `GET /api/analises/gastos_mensais/` - Análise de gastos mensais
- `GET /api/analises/gastos_por_moto/` - Gastos por moto
- `GET /api/analises/tipos_manutencao/` - Tipos de manutenção
- `GET /api/analises/eficiencia_combustivel/` - Eficiência de combustível

## 🎯 Funcionalidades

### Gestão de Motos
- ✅ Cadastro completo de motocicletas
- ✅ Controle de quilometragem
- ✅ Upload de documentos e fotos
- ✅ Histórico detalhado

### Gestão de Manutenções
- ✅ Planejamento de manutenções
- ✅ Controle de custos
- ✅ Status de execução
- ✅ Relatórios detalhados

### Dashboard e Análises
- ✅ Visão geral do sistema
- ✅ Métricas importantes
- ✅ Gráficos e relatórios
- ✅ Análise de gastos

## 🔧 Configuração para Produção

Para produção, altere as seguintes configurações:

### Backend
1. **Altere as permissões de `AllowAny` para `IsAuthenticated`** nos ViewSets
2. **Configure `ALLOWED_HOSTS`** no settings.py
3. **Configure banco de dados** (PostgreSQL recomendado)
4. **Configure `DEBUG = False`**
5. **Configure `CORS_ALLOW_ALL_ORIGINS = False`**

### Frontend
1. **Configure `REACT_APP_API_URL`** para URL de produção
2. **Execute `npm run build`** para build de produção

## 🛠️ Tecnologias Utilizadas

### Backend
- Django 5.2.6
- Django REST Framework
- Django CORS Headers
- Pillow (para imagens)
- SQLite (desenvolvimento)

### Frontend
- React 18
- React Router DOM
- Axios
- Bootstrap 5
- Font Awesome

## 📝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!**
