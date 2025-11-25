import React from 'react';
// import './Navbar.css'; // Removing old CSS import as we use global App.css now

const Navbar = ({ theme, toggleTheme }) => {
  return (
    <nav className="navbar">
      <a href="/" className="navbar-brand">
        LiaPlus
      </a>
      <div className="navbar-links">
        <button className="nav-btn" onClick={() => window.location.href = '/login'}>
          Login
        </button>
        <button className="nav-btn" onClick={toggleTheme}>
          {theme === 'dark' ? '☀️' : '🌙'}
        </button>
        <a
          href="https://github.com/hardiksharmmaaaa/SentiBot/tree/dev/sentiment-chatbot"
          target="_blank"
          rel="noopener noreferrer"
          className="nav-btn github-btn"
        >
          GitHub
        </a>
      </div>
    </nav>
  );
};

export default Navbar;