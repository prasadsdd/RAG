from langchain.llms.bedrock import Bedrock
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS
import boto3
from config import Config
from modules.embeddings import get_embeddings

prompt_template = """
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
    try:
        bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=Config.REGION_NAME,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        )
        return Bedrock(
            model_id="meta.llama3-70b-instruct-v1:0",
            client=bedrock_client
        )
    except Exception as e:
        raise RuntimeError(f"LLM initialization failed: {str(e)}")

def get_llm_response(question):
    try:
        embeddings = get_embeddings()
        vectorstore = FAISS.load_local(
            Config.FAISS_INDEX_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        qa = RetrievalQA.from_chain_type(
            llm=get_llm(),
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        result = qa({"query": question})
        return result['result']
    except Exception as e:
        raise RuntimeError(f"Query processing failed: {str(e)}")
