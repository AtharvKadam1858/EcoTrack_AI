# EcoTrack AI — Predictive Carbon Intelligence Platform
### Hack For Green Bharat 2026 | Team AtharvKadam1858

🌐 **Live Demo:** https://x9ktxp.vercel.app  
🐙 **GitHub:** https://github.com/AtharvKadam1858/ecotrack-ai_HACK_FOR_GREEN_BHARAT

---

## 🚀 Deploy to Render (Step-by-Step)

### Step 1 — Push to GitHub
```bash
cd ecotrack
git init
git add .
git commit -m "EcoTrack AI - Predictive Carbon Intelligence Platform"
git remote add origin https://github.com/YOUR_USERNAME/ecotrack-ai.git
git push -u origin main
```

### Step 2 — Deploy on Render
1. Go to **https://render.com** → Sign up / Log in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account → Select your repo
4. Fill in these settings:
   - **Name:** `ecotrack-ai`
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free

### Step 3 — Add Environment Variable
In Render dashboard → Your Service → **Environment** tab:
- Click **"Add Environment Variable"**
- Key: `ANTHROPIC_API_KEY`
- Value: `your-anthropic-api-key-here`

> Get your API key from: https://console.anthropic.com

### Step 4 — Deploy!
Click **"Create Web Service"** → Render will build and deploy automatically.
Your URL will be: `https://ecotrack-ai.onrender.com`

---

## 🏗️ Project Structure
```
ecotrack/
├── app.py              # Flask backend + API routes
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment config
├── .gitignore
├── README.md
└── templates/
    └── index.html      # Complete frontend (all 4 pages)
```

## 📡 API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main website |
| `/api/calculate` | POST | Calculate carbon footprint & green score |
| `/api/ai-insights` | POST | Get AI-powered sustainability insights |
| `/api/health` | GET | Health check |

## 🔧 Local Development
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here
python app.py
# Visit http://localhost:5000
```

## 🌿 Features
- ⚡ Carbon footprint prediction using BEE India emission factors
- 📊 Interactive resource trend charts (energy, water, paper)
- 🤖 AI-powered insights via Claude API
- 🏆 Green Score calculation with industry benchmarks
- ⚠️ Anomaly detection for unusual usage spikes
- 📋 Monthly data history with comparison
- 📱 Fully responsive design

## 🎯 UN SDG Alignment
- SDG 7 — Affordable & Clean Energy
- SDG 12 — Responsible Consumption & Production
- SDG 13 — Climate Action

---
Built with ❤️ for Hack For Green Bharat 2026
