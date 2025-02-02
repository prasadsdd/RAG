from langchain.embeddings import BedrockEmbeddings
from config import AWS_CONFIG
import boto3

def get_bedrock_embeddings():
    bedrock_client = boto3.client(
        service_name="bedrock-runtime",
        region_name=AWS_CONFIG["region_name"],
        aws_access_key_id=AWS_CONFIG["aws_access_key_id"],
        aws_secret_access_key=AWS_CONFIG["aws_secret_access_key"]
    )
    return BedrockEmbeddings(
        model_id="amazon.titan-embed-image-v1",
        client=bedrock_client
    )
