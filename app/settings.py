from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    project_name: str = os.getenv("PROJECT_NAME", "Steve Hof — Math & Stats Tutoring")
    environment: str = os.getenv("ENV", "dev")
    email_api_key: str | None = os.getenv("EMAIL_API_KEY")
    email_from: str = os.getenv("EMAIL_FROM", "no-reply@stevehof.com")
    email_to: str = os.getenv("EMAIL_TO", "stevenhof27@gmail.com")

settings = Settings()
