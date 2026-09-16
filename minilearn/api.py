import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from agent import collect_agent_response
from utils.catalog import load_catalog

app = FastAPI()
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_origin_regex=r"https://.*\.app\.github\.dev$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend Running"}

@app.get("/chat")
async def chat(message: str):
    if not message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        response = await collect_agent_response(message)
    except Exception as exc:
        logger.exception("Agent request failed")
        raise HTTPException(
            status_code=503,
            detail="The model service is temporarily unavailable. Check the Gemini API quota or billing plan.",
        ) from exc

    catalog_by_id = {course["learningId"]: course for course in load_catalog()}
    courses = [
        catalog_by_id[learning_id]
        for learning_id in response.learning_ids
        if learning_id in catalog_by_id
    ]

    return {
        "response": response.message,
        "learning_ids": response.learning_ids,
        "type": response.type,
        "courses": courses,
    }