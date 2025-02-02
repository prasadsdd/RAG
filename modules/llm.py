from langchain.llms.bedrock import Bedrock
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import boto3
from config import AWS_CONFIG

PROMPT_TEMPLATE = """
Human: Use the following pieces of context to provide a 
concise answer to the question at the end but use at least summarize with 
250 words with detailed explanations. If you don't know the answer, 
just say that you don't know, don't try to make up an answer.
<context>
{context}
</context>
Question: {question}
Assistant:"""

def get_llm():
    bedrock_client = boto3.client(
        service_name="bedrock-runtime",
        region_name=AWS_CONFIG["region_name"],
        aws_access_key_id=AWS_CONFIG["aws_access_key_id"],
        aws_secret_access_key=AWS_CONFIG["aws_secret_access_key"]
    )
    return Bedrock(
        model_id="meta.llama3-70b-instruct-v1:0",
        client=bedrock_client
    )

def get_response(question, vector_store):
    llm = get_llm()
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    
    return qa({"query": question})['result']
