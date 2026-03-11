from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "SmartStock AI is running!"}