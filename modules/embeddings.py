from langchain.embeddings import BedrockEmbeddings
import boto3
from config import Config

def get_embeddings():
    try:
        if not Config.REGION_NAME:
            raise RuntimeError("AWS region is not set. Please check your .env file.")

        bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=Config.REGION_NAME,  # ✅ Ensure REGION is correctly used
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        )
        return BedrockEmbeddings(
            model_id="amazon.titan-embed-text-v1",  # Change model_id if needed
            client=bedrock_client
        )
    except Exception as e:
        raise RuntimeError(f"Embeddings initialization failed: {str(e)}")

