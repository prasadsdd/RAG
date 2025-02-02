from langchain.vectorstores import FAISS
from modules.embeddings import get_embeddings
from config import Config

def get_vector_store(docs):
    try:
        if not docs or len(docs) == 0:
            raise ValueError("No documents provided for vector storage")

        embeddings = get_embeddings()
        
        # Try loading existing index
        try:
            vectorstore = FAISS.load_local(
                Config.FAISS_INDEX_PATH, 
                embeddings,
                allow_dangerous_deserialization=True
            )
            vectorstore.add_documents(docs)
        except:
            # Create new index if loading fails
            vectorstore = FAISS.from_documents(docs, embeddings)
        
        vectorstore.save_local(Config.FAISS_INDEX_PATH)
        return True
    except Exception as e:
        raise RuntimeError(f"Vector store error: {str(e)}")
