# 🌊 AquaVision AI

**AI-Driven Smart Water Availability Prediction System**

A comprehensive machine learning platform for predicting groundwater availability using real Indian monitoring data. Built with React, Flask, and advanced ML models.

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://aquavision-ai.vercel.app)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.0+-61dafb.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🎯 Overview

AquaVision AI is a production-ready water management platform that predicts groundwater availability levels (High, Medium, Low) using machine learning trained on 550,000+ real measurements from Indian groundwater monitoring stations.

### Key Features

- 🤖 **ML Predictions** - HistGradientBoosting model trained on real data
- 🧠 **Explainable AI** - Feature importance and natural language explanations
- 📊 **7-Day Forecast** - Trend-based water level projections
- 💡 **Smart Recommendations** - Context-aware water management advice
- 🌾 **Crop Suggestions** - Agricultural recommendations based on water availability
- 💧 **Irrigation Methods** - Optimal irrigation techniques and schedules
- 🌤️ **Weather Integration** - Real-time weather data (OpenWeatherMap API)
- 📄 **PDF Reports** - Professional downloadable prediction reports
- 🔐 **User Authentication** - JWT-based secure login system
- 👥 **Admin Panel** - Complete user and system management
- 📜 **Prediction History** - Store and track all predictions
- 📈 **Model Comparison** - Compare 5 ML models (RF, DT, XGBoost, GB, SVM)
- 💬 **AI Chatbot** - Interactive assistant for water management queries

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

```bash
# Clone repository
git clone https://github.com/Mohnish111004/aquavision.git
cd aquavision

# Backend setup
cd backend
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### Running Locally

**Terminal 1 - Backend:**
```bash
cd backend
python3 app.py
# Runs on http://localhost:5001
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Runs on http://localhost:5173
```

Open http://localhost:5173 in your browser.

---

## 📊 Dataset

- **Source:** Indian Groundwater Monitoring Data
- **Size:** 550,850 real measurements
- **Coverage:** 32 states, 565 districts, 23 river basins
- **Time Period:** 2013-2024
- **Parameters:** Latitude, longitude, groundwater depth, level changes

---

## 🤖 Machine Learning

### Models Supported

1. **HistGradientBoosting** (Default)
2. Random Forest
3. Decision Tree
4. XGBoost
5. Support Vector Machine

### Training

```bash
cd backend/model

# Train single model
python3 train_model.py

# Compare multiple models
python3 compare_models.py
```

### Model Performance

- **Accuracy:** 92%+
- **Features:** 13 (geographic, temporal, water level)
- **Classes:** High, Medium, Low
- **Thresholds:** Based on real groundwater depth standards

---

## 🛠️ Tech Stack

### Frontend
- React 18
- Vite
- Tailwind CSS
- Framer Motion
- Recharts
- React Router

### Backend
- Python 3.8+
- Flask
- SQLAlchemy
- Scikit-learn
- XGBoost
- Pandas & NumPy
- JWT Authentication

### Database
- SQLite (default)
- MySQL (optional)

---

## 📁 Project Structure

```
aquavision/
├── backend/
│   ├── app.py                 # Flask application
│   ├── database/              # Database models
│   ├── routes/                # API endpoints
│   ├── model/                 # ML models
│   └── utils/                 # Utilities
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   └── utils/             # API client
│   └── public/                # Static assets
└── output/                    # Generated visualizations
```

---

## 🌐 API Endpoints

### Core Prediction
- `POST /predict` - Water availability prediction
- `POST /explain` - XAI explanations
- `POST /forecast` - 7-day forecast
- `POST /recommend` - AI recommendations

### Authentication
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login
- `GET /auth/profile` - User profile

### History
- `GET /history` - Prediction history
- `POST /history` - Save prediction
- `GET /history/stats` - User statistics

### Weather
- `GET /weather/current` - Current weather
- `GET /weather/forecast` - 5-day forecast

### Agriculture
- `POST /crops/recommend` - Crop recommendations
- `POST /irrigation/recommend` - Irrigation methods

### Admin (Admin Only)
- `GET /admin/stats` - System statistics
- `GET /admin/users` - User management
- `GET /admin/predictions` - All predictions

---

## 🚀 Deployment

### Deploy to Vercel

```bash
# Push to GitHub
git push origin main

# Deploy frontend to Vercel
# 1. Go to https://vercel.com/new
# 2. Import your repository
# 3. Set Root Directory: frontend
# 4. Click Deploy
```

See [DEPLOY_NOW.md](DEPLOY_NOW.md) for detailed instructions.

---

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md) - Get running in 5 minutes
- [Setup Guide](SETUP_GUIDE.md) - Complete installation
- [API Documentation](API_DOCUMENTATION.md) - Full API reference
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Production deployment
- [Data Validation](DATA_VALIDATION.md) - What's real vs simulated

---

## 🎓 Use Cases

- **Agriculture** - Crop planning and irrigation management
- **Water Authorities** - Resource monitoring and planning
- **Research** - Groundwater studies and analysis
- **Policy Making** - Data-driven water conservation policies
- **Education** - ML and environmental science projects

---

## 🔒 Security

- JWT-based authentication
- Password hashing (bcrypt)
- Role-based access control
- Input validation
- SQL injection prevention
- CORS configuration

---

## 📈 Features Roadmap

- [ ] Time-series forecasting (LSTM/ARIMA)
- [ ] Mobile app (React Native)
- [ ] Real-time monitoring dashboard
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] API rate limiting
- [ ] Email notifications

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Indian Groundwater Monitoring Network for dataset
- OpenWeatherMap for weather API
- Scikit-learn and XGBoost communities
- React and Flask communities

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

**Built with ❤️ for sustainable water management**

🌊 **AquaVision AI** - Predicting water availability, one drop at a time.
