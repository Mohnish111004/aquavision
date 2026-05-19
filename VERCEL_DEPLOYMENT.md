# 🚀 Vercel Deployment Guide - Frontend + Backend

## ⚠️ Important: Backend Deployment

Vercel's free tier has **limited Python support** for Flask apps. The best approach is:

**Frontend → Vercel (Free)**  
**Backend → Render.com (Free)**

This gives you a fully working application with a single URL.

---

## 📦 Option 1: Full Stack Deployment (Recommended)

### Step 1: Deploy Backend to Render.com

1. **Go to:** https://render.com
2. **Sign up** with GitHub
3. Click **"New +"** → **"Web Service"**
4. **Connect** your GitHub repository: `Mohnish111004/aquavision`
5. **Configure:**
   ```
   Name: aquavision-backend
   Region: Choose closest to you
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
   ```

6. **Environment Variables:**
   ```
   DATABASE_URL=sqlite:///aquavision.db
   SECRET_KEY=your-secret-key-change-this
   JWT_SECRET_KEY=your-jwt-secret-change-this
   FLASK_ENV=production
   ```

7. Click **"Create Web Service"**

8. **Wait 3-5 minutes** for deployment

9. **Copy your backend URL:** `https://aquavision-backend.onrender.com`

### Step 2: Deploy Frontend to Vercel

1. **Go to:** https://vercel.com/new

2. **Import** your repository: `Mohnish111004/aquavision`

3. **Configure:**
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

4. **Environment Variables:**
   ```
   VITE_API_URL=https://aquavision-backend.onrender.com
   ```

5. Click **"Deploy"**

6. **Wait 2-3 minutes**

7. **Your app is live!** 🎉

### Step 3: Update CORS in Backend

After deployment, update `backend/app.py`:

```python
CORS(app, origins=[
    "https://your-vercel-url.vercel.app",
    "http://localhost:5173",
    "*"
])
```

Commit and push:
```bash
git add backend/app.py
git commit -m "Update CORS for production"
git push origin main
```

Render will auto-deploy the update.

---

## 📦 Option 2: Frontend Only (Demo Mode)

If you just want to deploy the frontend for portfolio/demo:

1. **Go to:** https://vercel.com/new

2. **Import** repository

3. **Configure:**
   ```
   Root Directory: frontend
   Framework: Vite
   ```

4. **Deploy**

5. **Note:** Backend features won't work, but the UI will be visible.

---

## 🔧 Option 3: Railway.app (Alternative)

Railway.app also offers free hosting:

1. Go to: https://railway.app
2. Sign up with GitHub
3. New Project → Deploy from GitHub
4. Select your repository
5. Add both services:
   - **Backend:** Root = `backend`, Start = `gunicorn app:app`
   - **Frontend:** Root = `frontend`, Build = `npm run build`

---

## ✅ Verify Deployment

### Test Backend:
```bash
curl https://aquavision-backend.onrender.com/health
```

Should return:
```json
{"status": "healthy", "timestamp": "..."}
```

### Test Frontend:
Visit your Vercel URL and try making a prediction.

---

## 🐛 Troubleshooting

### Backend Issues:

**Problem:** Backend not responding
- Check Render logs: Dashboard → Logs
- Verify environment variables are set
- Check if service is running

**Problem:** CORS errors
- Update CORS origins in `backend/app.py`
- Include your Vercel URL
- Redeploy backend

**Problem:** Database errors
- Render uses ephemeral storage
- For production, use PostgreSQL (Render offers free tier)

### Frontend Issues:

**Problem:** API calls failing
- Verify `VITE_API_URL` environment variable
- Check browser console for errors
- Test backend URL directly

**Problem:** Build fails
- Check Vercel build logs
- Verify all dependencies in `package.json`
- Check Node version compatibility

---

## 💰 Cost Breakdown

### Free Tier Limits:

**Vercel (Frontend):**
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Automatic HTTPS
- ✅ Global CDN

**Render (Backend):**
- ✅ 750 hours/month (enough for 1 service)
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ Cold start: 30-60 seconds
- ✅ Automatic HTTPS

**Total Cost:** $0/month 🎉

---

## 🚀 Production Upgrades

For a production app, consider:

1. **Render Paid Plan** ($7/month)
   - No sleep
   - Faster performance
   - More resources

2. **PostgreSQL Database**
   - Persistent storage
   - Better performance
   - Free tier available

3. **Custom Domain**
   - Buy from Namecheap/GoDaddy
   - Add to Vercel: Settings → Domains
   - Add to Render: Settings → Custom Domain

---

## 📝 Environment Variables Reference

### Backend (Render):
```env
DATABASE_URL=sqlite:///aquavision.db
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
FLASK_ENV=production
OPENWEATHER_API_KEY=your-api-key-optional
```

### Frontend (Vercel):
```env
VITE_API_URL=https://aquavision-backend.onrender.com
```

---

## 🔄 Continuous Deployment

Both platforms support auto-deployment:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```

2. **Automatic deployment:**
   - Vercel: Deploys frontend automatically
   - Render: Deploys backend automatically

3. **Wait 2-3 minutes**

4. **Changes are live!** 🎉

---

## 📱 Your Live URLs

After deployment:

- **Frontend:** `https://aquavision.vercel.app`
- **Backend:** `https://aquavision-backend.onrender.com`
- **Full App:** Use frontend URL (backend calls happen automatically)

---

## 🎯 Quick Deploy Checklist

- [ ] Push code to GitHub
- [ ] Deploy backend to Render
- [ ] Copy backend URL
- [ ] Deploy frontend to Vercel
- [ ] Add backend URL to Vercel env vars
- [ ] Update CORS in backend
- [ ] Test the application
- [ ] Share your link! 🎉

---

## 🆘 Need Help?

- **Render Docs:** https://render.com/docs
- **Vercel Docs:** https://vercel.com/docs
- **GitHub Issues:** Open an issue in your repository

---

**Deployment Time:** ~10 minutes  
**Cost:** $0 (Free tier)  
**Maintenance:** Auto-updates on git push

**Your app will be live and accessible worldwide!** 🌍🚀
