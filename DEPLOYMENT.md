# Agentic Trading System - Deployment Guide

## 🚀 Quick Start

This guide will help you deploy your trading system with a Next.js frontend and Flask backend.

## 📁 Project Structure

```
agentictrade/
├── frontend/          # Next.js frontend
├── api/              # Flask backend API
├── data/             # Trading strategies
├── backtest.py       # Backtesting engine
└── ingest/           # Data fetching & metrics
```

---

## 🖥️ Local Development

### 1. Backend Setup (Flask API)

```bash
# Install Python dependencies
pip install -r api/requirements.txt

# Start Flask server
cd api
python app.py

# API will run on http://localhost:5000
```

### 2. Frontend Setup (Next.js)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Frontend will run on http://localhost:3000
```

### 3. Database Setup

Make sure PostgreSQL with TimescaleDB is running:

```bash
# Start PostgreSQL (if not already running)
brew services start postgresql

# Your connection string in dataLodaer.py:
# postgresql://postgres:postgres@localhost:5432/postgres
```

---

## 🌐 Production Deployment

### Option 1: Vercel (Frontend) + Railway/Render (Backend)

#### Deploy Frontend to Vercel

1. **Push code to GitHub**:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Select `/frontend` as root directory
   - Click "Deploy"

3. **Configure environment variables in Vercel**:
   - Go to Project Settings → Environment Variables
   - Add: `NEXT_PUBLIC_API_URL` = `<your-backend-url>`

#### Deploy Backend to Railway

1. **Go to [railway.app](https://railway.app)**

2. **Create New Project**:
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

3. **Configure Backend**:
   - Set root directory to `/api`
   - Add environment variables:
     ```
     DATABASE_URL=<your-postgres-connection-string>
     FLASK_ENV=production
     ```

4. **Add Procfile** (create `/api/Procfile`):
   ```
   web: gunicorn app:app
   ```

5. **Update requirements.txt** to include:
   ```
   gunicorn==21.2.0
   ```

6. **Deploy** - Railway will auto-deploy

7. **Get Backend URL** from Railway dashboard

#### Alternative: Deploy Backend to Render

1. Go to [render.com](https://render.com)
2. New → Web Service
3. Connect GitHub repository
4. Configure:
   - **Root Directory**: `api`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add environment variables
6. Deploy

---

### Option 2: All-in-One Vercel Deployment

Vercel can also host your Flask API as serverless functions.

#### 1. Create API Route in Frontend

Create `/frontend/app/api/[...path]/route.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const body = await request.json();

  // Call your Python backend or implement logic here
  const response = await fetch('http://your-backend-url/api/backtest', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });

  const data = await response.json();
  return NextResponse.json(data);
}
```

#### 2. Deploy

```bash
cd frontend
vercel --prod
```

---

## 🔧 Configuration

### Update API URL in Frontend

Edit `/frontend/components/BacktestForm.tsx` line 51:

```typescript
// Development
const response = await fetch('http://localhost:5000/api/backtest', {

// Production
const response = await fetch(process.env.NEXT_PUBLIC_API_URL + '/api/backtest', {
```

### Database for Production

You'll need a hosted PostgreSQL database:

**Options**:
1. **Neon** (neon.tech) - Free tier, serverless Postgres
2. **Railway** - Includes Postgres
3. **Supabase** - Free tier with Postgres
4. **AWS RDS** - Production-grade

Update connection string in `data/dataLodaer.py`:

```python
pool = await asyncpg.create_pool(os.getenv('DATABASE_URL'))
```

---

## 📊 Testing the Deployment

1. **Frontend**: Visit your Vercel URL (e.g., `https://your-app.vercel.app`)

2. **Backend Health Check**:
   ```bash
   curl https://your-backend-url/api/health
   ```

3. **Run a Backtest**:
   - Select a strategy (e.g., Momentum)
   - Choose stocks (e.g., AAPL, TSLA, NVDA)
   - Click "Run Backtest"
   - View results with charts and metrics

---

## 🐛 Troubleshooting

### CORS Errors
Add to `/api/app.py`:
```python
CORS(app, origins=['https://your-frontend-url.vercel.app'])
```

### Database Connection Issues
- Check DATABASE_URL environment variable
- Ensure database is publicly accessible
- Verify connection string format

### Frontend Build Errors
```bash
cd frontend
npm run build  # Test build locally first
```

### Backend Import Errors
Ensure all paths are correct in production:
```python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

---

## 📈 Next Steps

1. **Add Authentication** - Protect your API with JWT or OAuth
2. **Caching** - Cache backtest results to reduce database load
3. **Rate Limiting** - Prevent abuse of your API
4. **Monitoring** - Add Sentry or LogRocket
5. **Analytics** - Track usage with Vercel Analytics

---

## 🎉 You're Done!

Your trading system is now live and ready to demo! Share your Vercel URL with others.

**Example URL**: `https://agentic-trade.vercel.app`

---

## 📞 Support

- Frontend: [Next.js Docs](https://nextjs.org/docs)
- Backend: [Flask Docs](https://flask.palletsprojects.com/)
- Deployment: [Vercel Docs](https://vercel.com/docs)
