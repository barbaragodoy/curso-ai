import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB: str = os.getenv("MONGODB_DB", "etl_db")
QUALITY_COLLECTION: str = "quality_reports"
DATASETS_COLLECTION: str = "datasets_index"
