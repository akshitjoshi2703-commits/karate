import React from 'react';
import './Progress.css';

const BELT_LEVELS = [
  { level: 1, name: 'White Belt', minPoints: 0, maxPoints: 300, color: '#ecf0f1' },
  { level: 2, name: 'Yellow Belt', minPoints: 300, maxPoints: 600, color: '#f1c40f' },
  { level: 3, name: 'Orange Belt', minPoints: 600, maxPoints: 900, color: '#e67e22' },
  { level: 4, name: 'Green Belt', minPoints: 900, maxPoints: 1200, color: '#27ae60' },
  { level: 5, name: 'Blue Belt', minPoints: 1200, maxPoints: 1500, color: '#3498db' },
  { level: 6, name: 'Purple Belt', minPoints: 1500, maxPoints: 1800, color: '#9b59b6' },
  { level: 7, name: 'Brown Belt', minPoints: 1800, maxPoints: 2100, color: '#8b4513' },
  { level: 8, name: 'Black Belt', minPoints: 2100, maxPoints: 3000, color: '#2c3e50' }
];

function Progress({ userProgress }) {
  const currentBelt = BELT_LEVELS.find(b => 
    userProgress.totalPoints >= b.minPoints && userProgress.totalPoints < b.maxPoints
  ) || BELT_LEVELS[0];

  const nextBelt = BELT_LEVELS[currentBelt.level] || currentBelt;
  const progressPercentage = ((userProgress.totalPoints - currentBelt.minPoints) / 
    (currentBelt.maxPoints - currentBelt.minPoints)) * 100;

  const stats = [
    { label: 'Total Points', value: userProgress.totalPoints, icon: '⭐' },
    { label: 'Techniques Learned', value: userProgress.completedTechniques.length, icon: '📚' },
    { label: 'Drills Completed', value: userProgress.completedDrills.length, icon: '💪' },
    { label: 'Current Level', value: currentBelt.level, icon: '🥋' }
  ];

  return (
    <div className="progress">
      <h2>Your Progress Dashboard</h2>
      <p className="subtitle">Track your karate journey</p>

      <div className="stats-grid">
        {stats.map((stat, idx) => (
          <div key={idx} className="stat-card">
            <span className="stat-icon">{stat.icon}</span>
            <h3>{stat.label}</h3>
            <p className="stat-value">{stat.value}</p>
          </div>
        ))}
      </div>

      <div className="belt-section">
        <h3>Current Belt Rank</h3>
        <div className="belt-display">
          <div 
            className="belt" 
            style={{ backgroundColor: currentBelt.color }}
            title={currentBelt.name}
          ></div>
          <div className="belt-info">
            <h2>{currentBelt.name}</h2>
            <p>Level {currentBelt.level} of {BELT_LEVELS.length}</p>
          </div>
        </div>

        <div className="progression-path">
          <h3>Belt Progression Path</h3>
          <div className="belts-timeline">
            {BELT_LEVELS.map((belt, idx) => (
              <div
                key={belt.level}
                className={`belt-item ${currentBelt.level >= belt.level ? 'completed' : ''} ${currentBelt.level === belt.level ? 'current' : ''}`}
              >
                <div 
                  className="belt-circle"
                  style={{ backgroundColor: belt.color }}
                ></div>
                <p>{belt.name}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="progress-bar-section">
          <div className="progress-info">
            <span>Progress to {nextBelt.name}</span>
            <span className="points">{userProgress.totalPoints} / {nextBelt.maxPoints} points</span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill"
              style={{ 
                width: `${progressPercentage}%`,
                backgroundColor: currentBelt.color
              }}
            ></div>
          </div>
          <div className="progress-percentage">{Math.round(progressPercentage)}%</div>
        </div>
      </div>

      <div className="achievements-section">
        <h3>🏆 Your Achievements</h3>
        <div className="achievements-grid">
          <div className="achievement-card">
            <span className="achievement-icon">🥋</span>
            <h4>Beginner's Journey</h4>
            <p>Earned after reaching Yellow Belt</p>
            <progress value={currentBelt.level} max="2" style={{ width: '100%' }}></progress>
          </div>
          <div className="achievement-card">
            <span className="achievement-icon">🔥</span>
            <h4>Dedicated Practitioner</h4>
            <p>Earned after 10 completed drills</p>
            <progress value={userProgress.completedDrills.length} max="10" style={{ width: '100%' }}></progress>
          </div>
          <div className="achievement-card">
            <span className="achievement-icon">📚</span>
            <h4>Technique Master</h4>
            <p>Earned after learning 6 techniques</p>
            <progress value={userProgress.completedTechniques.length} max="6" style={{ width: '100%' }}></progress>
          </div>
          <div className="achievement-card">
            <span className="achievement-icon">⭐</span>
            <h4>Rising Champion</h4>
            <p>Earned after 500 total points</p>
            <progress value={userProgress.totalPoints} max="500" style={{ width: '100%' }}></progress>
          </div>
        </div>
      </div>

      <div className="recommendations">
        <h3>📋 Personalized Recommendations</h3>
        <div className="recommendation-list">
          <div className="recommendation-item">
            <span className="rec-icon">✨</span>
            <p>You're {Math.round(progressPercentage)}% of the way to {nextBelt.name}! Keep practicing to advance.</p>
          </div>
          <div className="recommendation-item">
            <span className="rec-icon">💡</span>
            <p>Try practicing {Math.min(3, 12 - userProgress.completedTechniques.length)} more techniques to unlock new drills.</p>
          </div>
          <div className="recommendation-item">
            <span className="rec-icon">🎯</span>
            <p>Complete 3 more drills this week to stay on pace for your next belt level.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Progress;
