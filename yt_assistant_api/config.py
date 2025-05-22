# TODO update settings and refactor

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ENV: str = os.getenv("ENV")

    API_HOST: str = os.getenv("API_HOST")
    API_PORT: str = os.getenv("API_PORT")
    CLIENT_HOST: str = os.getenv("CLIENT_HOST")
    CLIENT_PORT: str = os.getenv("CLIENT_PORT")
    POSTGRES_URL: str = os.getenv("POSTGRES_URL")

    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
    JWT_ALGORITHM: str = "HS256"
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS")


settings = Settings()
