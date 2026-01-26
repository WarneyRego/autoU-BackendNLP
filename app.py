from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import sys
import io
import PyPDF2

# Adiciona o diretório src ao path para importar os módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from nlp_processor import NLPProcessor
from gemini_service import GeminiService
from supabase_service import SupabaseService
from email_service import EmailService

# Carrega as variáveis de ambiente do arquivo .env no diretório atual
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)
# Habilita CORS para todas as rotas, incluindo /health
CORS(app, resources={
    r"/api/*": {"origins": "*"},
    r"/health": {"origins": "*"},
    r"/": {"origins": "*"}
})

# Inicializa os serviços
nlp = NLPProcessor()
gemini = GeminiService()
supabase = SupabaseService()
email_srv = EmailService()

@app.route('/')
def home():
    return jsonify({"message": "AutoU Backend - NLP API"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/fetch-emails', methods=['GET'])
def fetch_emails():
    try:
        # Tenta pegar credenciais dos headers ou args (opcional, fallback para .env)
        user = request.args.get('email_user')
        password = request.args.get('email_pass')
        host = request.args.get('imap_host') or os.getenv("IMAP_HOST", "imap.gmail.com")
        
        if not user or not password:
            return jsonify({"error": "Configurações de email não encontradas. Por favor, configure seu email e senha de app no painel de configurações."}), 400
        
        limit = request.args.get('limit', default=10, type=int)
        
        # Instancia um novo serviço se houver credenciais dinâmicas
        if request.args.get('email_user'):
            temp_srv = EmailService()
            temp_srv.user = user
            temp_srv.password = password
            temp_srv.host = host
            emails = temp_srv.fetch_latest_emails(limit=limit)
        else:
            emails = email_srv.fetch_latest_emails(limit=limit)
            
        return jsonify(emails)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        user_email = request.args.get('email_user') or os.getenv("EMAIL_USER")
        if not user_email:
            return jsonify([]) # Retorna vazio se não houver email configurado
            
        limit = request.args.get('limit', default=20, type=int)
        history = supabase.get_history(user_email, limit=limit)
        return jsonify(history)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/<id>', methods=['DELETE'])
def delete_history_item(id):
    try:
        success = supabase.delete_analysis(id)
        if success:
            return jsonify({"message": "Item deleted successfully"}), 200
        else:
            return jsonify({"error": "Failed to delete item"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/process-file', methods=['POST'])
def process_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if file.filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return jsonify({"text": text})
        else:
            return jsonify({"error": "Unsupported file format"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/process', methods=['POST'])
def process_email():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided"}), 400
        
        text = data['text']
        subject = data.get('subject', 'Manual Input')
        sender = data.get('sender', 'User')
        user_email = data.get('email_user') or os.getenv("EMAIL_USER")
        
        if not user_email:
            return jsonify({"error": "Usuário não identificado. Configure seu email."}), 400
            
        # Pipeline de processamento passo a passo
        cleaned_text = nlp.clean_text(text)
        text_no_stopwords = nlp.remove_stopwords(cleaned_text)
        stemmed_text = nlp.apply_stemming(text_no_stopwords)
        
        # Análise com Gemini
        gemini_analysis = gemini.analyze_email(stemmed_text, text)

        # Salva no Supabase com metadados e vínculo do usuário
        analysis_to_save = {
            **gemini_analysis,
            "subject": subject,
            "sender": sender
        }
        supabase.save_analysis(text, analysis_to_save, user_email)

        result = {
            "original_text": text,
            "cleaned_text": cleaned_text,
            "text_no_stopwords": text_no_stopwords,
            "stemmed_text": stemmed_text,
            "stems": stemmed_text.split(),
            "gemini_analysis": gemini_analysis
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(debug=False, port=port, host='0.0.0.0')