import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

class Settings:
    PROJECT_NAME: str = "ECOSPHERE AI"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-Assisted Smart Environmental Monitoring and Sustainability Platform"

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{DATA_DIR / 'ecosphere.db'}"
    )

    # JWT & Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "ecosphere-ai-super-secret-security-jwt-key-2026-sustainability")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    # APIs
    OPENAQ_API_KEY: str = os.getenv("OPENAQ_API_KEY", "")
    DATA_GOV_IN_API_KEY: str = os.getenv("DATA_GOV_IN_API_KEY", "")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")

    # Default Monitoring Region
    DEFAULT_CITY: str = os.getenv("DEFAULT_CITY", "Warangal")
    DEFAULT_STATE: str = os.getenv("DEFAULT_STATE", "Telangana")
    DEFAULT_COUNTRY: str = os.getenv("DEFAULT_COUNTRY", "India")
    DEFAULT_LATITUDE: float = float(os.getenv("DEFAULT_LATITUDE", "17.9689"))
    DEFAULT_LONGITUDE: float = float(os.getenv("DEFAULT_LONGITUDE", "79.5941"))

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

settings = Settings()
