from fastapi import FastAPI

from app.api.users import router as users_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "SmartStock AI is running!"}

app.include_router(users_router)