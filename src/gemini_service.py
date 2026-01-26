from google import genai
from google.genai import types
import os
import json
import logging

# Configuração básica de log para ver o fallback acontecendo
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
            
            # Lista de modelos para fallback em ordem decrescente de preferência
            self.available_models = []
            
            # 1. Modelo definido no ambiente (se houver)
            env_model = os.getenv('GEMINI_MODEL')
            if env_model:
                self.available_models.append(env_model)
            
            # 2. Modelos padrão do Gemini (mais recentes/poderosos primeiro)
            # Lista atualizada com base nos modelos disponíveis na API (v1beta)
            default_models = [
                'gemini-3-pro-preview',   # SOTA (State of the Art)
                'gemini-3-flash-preview', # SOTA Rápido
                'gemini-2.5-pro',         # Alta performance
                'gemini-2.5-flash',       # Balanceado (Padrão)
                'gemini-2.0-flash',       # Versão anterior estável
                'gemini-1.5-pro',         # Legado estável
                'gemini-1.5-flash'        # Legado rápido
            ]
            
            for m in default_models:
                if m not in self.available_models:
                    self.available_models.append(m)
        else:
            self.client = None
            self.available_models = []

    def analyze_email(self, processed_text, original_text):
        if not self.client:
            return {
                "classification": "erro",
                "suggested_response": "Erro: Chave de API do Gemini não configurada."
            }

        prompt = f"""
        Você é um assistente de triagem de emails inteligente.
        
        Analise o seguinte email:
        
        TEXTO ORIGINAL:
        "{original_text}"
        
        TEXTO PROCESSADO (NLP):
        "{processed_text}"
        
        Tarefa:
        1. Classifique o email como 'produtivo' (requer ação humana, resposta, ou é importante) ou 'improdutivo' (spam, promoções, notificações automáticas, agradecimentos simples sem necessidade de follow-up).
        2. Se for 'produtivo', sugira uma resposta profissional e direta. Se for 'improdutivo', a resposta pode ser null ou uma breve justificativa.
        
        Retorne a resposta EXATAMENTE no formato JSON abaixo:
        {{
            "classification": "produtivo" | "improdutivo",
            "suggested_response":String | null,
            "reasoning": "Breve explicação da classificação"
        }}
        """

        last_error = None
        tried_models = []

        for model_name in self.available_models:
            try:
                logger.info(f"Tentando analisar com o modelo: {model_name}")
                
                # Configuração para resposta JSON
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
                )
                
                # Se chegou aqui, funcionou
                result = json.loads(response.text)
                
                # Adiciona metadados sobre qual modelo foi usado (útil para debug/info)
                result['model_used'] = model_name
                return result

            except Exception as e:
                last_error = str(e)
                tried_models.append(model_name)
                logger.warning(f"Falha com modelo {model_name}: {e}")
                continue

        # Se saiu do loop, todos falharam
        error_msg = f"Falha em todos os modelos tentados ({', '.join(tried_models)}). Último erro: {last_error}"
        logger.error(error_msg)
        
        return {
            "classification": "erro",
            "suggested_response": error_msg,
            "reasoning": "Falha de conexão com múltiplos modelos IA"
        }
