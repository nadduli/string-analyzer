# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.strings import router as strings_router

app = FastAPI(
    title="String Analyzer API",
    version="1.0.0",
    description="HNG13 Backend Stage 1 - Simple In-Memory String Analyzer"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(strings_router)

@app.get("/")
async def root():
    return {
        "message": "String Analyzer API",
        "version": "1.0.0",
        "storage": "in-memory array",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Add some sample data on startup
@app.on_event("startup")
async def startup_event():
    from app.storage import storage
    from app.utils.analyzer import StringAnalyzer
    
    # Add some sample strings for testing
    sample_strings = [
        "hello world",
        "madam",
        "racecar",
        "test string",
        "a",
        "python programming"
    ]
    
    for sample in sample_strings:
        if not storage.string_exists(sample):
            properties = StringAnalyzer.analyze_string(sample)
            storage.add_string({
                "value": sample,
                "properties": properties
            })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )