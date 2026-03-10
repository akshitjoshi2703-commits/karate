import os
from flask import Flask, render_template, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'karate-dev-key-2026')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///karate.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Initialize database
db = SQLAlchemy(app)

# ============ DATABASE MODELS ============
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    total_points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CompletedTechnique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    technique_id = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

class CompletedDrill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    drill_id = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables when app starts
with app.app_context():
    db.create_all()

# ============ STATIC DATA ============
TECHNIQUES = [
    {
        'id': 1, 'name': 'Punch (Zuki)', 'category': 'Striking', 'difficulty': 'Beginner',
        'description': 'A fundamental strike executed with a closed fist, driving power from the hips and core.',
        'steps': ['Stand in fighting stance', 'Rotate hips and core', 'Extend arm fully', 'Keep guard up', 'Retract quickly'],
        'benefits': ['Core strength', 'Upper body power', 'Coordination']
    },
    {
        'id': 2, 'name': 'Kick (Geri)', 'category': 'Striking', 'difficulty': 'Intermediate',
        'description': 'A versatile leg strike that generates tremendous power and reach.',
        'steps': ['Start in stance', 'Chamber knee', 'Extend leg', 'Keep support leg bent', 'Return to stance'],
        'benefits': ['Leg strength', 'Balance', 'Flexibility', 'Range']
    },
    {
        'id': 3, 'name': 'Block (Uke)', 'category': 'Defense', 'difficulty': 'Beginner',
        'description': 'Essential defensive technique to protect against incoming strikes.',
        'steps': ['Anticipate attack', 'Raise forearm', 'Redirect force', 'Ready counterattack', 'Maintain balance'],
        'benefits': ['Defensive skills', 'Reaction time', 'Upper body']
    },
    {
        'id': 4, 'name': 'Kata (Forms)', 'category': 'Forms', 'difficulty': 'Intermediate',
        'description': 'Pre-arranged sequences of techniques performed.',
        'steps': ['Memorize sequence', 'Practice precision', 'Flow smoothly', 'Focus on breathing', 'Increase speed'],
        'benefits': ['Body control', 'Memorization', 'Meditation', 'Breathing']
    },
    {
        'id': 5, 'name': 'Roundhouse Kick', 'category': 'Striking', 'difficulty': 'Intermediate',
        'description': 'A powerful circular kick using the shin or instep.',
        'steps': ['Chamber knee', 'Rotate hips', 'Swing leg circular', 'Strike with shin', 'Return to position'],
        'benefits': ['Hip flexibility', 'Core power', 'Leg conditioning']
    },
    {
        'id': 6, 'name': 'Horse Stance', 'category': 'Stance', 'difficulty': 'Beginner',
        'description': 'A fundamental wide stance that develops leg strength.',
        'steps': ['Wide stance', 'Bent knees', 'Upright posture', 'Centered weight', 'Hold position'],
        'benefits': ['Leg strength', 'Stability', 'Balance', 'Endurance']
    }
]

