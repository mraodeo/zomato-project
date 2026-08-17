# Deployment Plan: Railway (Backend) + Vercel (Frontend)

We will use a hybrid deployment architecture that leverages the best-in-class platforms for both of our technologies:
- **Backend (FastAPI)**: Railway
- **Frontend (Next.js)**: Vercel

## Open Questions

> [!NOTE]
> Are you deploying the frontend and backend from the **same GitHub repository** (a monorepo) or **separate repositories**? 
> (If same repo, we will need to configure Vercel's Root Directory setting).

## Proposed Changes

To prepare our codebase for deployment, I will make the following code changes:

### Backend Configuration (Railway)

We need to tell Railway how to start our Python FastAPI application.

#### [NEW] [Procfile](file:///c:/Users/mange/Desktop/Project-Nextleap/Procfile)
- I will create a `Procfile` in the root directory containing: `web: uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`

#### [MODIFY] [main.py](file:///c:/Users/mange/Desktop/Project-Nextleap/src/api/main.py)
- Currently, CORS allows all origins (`*`). This is fine for initial deployment, but I will prepare it so it can optionally read an `ALLOWED_ORIGINS` environment variable to strictly allow the Vercel URL in the future.

### Frontend Configuration (Vercel)

We need to stop hardcoding `http://localhost:8000` in our frontend so that it dynamically talks to the Railway API in production.

#### [MODIFY] [page.tsx](file:///c:/Users/mange/Desktop/Project-Nextleap/stitch_tablemate_ai_recommendation_engine/src/app/page.tsx)
- I will replace the hardcoded `http://localhost:8000/api/v1/recommendations` with an environment variable: `const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";`

#### [NEW] [.env.local](file:///c:/Users/mange/Desktop/Project-Nextleap/stitch_tablemate_ai_recommendation_engine/.env.local)
- I will create a local environment file so your local development still talks to `localhost:8000`. 
- In the Vercel Dashboard, you will set `NEXT_PUBLIC_API_URL` to your live Railway domain.

## Execution Steps

1. **Approve this plan** so I can make the necessary code changes listed above.
2. Push your code to GitHub.
3. Log into **Railway**, connect your repo, and it will automatically detect the Python app and deploy it. (You will get a `.up.railway.app` URL).
4. Log into **Vercel**, connect your repo, set the Framework Preset to Next.js, and set the `NEXT_PUBLIC_API_URL` Environment Variable to your Railway URL.

Click "Proceed" if you want me to automatically implement the Proposed Changes in your codebase!
