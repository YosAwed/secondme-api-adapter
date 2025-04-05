import requests
from logger import log_request, log_response, log_error
from config import OLLAMA_CHAT_URL, OLLAMA_EMBEDDING_URL, CHAT_MODEL_NAME, EMBEDDING_MODEL_NAME

def convert_to_ollama_chat_request(openai_request):
    """
    Convert OpenAI format chat request to Ollama format
    """
    ollama_request = {
        "model": CHAT_MODEL_NAME,
        "messages": openai_request.get("messages", []),
        "stream": openai_request.get("stream", False)
    }
    
    # Convert optional parameters
    if "temperature" in openai_request:
        ollama_request["temperature"] = openai_request["temperature"]
    if "max_tokens" in openai_request:
        ollama_request["max_tokens"] = openai_request["max_tokens"]
    if "top_p" in openai_request:
        ollama_request["top_p"] = openai_request["top_p"]
    
    return ollama_request

def convert_from_ollama_chat_response(ollama_response):
    """
    Convert Ollama format chat response to OpenAI format
    """
    openai_response = {
        "id": "chatcmpl-" + ollama_response.get("id", "default"),
        "object": "chat.completion",
        "created": int(float(ollama_response.get("created_at", "0").replace("Z", "").replace("T", " ").split(".")[0].replace("-", "").replace(":", "").replace(" ", ""))),
        "model": CHAT_MODEL_NAME,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": ollama_response.get("message", {}).get("content", "")
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": ollama_response.get("prompt_eval_count", 0),
            "completion_tokens": ollama_response.get("eval_count", 0),
            "total_tokens": ollama_response.get("prompt_eval_count", 0) + ollama_response.get("eval_count", 0)
        }
    }
    
    return openai_response

def convert_to_ollama_embedding_request(openai_request):
    """
    Convert OpenAI format embedding request to Ollama format
    """
    input_text = openai_request.get("input", "")
    if isinstance(input_text, list):
        # If multiple inputs are provided, use only the first one (due to Ollama's limitation)
        input_text = input_text[0]
    
    ollama_request = {
        "model": EMBEDDING_MODEL_NAME,
        "prompt": input_text
    }
    
    return ollama_request, input_text

def convert_from_ollama_embedding_response(ollama_response, input_text):
    """
    Convert Ollama format embedding response to OpenAI format
    """
    openai_response = {
        "object": "list",
        "data": [
            {
                "object": "embedding",
                "embedding": ollama_response.get("embedding", []),
                "index": 0
            }
        ],
        "model": EMBEDDING_MODEL_NAME,
        "usage": {
            "prompt_tokens": len(input_text.split()),
            "total_tokens": len(input_text.split())
        }
    }
    
    return openai_response

def send_ollama_chat_request(ollama_request):
    """
    Send chat request to Ollama
    """
    try:
        log_request("chat", ollama_request)
        response = requests.post(OLLAMA_CHAT_URL, json=ollama_request)
        response.raise_for_status()
        ollama_response = response.json()
        log_response("chat", ollama_response)
        return ollama_response, None
    except requests.exceptions.RequestException as e:
        error_msg = f"Error occurred while sending request to Ollama server: {str(e)}"
        log_error("chat", error_msg)
        return None, (error_msg, 500)

def send_ollama_embedding_request(ollama_request):
    """
    Send embedding request to Ollama
    """
    try:
        log_request("embeddings", ollama_request)
        response = requests.post(OLLAMA_EMBEDDING_URL, json=ollama_request)
        response.raise_for_status()
        ollama_response = response.json()
        log_response("embeddings", ollama_response)
        return ollama_response, None
    except requests.exceptions.RequestException as e:
        error_msg = f"Error occurred while sending request to Ollama server: {str(e)}"
        log_error("embeddings", error_msg)
        return None, (error_msg, 500)
