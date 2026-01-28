# AutoU Email Classifier - Backend

Backend da aplicação AutoU Email Classifier, desenvolvido com FastAPI e Python.

## 🚀 Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **Python 3.8+** - Linguagem de programação
- **NLTK** - Processamento de linguagem natural
- **PyPDF2** - Processamento de arquivos PDF
- **Transformers** - Modelos de IA (Hugging Face)

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes)

## 🔧 Instalação

1. Clone o repositório
2. Navegue até a pasta backend:
   ```bash
   cd backend
   ```

3. Crie e ative o ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

## 🏃‍♂️ Executando a aplicação

### Desenvolvimento (com reload automático)
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Produção
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 📡 Endpoints da API

### Health Check
- `GET /` - Informações básicas da API
- `GET /health` - Verifica se a API está funcionando

### Classificação
- `POST /classify/text` - Classifica email a partir de texto
- `POST /classify/file` - Classifica email a partir de arquivo (.txt ou .pdf)

## 🧪 Executando os testes

```bash
pytest tests/ -v
```

## 📁 Estrutura do Projeto

```
backend/
├── app.py                    # Aplicação FastAPI principal
├── config.py                 # Configurações da aplicação
├── requirements.txt          # Dependências do projeto
├── .env.example              # Exemplo de arquivo de configuração
├── src/                      # Código fonte principal
│   ├── __init__.py
│   ├── email_processor.py   # Processamento de arquivos
│   ├── nlp_processor.py     # Processamento NLP
│   ├── classifier.py        # Classificação de emails
│   └── response_generator.py # Geração de respostas
├── tests/                    # Testes da aplicação
│   └── test_basic.py        # Testes básicos
└── data/                     # Dados da aplicação
    ├── uploads/             # Arquivos enviados
    ├── samples/             # Amostras de teste
    └── processed/           # Dados processados
```

## 🔐 Segurança

- Validação de tipos de arquivo
- Limitação de tamanho de upload
- CORS configurado
- Tratamento de erros apropriado

## 📝 Notas

- Esta é a Fase 1 do projeto (Setup e estrutura base)
- A classificação atual é baseada em palavras-chave simples
- Modelos de IA serão implementados nas próximas fases

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença especificada no repositório principal.