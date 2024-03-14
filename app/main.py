from fastapi import FastAPI

from app.auth.router import router as auth


app = FastAPI()

app.include_router(auth)

@app.get("/")
def root():
    return {"status": "ok"}
