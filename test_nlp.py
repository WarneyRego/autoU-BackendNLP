from src.nlp_processor import NLPProcessor

def test_nlp():
    print("Iniciando teste de NLP...")
    
    # Instanciar processador
    processor = NLPProcessor()
    
    # Texto de exemplo (similar ao contexto de email)
    sample_text = """
    Olá equipe,
    
    Gostaria de agendar uma reunião para discutir o projeto AutoU.
    Por favor, confirmem a disponibilidade para amanhã às 14h.
    
    Atenciosamente,
    João Silva
    joao.silva@example.com
    http://example.com
    """
    
    print(f"\nTexto Original:\n{'-'*20}\n{sample_text}\n{'-'*20}")
    
    # Teste 1: Limpeza básica
    cleaned = processor.clean_text(sample_text)
    print(f"\n1. Texto Limpo (clean_text):\n{cleaned}")
    
    # Teste 2: Remoção de Stopwords
    no_stopwords = processor.remove_stopwords(cleaned)
    print(f"\n2. Sem Stopwords (remove_stopwords):\n{no_stopwords}")
    
    # Teste 3: Stemming
    stemmed = processor.apply_stemming(no_stopwords)
    print(f"\n3. Com Stemming (apply_stemming):\n{stemmed}")
    
    # Teste 4: Processamento completo
    processed = processor.preprocess(sample_text)
    print(f"\n4. Processamento Completo (preprocess):\n{processed}")
    
    print("\nTeste concluído com sucesso!")

if __name__ == "__main__":
    test_nlp()