from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import subprocess
import sys

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeRequest(BaseModel):
    username: str


@app.post("/api/scrape")
def scrape(request: ScrapeRequest):
    project_root = Path(__file__).resolve().parent.parent
    main_script = project_root / "main.py"
    if not main_script.exists():
        raise HTTPException(status_code=500, detail="main.py not found")

    cmd = [sys.executable, str(main_script), "--username", request.username]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(project_root), timeout=600)
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Scraping timed out")

    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {result.stderr[:1000]}")

    return {"stdout": result.stdout, "stderr": result.stderr}
