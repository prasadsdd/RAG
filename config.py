import os
from dotenv import load_dotenv

load_dotenv()

AWS_CONFIG = {
    "aws_access_key_id": os.getenv("aws_access_key_id"),
    "aws_secret_access_key": os.getenv("aws_secret_access_key"),
    "region_name": os.getenv("region_name")
}