from flask import Flask, render_template, request, jsonify
from modules.data_loader import load_pdf
from modules.chunking import split_documents
from modules.vector_store import get_or_create_vectorstore, add_documents_to_store, save_vectorstore
from modules.llm import get_response
import os
from config import AWS_CONFIG

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.pdf'):
        filename = str(uuid.uuid4()) + ".pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process PDF
        documents = load_pdf(filepath)
        chunks = split_documents(documents)
        vector_store = get_or_create_vectorstore()
        add_documents_to_store(vector_store, chunks)
        save_vectorstore(vector_store)
        
        return jsonify({'message': 'File processed successfully'}), 200
    
    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    vector_store = get_or_create_vectorstore()
    response = get_response(question, vector_store)
    
    return jsonify({'answer': response}), 200

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)