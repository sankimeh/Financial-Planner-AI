from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Financial Planner API is running!"}
