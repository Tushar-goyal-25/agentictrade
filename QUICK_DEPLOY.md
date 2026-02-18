# Quick Deploy Instructions

## Fastest Way to Deploy

### 1. Deploy Frontend Only (No Backend)

```bash
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

You'll get a URL instantly!

### 2. Deploy with Backend (Full Setup)

**A. Push to GitHub first:**
```bash
git add .
git commit -m "Ready for deployment"
git push origin master
```

**B. Deploy Frontend (Vercel):**
1. Go to https://vercel.com
2. New Project → Import from GitHub
3. Root Directory: `frontend`
4. Deploy

**C. Deploy Backend (Railway):**
1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Select your repo
4. Settings → Root Directory: `api`
5. Add Postgres database (click "New" → PostgreSQL)
6. Deploy

**D. Connect them:**
- Get backend URL from Railway
- Update Vercel env var: `NEXT_PUBLIC_API_URL=<backend-url>`
- Redeploy

## Environment Variables Needed

**Vercel (Frontend):**
```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

**Railway (Backend):**
```
DATABASE_URL=<auto-provided-by-railway>
```

## Sharing Your Demo

Once deployed, share:
```
https://agentic-trade.vercel.app
```

People can:
- Select strategies
- Pick stocks
- Run backtests
- See beautiful results!
