import React, { useState } from 'react';
import './App.css';
import Navigation from './components/Navigation';
import TechniqueLibrary from './components/TechniqueLibrary';
import Drills from './components/Drills';
import Progress from './components/Progress';
import VideoTutorials from './components/VideoTutorials';

function App() {
  const [currentView, setCurrentView] = useState('home');
  const [userProgress, setUserProgress] = useState({
    level: 1,
    totalPoints: 0,
    completedTechniques: [],
    completedDrills: [],
    beltLevel: 'White'
  });

  const updateProgress = (pointsEarned, newItem, itemType) => {
    setUserProgress(prev => ({
      ...prev,
      totalPoints: prev.totalPoints + pointsEarned,
      completedTechniques: itemType === 'technique' ? [...prev.completedTechniques, newItem] : prev.completedTechniques,
      completedDrills: itemType === 'drill' ? [...prev.completedDrills, newItem] : prev.completedDrills
    }));
  };

  const renderContent = () => {
    switch(currentView) {
      case 'techniques':
        return <TechniqueLibrary updateProgress={updateProgress} />;
      case 'drills':
        return <Drills updateProgress={updateProgress} />;
      case 'videos':
        return <VideoTutorials />;
      case 'progress':
        return <Progress userProgress={userProgress} />;
      default:
        return <HomePage />;
    }
  };

  return (
    <div className="app">
      <Navigation currentView={currentView} setCurrentView={setCurrentView} />
      <main className="main-content">
        {renderContent()}
      </main>
    </div>
  );
}

function HomePage() {
  return (
    <div className="home-page">
      <div className="hero">
        <h1>🥋 Karate Learning Academy</h1>
        <p>Master the art of karate at your own pace</p>
      </div>
      <div className="features">
        <div className="feature-card">
          <h3>📚 Learn Techniques</h3>
          <p>Discover fundamental and advanced karate techniques with detailed instructions and images</p>
        </div>
        <div className="feature-card">
          <h3>🎬 Video Tutorials</h3>
          <p>Watch step-by-step video demonstrations from expert instructors</p>
        </div>
        <div className="feature-card">
          <h3>💪 Interactive Drills</h3>
          <p>Practice with guided drills to enhance your skills and consistency</p>
        </div>
        <div className="feature-card">
          <h3>📊 Track Progress</h3>
          <p>Monitor your learning journey and advance through belt levels</p>
        </div>
      </div>
    </div>
  );
}

export default App;
