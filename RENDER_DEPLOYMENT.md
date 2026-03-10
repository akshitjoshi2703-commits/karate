# Karate Learning App - Python Flask - Render Deployment

This is a **Python Flask** karate learning application configured for deployment on [Render](https://render.com/).

## Quick Start Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Visit http://localhost:5000
```

## Deployment on Render

### Step 1: Push to GitHub

```bash
# Initialize git
git init
git add .
git commit -m "Initial karate app with Python Flask"

# Create a new repository on GitHub (https://github.com/new)
# Then run:
git remote add origin https://github.com/YOUR_USERNAME/karate-learning-app.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to [render.com](https://render.com)
2. Sign in or create an account
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub account and select your repository
5. Configure the following settings:
   - **Name**: `karate-learning-app` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (recommended to start)
6. Click **"Create Web Service"**

### Step 3: Environment Variables (Optional)

In the Render dashboard:
1. Go to your service
2. Click "Environment"
3. Add these variables if needed:
   - `SECRET_KEY`: Your secret key for production
   - `DATABASE_URL`: PostgreSQL connection string (auto-provided if using Render PostgreSQL)

### Step 4: Monitor Deployment

- Render will automatically build and deploy your app
- View logs in the Render dashboard
- Your app will be live at: `https://your-app-name.onrender.com`

## Features

✅ Technique Library with 6+ karate techniques
✅ Interactive Drills with timer functionality
✅ Video Tutorials from expert instructors
✅ Progress Tracking with belt levels (White to Black)
✅ User sessions with SQLite database (auto-upgrades to PostgreSQL on Render)
✅ Responsive design for mobile and desktop

## Database

- **Local**: SQLite (`karate.db`)
- **Production (Render)**: PostgreSQL (recommended)

When deploying to Render, you can attach a PostgreSQL database:
1. In Render dashboard, create a new PostgreSQL database
2. Copy the connection URL
3. Add it as the `DATABASE_URL` environment variable
4. Update the database URI in `app.py` to use it

## Auto-deployment

- Every push to your `main` branch triggers automatic deployment
- Manual deployments available from the Render dashboard

## Troubleshooting

- **App spins down**: Free tier spins down after 15 minutes of inactivity (upgrade to paid for always-on)
- **Database errors**: Ensure `DATABASE_URL` is set correctly
- **Port issues**: Render automatically assigns port 5000

## Production Tips

- Change `SECRET_KEY` to a secure random value
- Use PostgreSQL instead of SQLite
- Enable HTTPS (automatic on Render)
- Monitor app logs regularly
