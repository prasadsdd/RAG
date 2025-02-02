from flask import Flask, render_template, request, jsonify
import os
import uuid
from modules.data_loader import process_pdf
from modules.vector_store import get_vector_store
from modules.llm import get_llm_response
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # File upload handling
            if 'file' in request.files:
                file = request.files['file']
                if file.filename == '':
                    return jsonify({'error': 'No selected file'}), 400
                
                if not file.filename.lower().endswith('.pdf'):
                    return jsonify({'error': 'Only PDF files are allowed'}), 400

                # Save file with UUID to prevent conflicts
                temp_filename = f"{uuid.uuid4()}.pdf"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
                file.save(file_path)
                
                # Process PDF and create vectors
                docs = process_pdf(file_path)
                get_vector_store(docs)
                
                # Cleanup temporary file
                os.remove(file_path)
                return jsonify({'status': 'PDF processed successfully'})

            # Question handling
            if 'question' in request.form:
                question = request.form['question'].strip()
                if not question:
                    return jsonify({'error': 'Please enter a question'}), 400
                
                response = get_llm_response(question)
                return jsonify({'answer': response})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(Config.FAISS_INDEX_PATH, exist_ok=True)
    app.run(debug=True)