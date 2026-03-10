import React, { useState } from 'react';
import './TechniqueLibrary.css';

const TECHNIQUES = [
  {
    id: 1,
    name: 'Punch (Zuki)',
    category: 'Striking',
    difficulty: 'Beginner',
    description: 'A fundamental strike executed with a closed fist, driving power from the hips and core.',
    steps: [
      'Stand in fighting stance with feet shoulder-width apart',
      'Rotate hips and core toward the target',
      'Extend arm fully while keeping elbow straight',
      'Keep other hand protecting your face',
      'Retract hand quickly after impact'
    ],
    benefits: ['Core strength', 'Upper body power', 'Coordination']
  },
  {
    id: 2,
    name: 'Kick (Geri)',
    category: 'Striking',
    difficulty: 'Intermediate',
    description: 'A versatile leg strike that generates tremendous power and reach.',
    steps: [
      'Start in fighting stance',
      'Chamber knee up to waist height',
      'Extend leg toward target',
      'Keep supporting leg slightly bent',
      'Retract leg quickly and return to stance'
    ],
    benefits: ['Leg strength', 'Balance', 'Flexibility', 'Range']
  },
  {
    id: 3,
    name: 'Block (Uke)',
    category: 'Defense',
    difficulty: 'Beginner',
    description: 'Essential defensive technique to protect against incoming strikes.',
    steps: [
      'Anticipate incoming attack',
      'Raise forearm to intercept strike',
      'Use entire arm to redirect force',
      'Keep hands ready for counterattack',
      'Maintain balance and stance'
    ],
    benefits: ['Defensive skills', 'Reaction time', 'Upper body conditioning']
  },
  {
    id: 4,
    name: 'Kata (Forms)',
    category: 'Forms',
    difficulty: 'Intermediate',
    description: 'Pre-arranged sequences of techniques performed against imaginary opponents.',
    steps: [
      'Memorize the sequence of moves',
      'Practice each movement with precision',
      'Flow smoothly from one technique to another',
      'Focus on proper form and breathing',
      'Increase speed while maintaining accuracy'
    ],
    benefits: ['Body control', 'Memorization', 'Meditation', 'Breathing']
  },
  {
    id: 5,
    name: 'Roundhouse Kick (Mawashi Geri)',
    category: 'Striking',
    difficulty: 'Intermediate',
    description: 'A powerful circular kick using the shin or instep to strike.',
    steps: [
      'Chamber knee at hip height',
      'Rotate hips dramatically',
      'Swing leg in circular motion',
      'Strike with shin or instep',
      'Chamber leg and return to position'
    ],
    benefits: ['Hip flexibility', 'Core power', 'Leg conditioning']
  },
  {
    id: 6,
    name: 'Horse Stance (Kiba Dachi)',
    category: 'Stance',
    difficulty: 'Beginner',
    description: 'A fundamental wide stance that develops leg strength and stability.',
    steps: [
      'Stand with feet about twice shoulder-width apart',
      'Keep knees bent at 45-degree angle',
      'Maintain upright posture',
      'Keep weight centered',
      'Hold position for extended periods'
    ],
    benefits: ['Leg strength', 'Stability', 'Balance', 'Endurance']
  }
];

function TechniqueLibrary({ updateProgress }) {
  const [selectedTechnique, setSelectedTechnique] = useState(null);
  const [filter, setFilter] = useState('All');
  const [completed, setCompleted] = useState([]);

  const categories = ['All', ...new Set(TECHNIQUES.map(t => t.category))];
  
  const filteredTechniques = filter === 'All' 
    ? TECHNIQUES 
    : TECHNIQUES.filter(t => t.category === filter);

  const markComplete = (techniqueId) => {
    if (!completed.includes(techniqueId)) {
      setCompleted([...completed, techniqueId]);
      updateProgress(50, techniqueId, 'technique');
    }
  };

  return (
    <div className="technique-library">
      <h2>Technique Library</h2>
      <p className="subtitle">Learn fundamental and advanced karate techniques</p>

      <div className="filters">
        {categories.map(cat => (
          <button
            key={cat}
            className={`filter-btn ${filter === cat ? 'active' : ''}`}
            onClick={() => setFilter(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      <div className="techniques-grid">
        {filteredTechniques.map(technique => (
          <div
            key={technique.id}
            className={`technique-card ${completed.includes(technique.id) ? 'completed' : ''}`}
            onClick={() => setSelectedTechnique(technique)}
          >
            <div className="technique-header">
              <h3>{technique.name}</h3>
              {completed.includes(technique.id) && <span className="checkmark">✓</span>}
            </div>
            <p className="category">{technique.category}</p>
            <p className="difficulty">{technique.difficulty}</p>
            <p className="description">{technique.description}</p>
            <button
              className="learn-btn"
              onClick={(e) => {
                e.stopPropagation();
                setSelectedTechnique(technique);
              }}
            >
              Learn More →
            </button>
          </div>
        ))}
      </div>

      {selectedTechnique && (
        <div className="modal" onClick={() => setSelectedTechnique(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <button className="close-btn" onClick={() => setSelectedTechnique(null)}>×</button>
            <h2>{selectedTechnique.name}</h2>
            <p className="modal-description">{selectedTechnique.description}</p>

            <div className="modal-section">
              <h4>Steps to Execute:</h4>
              <ol>
                {selectedTechnique.steps.map((step, idx) => (
                  <li key={idx}>{step}</li>
                ))}
              </ol>
            </div>

            <div className="modal-section">
              <h4>Benefits:</h4>
              <div className="benefits">
                {selectedTechnique.benefits.map((benefit, idx) => (
                  <span key={idx} className="benefit-tag">{benefit}</span>
                ))}
              </div>
            </div>

            <button
              className={`complete-btn ${completed.includes(selectedTechnique.id) ? 'completed' : ''}`}
              onClick={() => {
                markComplete(selectedTechnique.id);
                setSelectedTechnique(null);
              }}
              disabled={completed.includes(selectedTechnique.id)}
            >
              {completed.includes(selectedTechnique.id) ? '✓ Completed' : 'Mark as Complete (+50 pts)'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default TechniqueLibrary;
