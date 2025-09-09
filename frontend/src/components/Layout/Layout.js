import React from 'react';
import Navbar from './Navbar';
import Footer from './Footer';
import './Layout.css';

const Layout = ({ children }) => {
  return (
    <div className="layout">
      <Navbar />
      <main className="main-content">
        <div className="container-fluid py-4">
          <div className="container">
            {children}
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Layout;
