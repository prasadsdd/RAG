# RAG Application with AWS Bedrock

A Flask-based RAG application using AWS Bedrock for document question answering.

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt


rag_project/
├── app.py
├── requirements.txt
├── .env
├── config.py
├── uploads/
├── modules/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   └── llm.py
├── templates/
│   └── index.html
├── static/
│   ├── styles.css
│  
└── .gitignore   