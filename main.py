from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
from Background import analyze_resume  # Ensure this function is correctly implemented
from chat import get_response
from dash import extract_skills
app = FastAPI()

# CORS setup to allow frontend access (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def intro():
    return {"message": "Welcome to Background Checker"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # Save uploaded file to disk
    save_path = Path("data") / file.filename
    save_path.parent.mkdir(parents=True, exist_ok=True)  # Create 'data' folder if it doesn't exist

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Call background check logic and return parsed data
    result = analyze_resume(save_path)
    return result  # Return directly if it's already a dictionary

@app.get('/chat')
async def chat(request: Request):
    result=await get_response(request)
    print(result)
    return result

@app.get('/get-skills')
async def get_skills(request: Request):
    result=await extract_skills(request)
    return result