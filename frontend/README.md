# Frontend - REWIND Client

React-based frontend application with 3D video exploration and VoiceBridge™ narration interface.

## Overview

Modern React application built with Vite, featuring Three.js for 3D rendering, real-time video processing, and multilingual voice narration controls.

## Key Technologies

- **React 18**: UI framework with hooks
- **Vite**: Lightning-fast build tool
- **Three.js**: 3D rendering engine
- **Tailwind CSS**: Utility-first styling
- **Firebase SDK**: Authentication and storage
- **Lucide React**: Icon library

## Quick Start

```bash
# Install dependencies
npm install

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Start development server
npm run dev
```

Application runs at `http://localhost:5173`

## Project Structure

```
frontend/
├── src/
│   ├── components/       # React components
│   │   ├── upload/      # Video upload interface
│   │   ├── viewer/      # 3D scene viewer
│   │   ├── voice/       # VoiceBridge™ controls
│   │   ├── ui/          # Shared UI components
│   │   └── layout/      # Layout components
│   ├── hooks/           # Custom React hooks
│   ├── services/        # API clients
│   ├── utils/           # Helper functions
│   └── styles/          # Global styles
├── public/              # Static assets
└── package.json         # Dependencies
```

## Core Features

### Video Upload
Drag-and-drop interface with progress tracking and real-time processing status.

### 3D Viewer
Interactive Three.js scene with orbital controls, depth-based rendering, and clickable objects.

### VoiceBridge™ Interface
Voice cloning onboarding, language selection, and narration playback controls.

### Timeline Navigation
Smooth scrubbing through video moments with scene thumbnails.

## Key Components

### `SceneViewer.jsx`
Main component integrating 3D scene with narration controls.

### `VoiceCloneOnboarding.jsx`
Guides users through 30-second voice recording for cloning.

### `NarrationButton.jsx`
Triggers on-demand narration generation in selected language.

### `ThreeScene.jsx`
Renders 3D point clouds from depth maps with camera controls.

## Custom Hooks

- `useVideoUpload` - Handles file upload and processing
- `useThreeScene` - Manages Three.js scene lifecycle
- `useVoiceBridge` - VoiceBridge™ integration logic
- `useNarration` - Narration generation and playback
- `useFirebase` - Firebase authentication and storage

## Environment Variables

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_FIREBASE_API_KEY=your_key
VITE_FIREBASE_AUTH_DOMAIN=your_domain
VITE_FIREBASE_PROJECT_ID=your_project
VITE_FIREBASE_STORAGE_BUCKET=your_bucket
```

## Development

### Build for Production

```bash
npm run build
```

Output in `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

### Linting

```bash
npm run lint
```

### Format Code

```bash
npm run format
```

## Styling

Uses Tailwind CSS with custom space theme:

- Dark cosmic background
- Glassmorphism effects
- Smooth animations
- Responsive design

## Testing

```bash
# Run tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage
```

## Performance

- Code splitting for route-based lazy loading
- Image optimization and lazy loading
- Three.js LOD rendering for large point clouds
- Memoization for expensive computations

## Deployment

Deploy to Vercel:

```bash
npm i -g vercel
vercel --prod
```

Or use Docker:

```bash
docker build -t rewind-frontend .
docker run -p 5173:5173 rewind-frontend
```

## Troubleshooting

**Vite not starting**: Clear `node_modules` and reinstall

**Three.js performance**: Reduce point density or enable LOD

**Firebase errors**: Check API keys and project configuration

## Contributing

See main repository [CONTRIBUTING.md](../docs/CONTRIBUTING.md) for guidelines.

## Team

Frontend development led by **Ohinoyi Moiza** - [GitHub](https://github.com/Ohimoiza1205) | [LinkedIn](https://www.linkedin.com/in/ohinoyi-moiza/)