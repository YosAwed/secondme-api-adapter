import requests
import json
from flask import Flask, request, jsonify
from config import ADAPTER_HOST, ADAPTER_PORT, DEBUG_MODE
from logger import logger
from adapters import (
    convert_to_ollama_chat_request, convert_from_ollama_chat_response,
    convert_to_ollama_embedding_request, convert_from_ollama_embedding_response,
    send_ollama_chat_request, send_ollama_embedding_request
)

app = Flask(__name__)

# Ollamaのエンドポイント設定
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
OLLAMA_EMBEDDING_URL = "http://localhost:11434/api/embeddings"
CHAT_MODEL_NAME = "llama3.2"  # チャット用モデル
EMBEDDING_MODEL_NAME = "nomic-embed-text"  # 埋め込み用モデル

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    """
    OpenAIのchat completions APIと互換性のあるエンドポイント
    """
    try:
        data = request.json
        
        # OpenAIからOllamaへのリクエスト形式変換
        ollama_request = convert_to_ollama_chat_request(data)
        
        # Ollamaへリクエスト送信
        ollama_response, error = send_ollama_chat_request(ollama_request)
        
        if error:
            return jsonify({"error": error[0]}), error[1]
        
        # OllamaからOpenAI形式への変換
        openai_response = convert_from_ollama_chat_response(ollama_response)
        
        return jsonify(openai_response)
    except Exception as e:
        logger.error(f"チャット完了エンドポイントでエラーが発生しました: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/v1/embeddings', methods=['POST'])
def embeddings():
    """
    OpenAIのembeddings APIと互換性のあるエンドポイント
    """
    try:
        data = request.json
        
        # OpenAIからOllamaへのリクエスト形式変換
        ollama_request, input_text = convert_to_ollama_embedding_request(data)
        
        # Ollamaへリクエスト送信
        ollama_response, error = send_ollama_embedding_request(ollama_request)
        
        if error:
            return jsonify({"error": error[0]}), error[1]
        
        # OllamaからOpenAI形式への変換
        openai_response = convert_from_ollama_embedding_response(ollama_response, input_text)
        
        return jsonify(openai_response)
    except Exception as e:
        logger.error(f"埋め込みエンドポイントでエラーが発生しました: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    ヘルスチェックエンドポイント
    """
    return jsonify({"status": "ok", "message": "Secondme API Adapter is running"})

if __name__ == '__main__':
    logger.info(f"Secondme API Adapter を {ADAPTER_HOST}:{ADAPTER_PORT} で起動します")
    app.run(host=ADAPTER_HOST, port=ADAPTER_PORT, debug=DEBUG_MODE)