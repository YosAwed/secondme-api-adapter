# Ollama configuration
OLLAMA_HOST = "localhost"
OLLAMA_PORT = 11434
OLLAMA_CHAT_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/chat"
OLLAMA_EMBEDDING_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/embeddings"

# Model configuration
CHAT_MODEL_NAME = "llama3.2"  # Model for chat
EMBEDDING_MODEL_NAME = "nomic-embed-text"  # Model for embeddings

# Adapter configuration
ADAPTER_HOST = "0.0.0.0"
ADAPTER_PORT = 8080

# Logging configuration
DEBUG_MODE = False  # When debug mode is enabled, detailed request/response information will be displayed
