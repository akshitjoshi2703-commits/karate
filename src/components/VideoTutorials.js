import React, { useState } from 'react';
import './VideoTutorials.css';

const VIDEOS = [
  {
    id: 1,
    title: 'Basic Punch Tutorial',
    instructor: 'Master Chen',
    duration: '8:45',
    difficulty: 'Beginner',
    description: 'Learn the fundamentals of a proper karate punch with body rotation and hip engagement.',
    thumbnail: '🥊',
    videoUrl: 'https://example.com/video1',
    category: 'Striking'
  },
  {
    id: 2,
    title: 'Front Kick Mastery',
    instructor: 'Sensei Lisa',
    duration: '12:30',
    difficulty: 'Beginner',
    description: 'Complete guide to executing powerful and precise front kicks.',
    thumbnail: '🦶',
    videoUrl: 'https://example.com/video2',
    category: 'Striking'
  },
  {
    id: 3,
    title: 'Roundhouse Kick Technique',
    instructor: 'Master Chen',
    duration: '14:20',
    difficulty: 'Intermediate',
    description: 'Advanced kicking technique with demonstrations and corrections.',
    thumbnail: '🌀',
    videoUrl: 'https://example.com/video3',
    category: 'Striking'
  },
  {
    id: 4,
    title: 'Defensive Blocks',
    instructor: 'Sensei Marcus',
    duration: '10:15',
    difficulty: 'Beginner',
    description: 'Master essential blocking techniques to defend against strikes.',
    thumbnail: '🛡️',
    videoUrl: 'https://example.com/video4',
    category: 'Defense'
  },
  {
    id: 5,
    title: 'Kata - Heian Shodan',
    instructor: 'Sensei Lisa',
    duration: '18:00',
    difficulty: 'Intermediate',
    description: 'Learn the first kata form with step-by-step instructions and applications.',
    thumbnail: '🧘',
    videoUrl: 'https://example.com/video5',
    category: 'Forms'
  },
  {
    id: 6,
    title: 'Combination Drills',
    instructor: 'Master Chen',
    duration: '16:45',
    difficulty: 'Advanced',
    description: 'Complex punch and kick combinations for advanced practitioners.',
    thumbnail: '⚡',
    videoUrl: 'https://example.com/video6',
    category: 'Combinations'
  },
  {
    id: 7,
    title: 'Stance Fundamentals',
    instructor: 'Sensei Marcus',
    duration: '11:30',
    difficulty: 'Beginner',
    description: 'Understanding proper stance is crucial for balance and power.',
    thumbnail: '🚶',
    videoUrl: 'https://example.com/video7',
    category: 'Fundamentals'
  },
  {
    id: 8,
    title: 'Sparring Techniques',
    instructor: 'Master Chen',
    duration: '20:00',
    difficulty: 'Advanced',
    description: 'Learn strategies and techniques for competitive sparring.',
    thumbnail: '🥋',
    videoUrl: 'https://example.com/video8',
    category: 'Sparring'
  }
];

function VideoTutorials() {
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [watchedVideos, setWatchedVideos] = useState([]);
  const [filter, setFilter] = useState('All');

  const categories = ['All', ...new Set(VIDEOS.map(v => v.category))];

  const filteredVideos = filter === 'All' 
    ? VIDEOS 
    : VIDEOS.filter(v => v.category === filter);

  const markAsWatched = (videoId) => {
    if (!watchedVideos.includes(videoId)) {
      setWatchedVideos([...watchedVideos, videoId]);
    }
  };

  return (
    <div className="video-tutorials">
      <h2>Video Tutorials</h2>
      <p className="subtitle">Learn from expert instructors</p>

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

      <div className="videos-grid">
        {filteredVideos.map(video => (
          <div
            key={video.id}
            className={`video-card ${watchedVideos.includes(video.id) ? 'watched' : ''}`}
            onClick={() => setSelectedVideo(video)}
          >
            <div className="video-thumbnail">
              <span className="emoji">{video.thumbnail}</span>
              <span className="duration">{video.duration}</span>
              {watchedVideos.includes(video.id) && <span className="watched-badge">✓ Watched</span>}
            </div>
            <div className="video-info">
              <h3>{video.title}</h3>
              <p className="instructor">By {video.instructor}</p>
              <p className="category">{video.category}</p>
              <p className="difficulty">{video.difficulty}</p>
              <p className="description">{video.description}</p>
              <button className="watch-btn">Watch Video →</button>
            </div>
          </div>
        ))}
      </div>

      {selectedVideo && (
        <div className="modal" onClick={() => setSelectedVideo(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <button className="close-btn" onClick={() => setSelectedVideo(null)}>×</button>
            <div className="video-player">
              <div className="player-placeholder">
                <span className="play-icon">▶</span>
                <p>Video Player</p>
                {selectedVideo.thumbnail}
              </div>
            </div>

            <h2>{selectedVideo.title}</h2>
            <p className="instructor-info">
              <strong>Instructor:</strong> {selectedVideo.instructor}
            </p>
            <p className="meta-info">
              <span className="duration-badge">{selectedVideo.duration}</span>
              <span className="difficulty-badge">{selectedVideo.difficulty}</span>
              <span className="category-badge">{selectedVideo.category}</span>
            </p>

            <div className="modal-description">
              <h4>About this video:</h4>
              <p>{selectedVideo.description}</p>
            </div>

            <div className="learning-points">
              <h4>What you'll learn:</h4>
              <ul>
                <li>Proper technique and form</li>
                <li>Common mistakes to avoid</li>
                <li>Practical applications</li>
                <li>Practice tips for improvement</li>
              </ul>
            </div>

            <div className="button-group">
              <button className="play-full-btn">▶ Play Full Video</button>
              <button
                className={`watched-btn ${watchedVideos.includes(selectedVideo.id) ? 'completed' : ''}`}
                onClick={() => {
                  markAsWatched(selectedVideo.id);
                }}
              >
                {watchedVideos.includes(selectedVideo.id) ? '✓ Marked as Watched' : 'Mark as Watched'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default VideoTutorials;
