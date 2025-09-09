import React from 'react';
import { useAuth } from '../../contexts/AuthContext';

const DashboardTest = () => {
  const { user } = useAuth();
  
  console.log('=== DashboardTest Rendering ===');
  console.log('User:', user);

  return (
    <div className="container-fluid p-4">
      <h1>Dashboard Funcionando!</h1>
      <p>Usuário: {user?.username || 'Não identificado'}</p>
      <div className="alert alert-success">
        Se você está vendo esta mensagem, o Dashboard está renderizando corretamente.
      </div>
    </div>
  );
};

export default DashboardTest;
