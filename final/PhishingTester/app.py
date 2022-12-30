from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ml_model as ml

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def index():
    return {"message": "server is running!"}

@app.get('/examine/{url:path}')
def run_ml_predict(url: str):
    return {
        "url": url,
        "phishing_percentage": ml.get_phishing_percentage(url)
    }
