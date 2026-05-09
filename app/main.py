from fastapi import FastAPI

app = FastAPI(
    title="Helpdesk API",
    description="A helpdesk management API",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}