# 🥋 Karate Learning Academy - Python Flask App

A comprehensive, interactive web application for learning karate techniques, practicing drills, watching video tutorials, and tracking your progress through belt levels.

## Features

- **📚 Technique Library**: Learn 6+ fundamental and advanced karate techniques with step-by-step instructions
- **🎬 Video Tutorials**: Watch expert-led video demonstrations from instructors
- **💪 Interactive Drills**: Practice with guided drills to improve speed, power, and accuracy
- **📊 Progress Tracking**: Track earned points, completed techniques/drills, and advance through belt levels
- **🥋 Belt Progression System**: Progress from White Belt (beginner) to Black Belt (advanced)
- **🏆 Achievement Badges**: Earn badges as you complete milestones
- **📱 Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## Tech Stack

- **Backend**: Python 3.11 with Flask
- **Database**: SQLite (local) / PostgreSQL (production on Render)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Deployment**: Render
- **ORM**: SQLAlchemy

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/karate-learning-app.git
cd karate-learning-app
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open in browser**
```
http://localhost:5000
```

## Project Structure

```
karate-learning-app/
├── app.py                       # Main Flask application
├── requirements.txt             # Python dependencies
├── runtime.txt                  # Python version for Render
├── Procfile                     # Render deployment config
├── templates/                   # HTML templates
│   ├── base.html               # Base layout template
│   ├── index.html              # Home page
│   ├── techniques.html         # Technique library
│   ├── drills.html             # Interactive drills
│   ├── videos.html             # Video tutorials
│   └── progress.html           # Progress tracking
├── static/                      # Static files
│   ├── css/
│   │   └── style.css           # Main stylesheet
│   └── js/
│       └── script.js           # JavaScript
└── RENDER_DEPLOYMENT.md        # Deployment guide
```

## Features in Detail

### Technique Library
- Browse 6+ karate techniques organized by category (Striking, Defense, Forms, Stance)
- Filter by difficulty level (Beginner, Intermediate, Advanced)
- Detailed step-by-step instructions for each technique
- View benefits and applications
- Mark techniques as completed to earn 50 points each

### Interactive Drills
- 6 practice routines ranging from 5-20 minutes
- Built-in timer functionality
- Clear instructions and pro tips for each drill
- Track practice repetitions
- Earn 100 points per completed drill

### Video Tutorials
- 8 professional video lessons
- Expert instructors demonstrating techniques
- Categories: Striking, Defense, Forms, Combinations, Fundamentals, Sparring
- Mark videos as watched for progress tracking

### Progress Dashboard
- Real-time statistics (points, techniques, drills, belt level)
- Visual belt progression from White to Black Belt
- Progress bar showing advancement toward next belt
- Achievement badges with progress tracking
- Personalized recommendations

## Database Schema

### Users
- Session-based user management
- Tracks total points and completion history

### Completed Techniques
- Stores completed technique IDs per user
- Timestamps for tracking

### Completed Drills
- Stores completed drill IDs per user
- Timestamps for tracking

## API Endpoints

- `POST /api/technique/complete/<id>` - Mark technique as complete
- `POST /api/drill/complete/<id>` - Mark drill as complete
- `GET /api/progress` - Get user progress data

## Deployment on Render

See [RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy
1. Push code to GitHub
2. Connect repository to Render
3. Configure with:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. Deploy!

## Contributing

Contributions are welcome! Feel free to:
- Add more techniques
- Create additional drills
- Improve UI/UX
- Add new features

## License

MIT License - feel free to use this project for personal or educational purposes.

## Support

For issues or questions:
1. Check existing issues on GitHub
2. Create a new issue with detailed description
3. Contact the maintainer

---

**Happy Learning! Kihon wo taisetsu ni! (Master the fundamentals!) 🥋**