DRILLS = [
    {
        'id': 1, 'name': 'Basic Punch Drill', 'difficulty': 'Beginner', 'duration': '5 min',
        'description': 'Practice basic punching combinations.',
        'instructions': ['Stand in fighting stance', 'Perform 10 left jabs', 'Perform 10 right crosses', 'Repeat 5 times'],
        'tips': ['Keep hands up', 'Rotate hips', 'Focus on speed'], 'repetitions': 50
    },
    {
        'id': 2, 'name': 'Kick Conditioning', 'difficulty': 'Intermediate', 'duration': '10 min',
        'description': 'Build leg strength and flexibility.',
        'instructions': ['Warm up with stretches', '20 slow kicks per leg', '20 fast kicks per leg', 'Hold final kick'],
        'tips': ['Keep core tight', 'Maintain balance', 'Increase range'], 'repetitions': 80
    },
    {
        'id': 3, 'name': 'Stance Practice', 'difficulty': 'Beginner', 'duration': '8 min',
        'description': 'Master fundamental stances.',
        'instructions': ['Hold Horse Stance', 'Hold Fighting Stance', 'Hold Forward Stance', 'Complete 5 rounds'],
        'tips': ['Keep posture upright', 'Engage core', 'Breathe steadily'], 'repetitions': 5
    },
    {
        'id': 4, 'name': 'Combination Series', 'difficulty': 'Advanced', 'duration': '15 min',
        'description': 'Complex combinations of punches and kicks.',
        'instructions': ['Jab, Cross, Hook x10', 'Kick combinations x10', 'Punch-Punch-Kick x10', 'Repeat 3 times'],
        'tips': ['Flow smoothly', 'Maintain breathing', 'Keep hands up'], 'repetitions': 90
    },
    {
        'id': 5, 'name': 'Speed Bag Work', 'difficulty': 'Intermediate', 'duration': '7 min',
        'description': 'Increase hand speed and coordination.',
        'instructions': ['30s slow punches', '30s medium speed', '30s fast punches', 'Repeat 5 rounds'],
        'tips': ['Shoulders relaxed', 'Stay focused', 'Increase pace'], 'repetitions': 150
    },
    {
        'id': 6, 'name': 'Kata Repetition', 'difficulty': 'Advanced', 'duration': '20 min',
        'description': 'Perfect your form through practice.',
        'instructions': ['Kata slow speed x3', 'Kata normal speed x3', 'Kata fast speed x3', 'Focus on precision'],
        'tips': ['Breathe with movement', 'Visualize opponents', 'Perfect form'], 'repetitions': 9
    }
]

VIDEOS = [
    {'id': 1, 'title': 'Basic Punch Tutorial', 'instructor': 'Master Chen', 'duration': '8:45', 'difficulty': 'Beginner', 'description': 'Learn proper karate punch.', 'category': 'Striking'},
    {'id': 2, 'title': 'Front Kick Mastery', 'instructor': 'Sensei Lisa', 'duration': '12:30', 'difficulty': 'Beginner', 'description': 'Execute powerful front kicks.', 'category': 'Striking'},
    {'id': 3, 'title': 'Roundhouse Kick', 'instructor': 'Master Chen', 'duration': '14:20', 'difficulty': 'Intermediate', 'description': 'Advanced kicking technique.', 'category': 'Striking'},
    {'id': 4, 'title': 'Defensive Blocks', 'instructor': 'Sensei Marcus', 'duration': '10:15', 'difficulty': 'Beginner', 'description': 'Essential blocking techniques.', 'category': 'Defense'},
    {'id': 5, 'title': 'Kata - Heian Shodan', 'instructor': 'Sensei Lisa', 'duration': '18:00', 'difficulty': 'Intermediate', 'description': 'First kata form.', 'category': 'Forms'},
    {'id': 6, 'title': 'Combination Drills', 'instructor': 'Master Chen', 'duration': '16:45', 'difficulty': 'Advanced', 'description': 'Complex combinations.', 'category': 'Combinations'},
    {'id': 7, 'title': 'Stance Fundamentals', 'instructor': 'Sensei Marcus', 'duration': '11:30', 'difficulty': 'Beginner', 'description': 'Proper stance importance.', 'category': 'Fundamentals'},
    {'id': 8, 'title': 'Sparring Techniques', 'instructor': 'Master Chen', 'duration': '20:00', 'difficulty': 'Advanced', 'description': 'Competitive sparring.', 'category': 'Sparring'}
]

