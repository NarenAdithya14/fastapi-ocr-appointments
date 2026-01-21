from pydantic import BaseSettings

class Settings(BaseSettings):
    # Define your application settings here
    # For example, you can add database URL, API keys, etc.
    OCR_SERVICE_URL: str = "http://localhost:8000/ocr"
    NLP_SERVICE_URL: str = "http://localhost:8000/nlp"
    APP_ENV: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()