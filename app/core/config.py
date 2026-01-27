from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGO_URL: str = os.getenv("MONOGO_URL")
    MONGO_DB: str = os.getenv("MONGO_DB")
    SECRET_KEY: str = os.getenv("SECRET_KEY")

settings = Settings()