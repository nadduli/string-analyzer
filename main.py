from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.strings import router

app = FastAPI(
    title="String Analyzer API",
    version="1.0.0",
    description="HNG13 Backend Stage 1 - String Analyzer Service"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "String Analyzer API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)