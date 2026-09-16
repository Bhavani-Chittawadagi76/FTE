import google.generativeai as genai
import logging

from config.settings import *

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

logger.info("[STEP 1] Gemini Loading")

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    GEMINI_MODEL
)

logger.info("[STEP 2] Gemini Ready")

def run_agent(user_input):

    logger.info("[STEP 3] Request Received")

    response = model.generate_content(
        user_input
    )

    logger.info("[STEP 4] Response Generated")

    return response.text