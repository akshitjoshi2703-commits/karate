import React from 'react';
import './Navigation.css';

function Navigation({ currentView, setCurrentView }) {
  return (
    <nav className="navbar">
      <div className="nav-container">
        <div className="logo" onClick={() => setCurrentView('home')}>
          🥋 Karate Academy
        </div>
        <ul className="nav-links">
          <li className={currentView === 'home' ? 'active' : ''}>
            <button onClick={() => setCurrentView('home')}>Home</button>
          </li>
          <li className={currentView === 'techniques' ? 'active' : ''}>
            <button onClick={() => setCurrentView('techniques')}>📚 Techniques</button>
          </li>
          <li className={currentView === 'videos' ? 'active' : ''}>
            <button onClick={() => setCurrentView('videos')}>🎬 Videos</button>
          </li>
          <li className={currentView === 'drills' ? 'active' : ''}>
            <button onClick={() => setCurrentView('drills')}>💪 Drills</button>
          </li>
          <li className={currentView === 'progress' ? 'active' : ''}>
            <button onClick={() => setCurrentView('progress')}>📊 Progress</button>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navigation;
