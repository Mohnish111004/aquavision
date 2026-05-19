# 🚀 AquaVision AI - Local Setup Guide

## Complete guide to clone and run on any computer

---

## 📋 Prerequisites

Before you start, make sure you have:

- ✅ **Python 3.8+** - [Download](https://www.python.org/downloads/)
- ✅ **Node.js 16+** - [Download](https://nodejs.org/)
- ✅ **Git** - [Download](https://git-scm.com/downloads/)
- ✅ **Terminal/Command Prompt** access

### Check if installed:

```bash
python3 --version   # Should show 3.8 or higher
node --version      # Should show 16 or higher
npm --version       # Should show 8 or higher
git --version       # Should show any version
```

---

## 🔽 Step 1: Clone the Repository

```bash
# Clone from GitHub
git clone https://github.com/Mohnish111004/aquavision.git

# Navigate to project folder
cd aquavision
```

---

## 🐍 Step 2: Setup Backend (Python/Flask)

### 2.1 Navigate to backend folder

```bash
cd backend
```

### 2.2 Create virtual environment (recommended)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 2.3 Install Python dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed flask-3.0.3 flask-cors-4.0.1 ...
```

### 2.4 Train the ML Model

⚠️ **Important:** The model file is not in GitHub (too large). You need to train it:

```bash
cd model
python3 train_model_simple.py
```

**This will:**
- Load the dataset (if you have it)
- Train the Random Forest model
- Save `aquavision_model.joblib`
- Takes 2-3 minutes

**Note:** If you don't have the dataset, download it separately or contact the repository owner.

### 2.5 Create environment file (optional)

```bash
cd ..  # Back to backend folder
cp .env.example .env
```

Edit `.env` if needed (optional for local development).

---

## ⚛️ Step 3: Setup Frontend (React/Vite)

### 3.1 Open a NEW terminal (keep backend terminal open)

### 3.2 Navigate to frontend folder

```bash
cd aquavision/frontend
```

### 3.3 Install Node dependencies

```bash
npm install
```

**Expected output:**
```
added 234 packages in 15s
```

**This will take 1-2 minutes.**

---

## 🚀 Step 4: Run the Application

### 4.1 Start Backend Server

**In Terminal 1 (backend folder):**

```bash
cd aquavision/backend
python3 app.py
```

**Expected output:**
```
✅ Model loaded: HistGradientBoosting
✅ Database initialized
✅ All routes registered
📍 Server running on http://localhost:5001
```

**Keep this terminal running!**

### 4.2 Start Frontend Server

**In Terminal 2 (frontend folder):**

```bash
cd aquavision/frontend
npm run dev
```

**Expected output:**
```
VITE v8.0.13  ready in 459 ms
➜  Local:   http://localhost:5173/
```

**Keep this terminal running too!**

---

## 🌐 Step 5: Access the Application

Open your browser and go to:

```
http://localhost:5173
```

**You should see the AquaVision AI dashboard!** 🎉

---

## 🧪 Step 6: Test the Application

1. **Navigate to "Predict Water Availability"**
2. **Fill in the form** with sample data:
   ```
   Latitude: 28.6139
   Longitude: 77.2090
   Current Level: 5.2
   Level Difference: -0.3
   Date: Today's date
   State: Delhi
   District: New Delhi
   Basin: Ganga
   Sub-Basin: Yamuna
   Station: CGWB-001
   ```
3. **Click "Predict"**
4. **View results** in 4 tabs (Result, AI Explain, Forecast, Actions)

---

## 📁 Project Structure

```
aquavision/
├── backend/                    # Python Flask backend
│   ├── app.py                 # Main Flask app
│   ├── requirements.txt       # Python dependencies
│   ├── model/                 # ML models
│   │   ├── train_model_simple.py
│   │   └── aquavision_model.joblib (you create this)
│   ├── routes/                # API endpoints
│   └── database/              # Database models
│
├── frontend/                   # React frontend
│   ├── package.json           # Node dependencies
│   ├── src/                   # Source code
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   └── utils/             # Utilities
│   └── public/                # Static assets
│
└── groundwater-DATASET.csv    # Dataset (not in GitHub)
```

---

## 🛑 Stopping the Application

**To stop the servers:**

1. **Backend:** Press `Ctrl+C` in Terminal 1
2. **Frontend:** Press `Ctrl+C` in Terminal 2

---

## 🐛 Troubleshooting

### Problem: "Module not found" errors

**Solution:**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Problem: "Model file not found"

**Solution:**
```bash
cd backend/model
python3 train_model_simple.py
```

### Problem: "Port already in use"

**Solution:**

**For port 5001 (backend):**
```bash
# macOS/Linux
lsof -ti:5001 | xargs kill -9

# Windows
netstat -ano | findstr :5001
taskkill /PID <PID> /F
```

**For port 5173 (frontend):**
```bash
# macOS/Linux
lsof -ti:5173 | xargs kill -9

# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

### Problem: "Cannot connect to backend"

**Solution:**
1. Check backend is running on port 5001
2. Check `frontend/vite.config.js` proxy settings
3. Restart both servers

### Problem: "Dataset not found"

**Solution:**
- The dataset is too large for GitHub
- Contact repository owner for dataset
- Or use your own groundwater dataset

### Problem: Python version issues

**Solution:**
```bash
# Use Python 3.8 or higher
python3 --version

# If too old, download from python.org
```

---

## 📦 What Gets Installed

### Backend Dependencies:
- Flask (web framework)
- Flask-CORS (cross-origin requests)
- Flask-SQLAlchemy (database)
- Scikit-learn (machine learning)
- Pandas, NumPy (data processing)
- JWT (authentication)
- And more... (see requirements.txt)

### Frontend Dependencies:
- React (UI framework)
- Vite (build tool)
- Tailwind CSS (styling)
- Framer Motion (animations)
- Recharts (charts)
- And more... (see package.json)

---

## 🔧 Development Tips

### Backend Development:

```bash
# Run with auto-reload
cd backend
python3 app.py
# Changes auto-reload in debug mode
```

### Frontend Development:

```bash
# Run dev server
cd frontend
npm run dev
# Changes auto-reload with hot module replacement
```

### Build for Production:

```bash
# Frontend
cd frontend
npm run build
# Creates optimized build in dist/
```

---

## 🌐 Environment Variables

### Backend (.env):
```env
DATABASE_URL=sqlite:///aquavision.db
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
OPENWEATHER_API_KEY=your-api-key-optional
```

### Frontend:
```env
VITE_API_URL=http://localhost:5001
```

---

## 📚 Additional Documentation

- **API Documentation:** See `API_DOCUMENTATION.md`
- **Deployment Guide:** See `VERCEL_DEPLOYMENT.md`
- **Quick Start:** See `QUICKSTART.md`
- **Data Validation:** See `DATA_VALIDATION.md`

---

## 🆘 Need Help?

1. **Check documentation** in the repository
2. **Read error messages** carefully
3. **Check if all dependencies installed**
4. **Verify Python and Node versions**
5. **Open an issue** on GitHub

---

## ✅ Quick Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] Git installed
- [ ] Repository cloned
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] ML model trained
- [ ] Backend server running (port 5001)
- [ ] Frontend server running (port 5173)
- [ ] Application accessible at http://localhost:5173
- [ ] Predictions working

---

## 🎯 Summary Commands

**Complete setup in one go:**

```bash
# Clone
git clone https://github.com/Mohnish111004/aquavision.git
cd aquavision

# Backend setup
cd backend
pip install -r requirements.txt
cd model
python3 train_model_simple.py
cd ..

# Frontend setup (in new terminal)
cd frontend
npm install

# Run backend (Terminal 1)
cd backend
python3 app.py

# Run frontend (Terminal 2)
cd frontend
npm run dev

# Open browser
# http://localhost:5173
```

---

## 🎉 Success!

If you see the AquaVision AI dashboard and can make predictions, you're all set!

**Estimated setup time:** 10-15 minutes

**Your local development environment is ready!** 🌊💧🚀

---

## 📝 Notes

- **Dataset:** Not included in GitHub (too large). Train model with your own data or contact owner.
- **Model file:** Generated when you run `train_model_simple.py`
- **Database:** Created automatically on first run (SQLite)
- **Ports:** Backend uses 5001, Frontend uses 5173
- **Auto-reload:** Both servers support hot reload during development

---

**Built with ❤️ for sustainable water management**
