from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import engine, Base, AsyncSessionLocal
import models
from routers import workspace, ask_neon, seo_engine, campaigns

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Auto-seed default workspace state if empty
    async with AsyncSessionLocal() as session:
        await workspace.seed_database_if_empty(session)
        
    print(f"[{settings.PROJECT_NAME}] Database initialized & seeded successfully.")
    yield
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Configure CORS for Vite frontend and production domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers under /api/v1
app.include_router(workspace.router, prefix=settings.API_V1_PREFIX)
app.include_router(ask_neon.router, prefix=settings.API_V1_PREFIX)
app.include_router(seo_engine.router, prefix=settings.API_V1_PREFIX)
app.include_router(campaigns.router, prefix=settings.API_V1_PREFIX)

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": settings.DATABASE_URL.split("://")[0],
        "modules": [
            "Visual Website Builder",
            "Omnichannel Campaign Studio",
            "Technical & Semantic AI SEO Auditor",
            "Live Visibility Score Engine (0-100)",
            "100K+ Email Parallel Batch Sender",
            "Social Scheduler",
            "Live Cheerio/BeautifulSoup DOM Crawler"
        ]
    }

@app.get("/")
async def root():
    return {
        "message": f"{settings.PROJECT_NAME} v{settings.VERSION} is running.",
        "docs": "/docs",
        "api": "/api/v1"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
