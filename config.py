# Ollamaの設定
OLLAMA_HOST = "localhost"
OLLAMA_PORT = 11434
OLLAMA_CHAT_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/chat"
OLLAMA_EMBEDDING_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/embeddings"

# モデル設定
CHAT_MODEL_NAME = "llama3.2"  # チャット用モデル
EMBEDDING_MODEL_NAME = "nomic-embed-text"  # 埋め込み用モデル

# アダプターの設定
ADAPTER_HOST = "0.0.0.0"
ADAPTER_PORT = 8080

# ログ設定
DEBUG_MODE = False  # デバッグモードを有効にするとリクエスト/レスポンスの詳細が表示されます
