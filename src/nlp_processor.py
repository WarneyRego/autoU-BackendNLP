"""
Módulo para processamento NLP de textos de email
Inclui limpeza, tokenização, remoção de stop words e stemming
"""

import nltk
import re
import string
import ssl
import os
import unicodedata
from typing import List

# Fix para erro de SSL no download do NLTK (comum em macOS)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Configurar diretório de dados do NLTK local para evitar erro de permissão
nltk_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'nltk_data')
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)
nltk.data.path.append(nltk_data_dir)

# Download de recursos necessários do NLTK (será feito na primeira execução)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print(f"Baixando NLTK punkt em {nltk_data_dir}...")
    nltk.download('punkt', download_dir=nltk_data_dir)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print(f"Baixando NLTK stopwords em {nltk_data_dir}...")
    nltk.download('stopwords', download_dir=nltk_data_dir)

try:
    nltk.data.find('stemmers/rslp')
except LookupError:
    print(f"Baixando NLTK rslp em {nltk_data_dir}...")
    nltk.download('rslp', download_dir=nltk_data_dir)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer

class NLPProcessor:
    """
    Classe responsável pelo processamento de linguagem natural
    """
    
    def __init__(self, language: str = 'portuguese'):
        self.language = language
        self.stop_words = set()
        self._load_stopwords()
        self.stemmer = RSLPStemmer()
    
    def _load_stopwords(self):
        """Carrega stopwords para o idioma especificado"""
        try:
            self.stop_words = set(stopwords.words(self.language))
        except:
            # Se não houver stopwords para o idioma, usar lista básica
            self.stop_words = {
                'a', 'o', 'e', 'do', 'da', 'em', 'um', 'uma', 'com', 'no', 'na',
                'por', 'os', 'as', 'dos', 'das', 'ou', 'para', 'é', 'são', 'foi',
                'era', 'eram', 'este', 'esta', 'estes', 'estas', 'de', 'que'
            }
    
    def clean_text(self, text: str) -> str:
        """
        Limpa o texto removendo caracteres especiais e normalizando
        
        Args:
            text: Texto a ser limpo
            
        Returns:
            Texto limpo
        """
        # Converter para minúsculas
        text = text.lower()
        
        # Remover acentos
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
        
        # Remover URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remover emails
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remover caracteres especiais mas manter pontuação básica
        text = re.sub(r'[^\w\s\.\,\!\?\;\:]', ' ', text)
        
        # Remover espaços extras
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def remove_stopwords(self, text: str) -> str:
        """
        Remove stopwords do texto
        
        Args:
            text: Texto a ser processado
            
        Returns:
            Texto sem stopwords
        """
        tokens = word_tokenize(text, language=self.language)
        filtered_tokens = [token for token in tokens if token.lower() not in self.stop_words]
        return ' '.join(filtered_tokens)
    
    def apply_stemming(self, text: str) -> str:
        """
        Aplica stemming ao texto (reduz palavras à sua raiz)
        
        Args:
            text: Texto a ser processado
            
        Returns:
            Texto com stemming aplicado
        """
        tokens = word_tokenize(text, language=self.language)
        stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
        return ' '.join(stemmed_tokens)
    
    def preprocess(self, text: str, remove_stopwords_flag: bool = True, apply_stemming_flag: bool = True) -> str:
        """
        Processamento completo do texto
        
        Args:
            text: Texto a ser processado
            remove_stopwords_flag: Se deve remover stopwords
            apply_stemming_flag: Se deve aplicar stemming
            
        Returns:
            Texto processado
        """
        # 1. Limpeza básica
        text = self.clean_text(text)
        
        # 2. Remoção de Stopwords
        if remove_stopwords_flag:
            text = self.remove_stopwords(text)
            
        # 3. Stemming (opcional, mas recomendado para classificação)
        if apply_stemming_flag:
            text = self.apply_stemming(text)
            
        return text