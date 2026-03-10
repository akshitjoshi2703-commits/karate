import React, { useState } from 'react';
import './Drills.css';

const DRILLS = [
  {
    id: 1,
    name: 'Basic Punch Drill',
    difficulty: 'Beginner',
    duration: '5 min',
    description: 'Practice basic punching combinations to build speed and accuracy',
    instructions: [
      'Stand in fighting stance',
      'Perform 10 left jabs',
      'Perform 10 right crosses',
      'Repeat 5 times with 30 seconds rest between rounds'
    ],
    tips: ['Keep hands up', 'Rotate hips', 'Focus on speed'],
    repetitions: 50
  },
  {
    id: 2,
    name: 'Kick Conditioning',
    difficulty: 'Intermediate',
    duration: '10 min',
    description: 'Build leg strength and flexibility through repetitive kicking',
    instructions: [
      'Warm up with leg stretches',
      'Perform 20 slow, controlled kicks per leg',
      'Perform 20 fast kicks per leg',
      'Hold each final kick for 3 seconds'
    ],
    tips: ['Keep core tight', 'Maintain balance', 'Increase range gradually'],
    repetitions: 80
  },
  {
    id: 3,
    name: 'Stance Practice',
    difficulty: 'Beginner',
    duration: '8 min',
    description: 'Master fundamental stances with timed holds',
    instructions: [
      'Hold Horse Stance for 30 seconds',
      'Hold Fighting Stance for 30 seconds',
      'Hold Forward Stance for 30 seconds',
      'Complete 5 rounds with 10 seconds rest'
    ],
    tips: ['Keep posture upright', 'Engage core', 'Breathe steadily'],
    repetitions: 5
  },
  {
    id: 4,
    name: 'Combination Series',
    difficulty: 'Advanced',
    duration: '15 min',
    description: 'Complex combinations of punches and kicks',
    instructions: [
      'Jab, Cross, Hook combination x 10',
      'Front Kick, Roundhouse Kick combination x 10',
      'Punch, Punch, Kick combination x 10',
      'Repeat entire series 3 times'
    ],
    tips: ['Flow smoothly between techniques', 'Maintain breathing', 'Keep hands up'],
    repetitions: 90
  },
  {
    id: 5,
    name: 'Speed Bag Work',
    difficulty: 'Intermediate',
    duration: '7 min',
    description: 'Increase hand speed and coordination',
    instructions: [
      '30 seconds slow punches',
      '30 seconds medium speed',
      '30 seconds fast punches',
      'Repeat 5 rounds'
    ],
    tips: ['Keep shoulders relaxed', 'Stay focused', 'Increase pace gradually'],
    repetitions: 150
  },
  {
    id: 6,
    name: 'Kata Repetition',
    difficulty: 'Advanced',
    duration: '20 min',
    description: 'Perfect your form through repeated kata practice',
    instructions: [
      'Perform your kata at slow speed x3',
      'Perform your kata at normal speed x3',
      'Perform your kata at fast speed x3',
      'Focus on precision over speed'
    ],
    tips: ['Breath with each movement', 'Visualize opponents', 'Perfect form'],
    repetitions: 9
  }
];

function Drills({ updateProgress }) {
  const [selectedDrill, setSelectedDrill] = useState(null);
  const [completed, setCompleted] = useState([]);
  const [activeTimer, setActiveTimer] = useState(null);

  const difficulties = ['All', 'Beginner', 'Intermediate', 'Advanced'];
  const [filter, setFilter] = useState('All');

  const filteredDrills = filter === 'All' 
    ? DRILLS 
    : DRILLS.filter(d => d.difficulty === filter);

  const completeDrill = (drillId) => {
    if (!completed.includes(drillId)) {
      setCompleted([...completed, drillId]);
      updateProgress(100, drillId, 'drill');
    }
  };

  const startTimer = (duration) => {
    const minutes = parseInt(duration);
    const totalSeconds = minutes * 60;
    let seconds = totalSeconds;

    const timer = setInterval(() => {
      seconds--;
      setActiveTimer(seconds);
      if (seconds <= 0) {
        clearInterval(timer);
        setActiveTimer(null);
      }
    }, 1000);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="drills">
      <h2>Interactive Drills</h2>
      <p className="subtitle">Practice to master your skills</p>

      <div className="filters">
        {difficulties.map(diff => (
          <button
            key={diff}
            className={`filter-btn ${filter === diff ? 'active' : ''}`}
            onClick={() => setFilter(diff)}
          >
            {diff}
          </button>
        ))}
      </div>

      <div className="drills-grid">
        {filteredDrills.map(drill => (
          <div
            key={drill.id}
            className={`drill-card ${completed.includes(drill.id) ? 'completed' : ''}`}
          >
            <div className="drill-header">
              <h3>{drill.name}</h3>
              {completed.includes(drill.id) && <span className="checkmark">✓</span>}
            </div>
            <p className="difficulty">{drill.difficulty}</p>
            <p className="duration">⏱️ {drill.duration}</p>
            <p className="description">{drill.description}</p>
            <p className="repetitions">Reps: {drill.repetitions}x</p>
            <button
              className="start-btn"
              onClick={() => setSelectedDrill(drill)}
            >
              Start Drill →
            </button>
          </div>
        ))}
      </div>

      {selectedDrill && (
        <div className="modal" onClick={() => setSelectedDrill(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <button className="close-btn" onClick={() => setSelectedDrill(null)}>×</button>
            <h2>{selectedDrill.name}</h2>
            <p className="difficulty-badge">{selectedDrill.difficulty}</p>
            <p className="modal-description">{selectedDrill.description}</p>

            <div className="timer-section">
              <p>Duration: {selectedDrill.duration}</p>
              {activeTimer && (
                <div className="timer">
                  <p className="time">{formatTime(activeTimer)}</p>
                </div>
              )}
            </div>

            <div className="modal-section">
              <h4>Instructions:</h4>
              <ol>
                {selectedDrill.instructions.map((instruction, idx) => (
                  <li key={idx}>{instruction}</li>
                ))}
              </ol>
            </div>

            <div className="modal-section">
              <h4>💡 Tips:</h4>
              <div className="tips">
                {selectedDrill.tips.map((tip, idx) => (
                  <div key={idx} className="tip-item">• {tip}</div>
                ))}
              </div>
            </div>

            <div className="button-group">
              <button
                className="timer-btn"
                onClick={() => activeTimer ? setActiveTimer(null) : startTimer(selectedDrill.duration)}
              >
                {activeTimer ? '⏸️ Stop Timer' : '▶️ Start Timer'}
              </button>
              <button
                className={`complete-btn ${completed.includes(selectedDrill.id) ? 'completed' : ''}`}
                onClick={() => {
                  completeDrill(selectedDrill.id);
                  setSelectedDrill(null);
                }}
                disabled={completed.includes(selectedDrill.id)}
              >
                {completed.includes(selectedDrill.id) ? '✓ Completed' : 'Mark Complete (+100 pts)'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Drills;
