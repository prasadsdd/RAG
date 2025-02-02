from langchain.document_loaders import PyPDFLoader

def process_pdf(file_path):
    try:
        loader = PyPDFLoader(file_path)
        return loader.load()
    except Exception as e:
        raise RuntimeError(f"PDF processing failed: {str(e)}")