# Deploy Backend to Railway - Step by Step

## 1. Go to Railway
**URL:** https://railway.app/new

## 2. Create New Project
- Click **"Deploy from GitHub repo"**
- Sign in with GitHub
- Select your **agentictrade** repository

## 3. Configure Service
After Railway creates the service:

### Set Root Directory:
1. Click on your service
2. Go to **Settings**
3. Find **"Root Directory"**
4. Enter: `api`
5. Click **"Update"**

### Verify Start Command:
- Should auto-detect from `railway.json`
- If not, manually set: `gunicorn app:app --bind 0.0.0.0:$PORT`

## 4. Add PostgreSQL Database
1. In your project, click **"+ New"**
2. Select **"Database"**
3. Choose **"Add PostgreSQL"**
4. Railway will automatically:
   - Create the database
   - Set `DATABASE_URL` environment variable
   - Link it to your service

## 5. Deploy
- Railway will automatically deploy
- Wait 2-3 minutes for build
- Check logs for any errors

## 6. Get Your Backend URL
1. Go to your service **Settings**
2. Find **"Domains"**
3. Click **"Generate Domain"**
4. Copy the URL (e.g., `https://agentictrade-production.up.railway.app`)

## 7. Populate Database (Important!)
Your database is empty! You need to add stock data:

### Option A: Run locally against Railway database
```bash
# Get DATABASE_URL from Railway dashboard
export DATABASE_URL="postgresql://..."

# Run data ingestion
python ingest/fetch_and_ingest_data.py
```

### Option B: Use Railway's PostgreSQL client
1. In Railway, click on PostgreSQL service
2. Click "Connect"
3. Use the provided connection string

## 8. Update Frontend
Now connect your Vercel frontend to Railway backend:

1. Go to **Vercel Dashboard**
2. Select your project
3. Go to **Settings → Environment Variables**
4. Add/Update:
   - **Name:** `NEXT_PUBLIC_API_URL`
   - **Value:** `https://your-railway-url.up.railway.app`
5. Go to **Deployments**
6. Click **"..."** on latest deployment
7. Click **"Redeploy"**

## 9. Test It!
1. Visit your Vercel URL
2. Click "Run Backtest"
3. It should work! 🎉

## Troubleshooting

### Build fails?
- Check logs in Railway dashboard
- Make sure `gunicorn` is in `requirements.txt`
- Verify root directory is set to `api`

### Database connection error?
- Check if `DATABASE_URL` is set in environment variables
- Make sure PostgreSQL service is running

### No data in results?
- Your database is probably empty
- Run the data ingestion script (Step 7)

### CORS errors?
- Backend should have `CORS(app)` enabled (already done)
- Check browser console for specific errors

## Summary
✅ Code updated for production
✅ Railway config added
✅ Database connection uses environment variable
✅ Ready to deploy!

**Next:** Push to GitHub, then follow steps 1-9 above!
