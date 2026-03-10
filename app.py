import os
from flask import Flask, render_template, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import cv2
import mediapipe as mp
import numpy as np
import base64
from PIL import Image
import io

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
        'id': 1, 'name': 'Jab Punch (Jun Zuki)', 'category': 'Striking', 'difficulty': 'Beginner',
        'description': 'The jab is the fastest punch in karate, used for speed, range-finding, and setting up combinations.',
        'steps': [
            'Start in natural stance with feet shoulder-width apart',
            'Keep your left hand (for right-handed) as the jab hand',
            'Rotate your fist so knuckles face up, thumb on top',
            'Extend your arm straight forward while rotating your hips slightly',
            'Keep your elbow slightly bent (not locked) to maintain speed',
            'Retract immediately and return to guard position',
            'Keep your right hand protecting your chin'
        ],
        'common_mistakes': [
            'Dropping your guard hand',
            'Not rotating hips',
            'Locking elbow straight',
            'Not retracting fast enough'
        ],
        'tips': [
            'Think of it as "poking" rather than "punching"',
            'Keep your chin tucked behind your shoulder',
            'Breathe out as you punch',
            'Practice speed over power initially'
        ],
        'benefits': ['Speed development', 'Range control', 'Combination setup']
    },
    {
        'id': 2, 'name': 'Cross Punch (Gyaku Zuki)', 'category': 'Striking', 'difficulty': 'Beginner',
        'description': 'The cross punch generates maximum power by utilizing full body rotation and weight transfer.',
        'steps': [
            'Start with lead foot forward, rear foot at 45-degree angle',
            'Keep your rear hand (right for orthodox) as the power hand',
            'Load your rear leg by bending it slightly',
            'Rotate your rear foot, hips, and shoulders simultaneously',
            'Drive your fist straight forward, palm facing down',
            'Transfer your weight from rear to front foot',
            'Keep your lead hand up for protection'
        ],
        'common_mistakes': [
            'Not rotating hips fully',
            'Leaning forward instead of rotating',
            'Dropping lead hand',
            'Not transferring weight'
        ],
        'tips': [
            'Imagine twisting a towel to wring water out',
            'Keep your eyes on the target throughout',
            'Power comes from rotation, not just arm strength',
            'Practice with slow motion first'
        ],
        'benefits': ['Power generation', 'Body coordination', 'Weight transfer']
    },
    {
        'id': 3, 'name': 'Front Kick (Mae Geri)', 'category': 'Striking', 'difficulty': 'Beginner',
        'description': 'A linear kick that uses the ball of the foot to strike, excellent for close-range attacks.',
        'steps': [
            'Start in fighting stance with knees slightly bent',
            'Chamber your knee up to waist height',
            'Keep your supporting leg bent for stability',
            'Extend your leg straight forward using hip flexors',
            'Strike with the ball of your foot (not toes)',
            'Keep your body upright, don't lean back',
            'Retract quickly and return to stance'
        ],
        'common_mistakes': [
            'Kicking with toes instead of ball of foot',
            'Leaning backward',
            'Not chambering knee high enough',
            'Locking supporting leg straight'
        ],
        'tips': [
            'Think of pushing through a wall with your foot',
            'Keep your core tight throughout',
            'Practice balance on supporting leg',
            'Start slow, focus on form'
        ],
        'benefits': ['Hip flexor strength', 'Balance', 'Linear power']
    },
    {
        'id': 4, 'name': 'Roundhouse Kick (Mawashi Geri)', 'category': 'Striking', 'difficulty': 'Intermediate',
        'description': 'A powerful circular kick using the shin, excellent for generating momentum and power.',
        'steps': [
            'Start in fighting stance',
            'Chamber your knee across your body to opposite shoulder',
            'Rotate your supporting foot and hips toward the target',
            'Swing your leg in a circular motion',
            'Strike with your shin (not instep)',
            'Keep your body upright and core engaged',
            'Chamber leg and return to stance'
        ],
        'common_mistakes': [
            'Not rotating hips',
            'Leaning away from the kick',
            'Striking with instep instead of shin',
            'Not chambering knee properly'
        ],
        'tips': [
            'Imagine your leg is a whip',
            'Keep your eyes on the target',
            'Practice the motion slowly first',
            'Build up speed gradually'
        ],
        'benefits': ['Hip mobility', 'Circular power', 'Coordination']
    },
    {
        'id': 5, 'name': 'Side Kick (Yoko Geri)', 'category': 'Striking', 'difficulty': 'Intermediate',
        'description': 'A devastating linear kick delivered to the side, using the heel or edge of the foot.',
        'steps': [
            'Turn sideways to the target, lead foot pointing toward it',
            'Chamber your knee up and across your body',
            'Keep your supporting leg straight and strong',
            'Extend your leg straight out to the side',
            'Strike with the heel or edge of your foot',
            'Keep your body upright, don't lean',
            'Retract and return to stance'
        ],
        'common_mistakes': [
            'Not turning sideways enough',
            'Leaning backward',
            'Chambering knee too low',
            'Not keeping supporting leg straight'
        ],
        'tips': [
            'Think of pushing a door open with your foot',
            'Keep your core tight',
            'Practice balance extensively',
            'Start with slow, controlled motions'
        ],
        'benefits': ['Lateral power', 'Balance', 'Hip strength']
    },
    {
        'id': 6, 'name': 'Horse Stance (Kiba Dachi)', 'category': 'Stance', 'difficulty': 'Beginner',
        'description': 'A wide, stable stance that builds leg strength and teaches proper weight distribution.',
        'steps': [
            'Stand with feet about 2-3 shoulder widths apart',
            'Turn toes slightly outward (about 45 degrees)',
            'Bend knees until thighs are parallel to ground',
            'Keep back straight and upright',
            'Distribute weight evenly between both legs',
            'Keep arms relaxed at sides or in guard position',
            'Hold position while maintaining steady breathing'
        ],
        'common_mistakes': [
            'Feet too narrow',
            'Knees not bent enough',
            'Leaning forward or backward',
            'Raising shoulders'
        ],
        'tips': [
            'Imagine sitting back into a chair',
            'Keep your weight in your heels',
            'Breathe steadily and deeply',
            'Start with shorter holds and build up'
        ],
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

# ============ COMPUTER VISION FUNCTIONS ============
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def calculate_angle(a, b, c):
    """Calculate angle between three points"""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

def analyze_horse_stance(landmarks):
    """Analyze horse stance posture"""
    feedback = []
    score = 0

    # Get key points
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                 landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                  landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
    left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
    right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

    # Check knee bend (should be ~90 degrees for horse stance)
    left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
    right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)

    if 80 <= left_knee_angle <= 100:
        feedback.append("✅ Left knee bend is good")
        score += 25
    else:
        feedback.append(f"❌ Left knee angle: {left_knee_angle:.1f}° (should be ~90°)")

    if 80 <= right_knee_angle <= 100:
        feedback.append("✅ Right knee bend is good")
        score += 25
    else:
        feedback.append(f"❌ Right knee angle: {right_knee_angle:.1f}° (should be ~90°)")

    # Check stance width (feet should be wide apart)
    foot_distance = abs(left_ankle[0] - right_ankle[0])
    if foot_distance > 0.3:  # Relative to image width
        feedback.append("✅ Stance width is good")
        score += 25
    else:
        feedback.append("❌ Feet should be wider apart")

    # Check upright posture
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

    shoulder_level = abs(left_shoulder[1] - right_shoulder[1])
    if shoulder_level < 0.05:
        feedback.append("✅ Shoulders are level")
        score += 25
    else:
        feedback.append("❌ Keep shoulders level")

    return score, feedback

