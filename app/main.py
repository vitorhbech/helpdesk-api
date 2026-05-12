from fastapi import FastAPI
from app.api.routes import auth


app = FastAPI(
    title="Helpdesk API",
    description="A helpdesk management API",
    version="0.1.0"
)

app.include_router(auth.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}