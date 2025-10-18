# Deployment Configuration

Deployment configurations for REWIND application components.

## Available Configurations

### [railway.json](railway.json)
Railway configuration for backend API deployment.

### [vercel.json](vercel.json)
Vercel configuration for frontend deployment.

### [firebase.json](firebase.json)
Firebase configuration for storage, hosting, and Firestore rules.

## Quick Deploy

### Frontend (Vercel)

```bash
cd ../frontend
npm i -g vercel
vercel --prod
```

### Backend (Railway)

```bash
cd ../backend
npm i -g @railway/cli
railway login
railway up
```

### Firebase Setup

```bash
npm i -g firebase-tools
firebase login
firebase deploy
```

## Environment Variables

Ensure all required environment variables are configured in deployment platform dashboards:

### Vercel (Frontend)
- `VITE_API_BASE_URL`
- `VITE_FIREBASE_*` variables

### Railway (Backend)
- `TWELVELABS_API_KEY`
- `GEMINI_API_KEY`
- `ELEVENLABS_API_KEY`
- `FIREBASE_*` variables

## Production Checklist

- [ ] Set all environment variables
- [ ] Configure CORS origins
- [ ] Enable production logging
- [ ] Set up error monitoring
- [ ] Configure CDN
- [ ] Test API endpoints
- [ ] Verify Firebase rules
- [ ] Set up domain/SSL
- [ ] Configure analytics
- [ ] Test deployment

## Monitoring

- **Backend**: Railway dashboard for logs and metrics
- **Frontend**: Vercel analytics and logs
- **Storage**: Firebase console for usage

## Rollback

### Vercel
```bash
vercel rollback [deployment-url]
```

### Railway
Revert through Railway dashboard or redeploy previous commit.

## Scaling

### Backend
Adjust Railway plan for CPU/memory requirements.

### Frontend
Vercel automatically scales with traffic.

### Storage
Firebase scales automatically; monitor quotas.

## Team

Deployment configurations maintained by the REWIND core team.