def analyze_fighting_stance(landmarks):
    """Analyze fighting stance posture"""
    feedback = []
    score = 0

    # Get key points
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                 landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                  landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

    # Check if in staggered stance (one foot forward)
    foot_distance = abs(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x -
                       landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x)

    if foot_distance > 0.2:
        feedback.append("✅ Good staggered stance")
        score += 30
    else:
        feedback.append("❌ Step one foot forward")

    # Check knee bend
    left_knee_angle = calculate_angle(left_hip, left_knee,
                                    [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y])
    right_knee_angle = calculate_angle(right_hip, right_knee,
                                     [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y])

    if 160 <= left_knee_angle <= 180 or 160 <= right_knee_angle <= 180:
        feedback.append("✅ Knees are straight")
        score += 35
    else:
        feedback.append("❌ Keep knees slightly bent")

    # Check hands up
    nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,
            landmarks[mp_pose.PoseLandmark.NOSE.value].y]
    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

    if left_wrist[1] < nose[1] and right_wrist[1] < nose[1]:
        feedback.append("✅ Hands are up protecting face")
        score += 35
    else:
        feedback.append("❌ Keep hands up to protect your face")

    return score, feedback

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

@app.route('/stance-check')
def stance_check():
    return render_template('stance_check.html')

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

@app.route('/api/analyze-stance', methods=['POST'])
def analyze_stance():
    try:
        data = request.get_json()
        image_data = data.get('image')
        stance_type = data.get('stance_type', 'horse')  # 'horse' or 'fighting'

        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400

        # Decode base64 image
        image_data = image_data.split(',')[1]  # Remove data:image/jpeg;base64, prefix
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))

        # Convert to OpenCV format
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Process with MediaPipe
        results = pose.process(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))

        if not results.pose_landmarks:
            return jsonify({
                'score': 0,
                'feedback': ['❌ No person detected. Please stand in frame.'],
                'stance_type': stance_type
            })

        # Analyze stance based on type
        if stance_type == 'horse':
            score, feedback = analyze_horse_stance(results.pose_landmarks.landmark)
        elif stance_type == 'fighting':
            score, feedback = analyze_fighting_stance(results.pose_landmarks.landmark)
        else:
            return jsonify({'error': 'Invalid stance type'}), 400

        return jsonify({
            'score': score,
            'feedback': feedback,
            'stance_type': stance_type,
            'success': True
        })

    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

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
