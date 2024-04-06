from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth
from app.config import settings


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST',],
    allow_headers=['Authorization'],
)

app.include_router(auth)

@app.get("/")
def root():
    return {"status": "ok"}
