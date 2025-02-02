from langchain.vectorstores import FAISS
from modules.embeddings import get_bedrock_embeddings

def get_or_create_vectorstore():
    embeddings = get_bedrock_embeddings()
    try:
        return FAISS.load_local("faiss_local", embeddings, allow_dangerous_deserialization=True)
    except:
        return FAISS.from_documents([], embeddings)

def add_documents_to_store(vector_store, documents):
    vector_store.add_documents(documents)

def save_vectorstore(vector_store):
    vector_store.save_local("faiss_local")