BELT_LEVELS = [
    {'level': 1, 'name': 'White Belt', 'minPoints': 0, 'maxPoints': 300},
    {'level': 2, 'name': 'Yellow Belt', 'minPoints': 300, 'maxPoints': 600},
    {'level': 3, 'name': 'Orange Belt', 'minPoints': 600, 'maxPoints': 900},
    {'level': 4, 'name': 'Green Belt', 'minPoints': 900, 'maxPoints': 1200},
    {'level': 5, 'name': 'Blue Belt', 'minPoints': 1200, 'maxPoints': 1500},
    {'level': 6, 'name': 'Purple Belt', 'minPoints': 1500, 'maxPoints': 1800},
    {'level': 7, 'name': 'Brown Belt', 'minPoints': 1800, 'maxPoints': 2100},
    {'level': 8, 'name': 'Black Belt', 'minPoints': 2100, 'maxPoints': 3000}
]


# ============ HELPER FUNCTIONS ============
def get_or_create_user():
    """Get or create user session"""
    if 'user_id' not in session:
        user = User(session_id=os.urandom(16).hex())
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
    return User.query.get(session['user_id'])

def get_user_progress(user):
    """Calculate user progress"""
    techniques_count = CompletedTechnique.query.filter_by(user_id=user.id).count()
    drills_count = CompletedDrill.query.filter_by(user_id=user.id).count()
    
    current_belt = next((b for b in BELT_LEVELS if user.total_points >= b['minPoints'] and user.total_points < b['maxPoints']), BELT_LEVELS[0])
    progress_pct = int(((user.total_points - current_belt['minPoints']) / (current_belt['maxPoints'] - current_belt['minPoints'])) * 100) if current_belt['maxPoints'] > current_belt['minPoints'] else 0
    
    return {
        'total_points': user.total_points,
        'completed_techniques': techniques_count,
        'completed_drills': drills_count,
        'current_belt': current_belt['name'],
        'level': current_belt['level'],
        'progress_percentage': progress_pct
    }

# ============ ROUTES ============
@app.route('/')
def home():
    user = get_or_create_user()
    progress = get_user_progress(user)
    return render_template('index.html', progress=progress)

@app.route('/techniques')
def techniques():
    user = get_or_create_user()
    completed = [t.technique_id for t in CompletedTechnique.query.filter_by(user_id=user.id).all()]
    return render_template('techniques.html', techniques=TECHNIQUES, completed=completed)

@app.route('/drills')
def drills():
    user = get_or_create_user()
    completed = [d.drill_id for d in CompletedDrill.query.filter_by(user_id=user.id).all()]
    return render_template('drills.html', drills=DRILLS, completed=completed)

@app.route('/videos')
def videos():
    return render_template('videos.html', videos=VIDEOS)

@app.route('/progress')
def progress():
    user = get_or_create_user()
    progress_data = get_user_progress(user)
    return render_template('progress.html', progress=progress_data, belts=BELT_LEVELS)

# ============ API ROUTES ============
@app.route('/api/technique/complete/<int:technique_id>', methods=['POST'])
def complete_technique(technique_id):
    try:
        user = get_or_create_user()
        existing = CompletedTechnique.query.filter_by(user_id=user.id, technique_id=technique_id).first()
        
        if not existing:
            completed = CompletedTechnique(user_id=user.id, technique_id=technique_id)
            user.total_points += 50
            db.session.add(completed)
            db.session.commit()
            return jsonify({'success': True, 'points_earned': 50, 'total_points': user.total_points})
        
        return jsonify({'success': False, 'message': 'Already completed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/drill/complete/<int:drill_id>', methods=['POST'])
def complete_drill(drill_id):
    try:
        user = get_or_create_user()
        existing = CompletedDrill.query.filter_by(user_id=user.id, drill_id=drill_id).first()
        
        if not existing:
            completed = CompletedDrill(user_id=user.id, drill_id=drill_id)
            user.total_points += 100
            db.session.add(completed)
            db.session.commit()
            return jsonify({'success': True, 'points_earned': 100, 'total_points': user.total_points})
        
        return jsonify({'success': False, 'message': 'Already completed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/progress')
def api_progress():
    user = get_or_create_user()
    return jsonify(get_user_progress(user))

# ============ ERROR HANDLERS ============
@app.errorhandler(404)
def not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# ============ INITIALIZATION & STARTUP ============
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
