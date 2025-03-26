import os
import re
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import PyPDF2
import ollama

app = Flask(__name__)

# Configure upload folder and allowed file types
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'xlsx'}

extracted_text = ""  # Global variable to store extracted text
chat_history = []    # Global variable to store conversation history

# Specify the model to use
LLAMA_MODEL = 'llama3.2:1b'

# Ensure uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        return f"Error reading PDF: {e}"
    return text

# Function to interact with Ollama using the llama 3.2:1b model
def get_llama_response(question, context, chat_history):
    # Combine conversation history into a single string
    history_text = "\n".join(chat_history)
    # Build the prompt including the context and conversation history
    prompt = f"Context: {context}\n\n{history_text}\nUser: {question}\nAssistant:"
    response = ollama.chat(model=LLAMA_MODEL, messages=[{"role": "user", "content": prompt}])
    return response['message']['content'] if 'message' in response else "Error generating response."

# Route for file upload
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    global extracted_text, chat_history
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            if filename.endswith('.pdf'):
                extracted_text = extract_text_from_pdf(filepath)
            # Reset chat history when a new file is uploaded
            chat_history = []
            return render_template('chatbot.html', response=extracted_text[:500] + "...")
        else:
            return "Invalid file format. Only PDF, DOCX, and XLSX are allowed."
    return render_template('upload.html')

# Route for continuous chat question answering
@app.route('/ask_question', methods=['POST'])
def ask_question():
    global chat_history, extracted_text
    question = request.form.get('question', '').strip()
    if not question:
        return jsonify({'answer': 'Please enter a valid question.'})
    
    # Append user's question to chat history
    chat_history.append(f"User: {question}")
    # Get assistant's answer using the full context and conversation history
    answer = get_llama_response(question, extracted_text, chat_history)
    # Append assistant's answer to chat history
    chat_history.append(f"Assistant: {answer}")
    return jsonify({'answer': answer})

# Home route
@app.route('/')
def index():
    return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run(debug=True)