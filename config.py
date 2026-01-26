"""
Configurações da aplicação AutoU Email Classifier
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do servidor
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Configurações de upload
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10485760))  # 10MB em bytes
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "data/uploads")

# Configurações de segurança
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Configurações de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configurações de IA/ML
MODEL_DIR = "models"
CLASSIFIER_MODEL_PATH = os.path.join(MODEL_DIR, "email_classifier.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")

# Chaves de API (para uso futuro)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Configurações de processamento
MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH", 10000))  # Máximo de caracteres
SUPPORTED_LANGUAGES = ["pt", "en", "es"]

# Criar diretórios necessários
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)