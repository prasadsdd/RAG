import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    REGION_NAME = os.getenv("AWS_REGION")
    UPLOAD_FOLDER = 'uploads'
    FAISS_INDEX_PATH = 'faiss_local'
    ALLOWED_EXTENSIONS = {'pdf'}