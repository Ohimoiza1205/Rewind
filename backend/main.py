from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import health, analysis, scene_data, narration

app = FastAPI(
    title="Rewind API",
    description="AI-powered video memory exploration",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(analysis.router, prefix="/api", tags=["analysis"])
app.include_router(scene_data.router, prefix="/api", tags=["scenes"])
app.include_router(narration.router, prefix="/api", tags=["narration"])

@app.get("/")
def root():
    return {
        "message": "Rewind API",
        "status": "running",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
