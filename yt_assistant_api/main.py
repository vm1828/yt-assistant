import os
from fastapi import FastAPI
from dotenv import load_dotenv


load_dotenv()

app = FastAPI(
    title=f"yt-assistant-{os.getenv('ENV')}",
    description="Web application designed to help users summarize YouTube video transcripts and extract valuable insights through question answering and reasoning",
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
