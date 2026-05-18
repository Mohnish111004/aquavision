# AquaVision AI – Requirements

## Introduction
AquaVision AI is a full-stack web application that predicts future water availability (High / Medium / Low) using a trained Machine Learning model. It serves farmers, communities, and local authorities who need reliable water availability estimates for irrigation planning, storage, and resource management.

The ML model and Flask backend already exist. This spec covers building the complete React frontend, restructuring the backend, and wiring everything together into a production-ready system.

---

## Requirements

### REQ-1: Project Structure
The project must be reorganised into a clean monorepo layout:
```
aquavision/
├── backend/
│   ├── app.py
│   ├── routes/
│   ├── model/
│   │   ├── train_model.py
│   │   ├── preprocess.py
│   │   └── aquavision_model.joblib
│   ├── static/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── App.jsx
│   ├── package.json
│   └── tailwind.config.js
├── README.md
└── .gitignore
```

**Acceptance Criteria:**
- All backend files live under `backend/`
- All frontend files live under `frontend/`
- Model file is referenced correctly from the new path
- README documents the full setup

---

### REQ-2: Backend API
The Flask backend must expose three REST endpoints.

**Acceptance Criteria:**
- `POST /predict` — accepts JSON with fields: `latitude`, `longitude`, `currentlevel`, `level_diff`, `date`, `state_name`, `district_name`, `basin`, `sub_basin`, `station_name`; returns `prediction`, `confidence`, `current_status`, `probabilities`
- `GET /health` — returns `{ "status": "ok", "model_loaded": true/false }`
- `GET /metrics` — returns model accuracy, model name, training date, dataset rows, class names
- CORS must be enabled for the React dev server (`http://localhost:5173`)
- All endpoints return JSON; errors return appropriate HTTP status codes with a message field
- Input validation rejects missing or malformed fields with HTTP 422

---

### REQ-3: ML Model Integration
The existing trained model (`aquavision_model.joblib`) must be loaded and served by the backend.

**Acceptance Criteria:**
- Model loads at startup; if missing, `/predict` returns HTTP 503 with a clear error
- Prediction uses the 13 features already defined in `train.py`
- Class labels returned are human-readable strings: `"High"`, `"Medium"`, `"Low"`
- Confidence score is returned as a percentage (0–100)
- Probability breakdown for all three classes is included in the response

---

### REQ-4: React Frontend – General
The frontend is a single-page React application using React Router for navigation.

**Acceptance Criteria:**
- Built with React 18 + Vite
- Styled with Tailwind CSS
- Animations via Framer Motion
- Charts via Recharts
- HTTP calls via Axios
- Dark/Light mode toggle persisted in localStorage
- Fully responsive: mobile (≥320px), tablet (≥768px), desktop (≥1024px)
- Toast notifications for success/error states

---

### REQ-5: Landing Page
**Acceptance Criteria:**
- Hero section with project name, tagline, and animated water background
- "Start Prediction" CTA button navigates to the Prediction Dashboard
- Statistics cards showing: dataset size, model accuracy, prediction classes, states covered
- Brief project overview section
- Footer with team name and links

---

### REQ-6: Prediction Dashboard
**Acceptance Criteria:**
- Form with labelled inputs: Rainfall (currentlevel), Temperature proxy (level_diff), Latitude, Longitude, Date, State, District, Basin, Sub-basin, Station
- Client-side validation: all fields required, numeric fields must be valid numbers
- On submit: shows loading spinner, calls `POST /predict`, displays result
- Result card colour-coded: High → green, Medium → yellow/amber, Low → red
- Result card shows: predicted class, confidence %, current status, probability bar chart
- Prediction is appended to a local history table (stored in sessionStorage)
- "Download Report" button exports the prediction result as a PDF

---

### REQ-7: Analytics Page
**Acceptance Criteria:**
- Displays model accuracy comparison bar chart (RF vs HGB) using static data from `/metrics`
- Feature importance horizontal bar chart
- Confusion matrix heatmap (rendered from static image or Recharts)
- Pie chart showing distribution of prediction classes from history
- Dataset insights cards: total rows, features used, training date

---

### REQ-8: About Page
**Acceptance Criteria:**
- Problem statement section
- Solution overview section
- Tech stack cards (Frontend, Backend, ML)
- Model performance summary

---

### REQ-9: Team Section
**Acceptance Criteria:**
- Team member cards with name, role, and avatar placeholder
- Project timeline / milestones

---

### REQ-10: Contact Page
**Acceptance Criteria:**
- Contact form with name, email, message fields
- Client-side validation
- On submit: shows success toast (no backend required for contact)

---

### REQ-11: Navigation
**Acceptance Criteria:**
- Sticky top navbar with links: Home, Predict, Analytics, About, Team, Contact
- Active link highlighted
- Mobile hamburger menu
- Dark/Light toggle in navbar

---

### REQ-12: Deployment Readiness
**Acceptance Criteria:**
- `backend/requirements.txt` lists all Python dependencies with pinned versions
- `frontend/package.json` lists all JS dependencies
- `README.md` contains: project overview, installation steps, model training steps, API usage, deployment instructions for Render (backend) and Vercel (frontend)
- `.gitignore` excludes: `__pycache__`, `*.joblib`, `node_modules`, `.env`, `dist`, `venv`
- `.env.example` documents required environment variables

---

### REQ-13: Water Conservation Tips (Bonus)
**Acceptance Criteria:**
- A tips section on the Landing Page or a dedicated sidebar on the Prediction Dashboard
- At least 6 actionable water conservation tips displayed as cards

---

### REQ-14: Future Trend Graph (Bonus)
**Acceptance Criteria:**
- On the Analytics page, a line chart showing a simulated 12-month water availability trend
- Uses the last prediction result to seed the trend if available
