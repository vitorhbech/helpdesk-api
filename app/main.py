from fastapi import FastAPI, Depends
from app.api.routes import auth
from app.api.deps import get_current_user

app = FastAPI(
    title="Helpdesk API",
    description="A helpdesk management API",
    version="0.1.0"
)

app.include_router(auth.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }