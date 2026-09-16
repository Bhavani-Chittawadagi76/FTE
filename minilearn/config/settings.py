import os
from dotenv import load_dotenv

load_dotenv()


def validate_config():
	"""Return the validated Gemini-compatible model configuration."""
	api_key = os.getenv("GEMINI_API_KEY")
	model = os.getenv("GEMINI_MODEL")

	missing = [
		name
		for name, value in {"GEMINI_API_KEY": api_key, "GEMINI_MODEL": model}.items()
		if not value
	]
	if missing:
		raise ValueError(f"Missing required configuration: {', '.join(missing)}")

	return {
		"GEMINI_API_KEY": api_key,
		"GEMINI_MODEL": model,
	}


config = validate_config()
GEMINI_API_KEY = config["GEMINI_API_KEY"]
GEMINI_MODEL = config["GEMINI_MODEL"]