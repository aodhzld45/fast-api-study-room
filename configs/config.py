from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    DATABASE_URL: str
    TZ: str = "Asia/Seoul"

settings = Settings(
    DATABASE_URL=os.environ["DATABASE_URL"],
    TZ=os.environ.get("TZ", "Asia/Seoul"),
)
