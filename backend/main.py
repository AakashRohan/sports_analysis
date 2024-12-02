from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes import odds_routes

app = FastAPI(title="Sports Analysis API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(odds_routes.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to Sports Analysis API"} 