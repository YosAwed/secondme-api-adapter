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

# Import settings from config.py
from config import OLLAMA_CHAT_URL, OLLAMA_EMBEDDING_URL, CHAT_MODEL_NAME, EMBEDDING_MODEL_NAME

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    """
    Endpoint compatible with OpenAI's chat completions API
    """
    try:
        data = request.json
        
        # Convert request format from OpenAI to Ollama
        ollama_request = convert_to_ollama_chat_request(data)
        
        # Send request to Ollama
        ollama_response, error = send_ollama_chat_request(ollama_request)
        
        if error:
            return jsonify({"error": error[0]}), error[1]
        
        # Convert response from Ollama to OpenAI format
        openai_response = convert_from_ollama_chat_response(ollama_response)
        
        return jsonify(openai_response)
    except Exception as e:
        logger.error(f"Error occurred in chat completions endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/v1/embeddings', methods=['POST'])
def embeddings():
    """
    Endpoint compatible with OpenAI's embeddings API
    """
    try:
        data = request.json
        
        # Convert request format from OpenAI to Ollama
        ollama_request, input_text = convert_to_ollama_embedding_request(data)
        
        # Send request to Ollama
        ollama_response, error = send_ollama_embedding_request(ollama_request)
        
        if error:
            return jsonify({"error": error[0]}), error[1]
        
        # Convert response from Ollama to OpenAI format
        openai_response = convert_from_ollama_embedding_response(ollama_response, input_text)
        
        return jsonify(openai_response)
    except Exception as e:
        logger.error(f"Error occurred in embeddings endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({"status": "ok", "message": "Secondme API Adapter is running"})

if __name__ == '__main__':
    logger.info(f"Starting Secondme API Adapter on {ADAPTER_HOST}:{ADAPTER_PORT}")
    app.run(host=ADAPTER_HOST, port=ADAPTER_PORT, debug=DEBUG_MODE)