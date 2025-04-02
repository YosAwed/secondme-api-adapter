import requests
from logger import log_request, log_response, log_error
from config import OLLAMA_CHAT_URL, OLLAMA_EMBEDDING_URL, CHAT_MODEL_NAME, EMBEDDING_MODEL_NAME

def convert_to_ollama_chat_request(openai_request):
    """
    OpenAIu5f62u5f0fu306eu30c1u30e3u30c3u30c8u30eau30afu30a8u30b9u30c8u3092Ollamau5f62u5f0fu306bu5909u63dbu3059u308b
    """
    ollama_request = {
        "model": CHAT_MODEL_NAME,
        "messages": openai_request.get("messages", []),
        "stream": openai_request.get("stream", False)
    }
    
    # u30aau30d7u30b7u30e7u30f3u30d1u30e9u30e1u30fcu30bfu306eu5909u63db
    if "temperature" in openai_request:
        ollama_request["temperature"] = openai_request["temperature"]
    if "max_tokens" in openai_request:
        ollama_request["max_tokens"] = openai_request["max_tokens"]
    if "top_p" in openai_request:
        ollama_request["top_p"] = openai_request["top_p"]
    
    return ollama_request

def convert_from_ollama_chat_response(ollama_response):
    """
    Ollamau5f62u5f0fu306eu30c1u30e3u30c3u30c8u30ecu30b9u30ddu30f3u30b9u3092OpenAIu5f62u5f0fu306bu5909u63dbu3059u308b
    """
    openai_response = {
        "id": "chatcmpl-" + ollama_response.get("id", "default"),
        "object": "chat.completion",
        "created": int(ollama_response.get("created_at", 0)),
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
    OpenAIu5f62u5f0fu306eu57cbu3081u8fbcu307fu30eau30afu30a8u30b9u30c8u3092Ollamau5f62u5f0fu306bu5909u63dbu3059u308b
    """
    input_text = openai_request.get("input", "")
    if isinstance(input_text, list):
        # u8907u6570u306eu5165u529bu304cu3042u308bu5834u5408u306fu6700u521du306eu3082u306eu3060u3051u4f7fu7528uff08Ollamau306eu5236u9650u306bu3088u308buff09
        input_text = input_text[0]
    
    ollama_request = {
        "model": EMBEDDING_MODEL_NAME,
        "prompt": input_text
    }
    
    return ollama_request, input_text

def convert_from_ollama_embedding_response(ollama_response, input_text):
    """
    Ollamau5f62u5f0fu306eu57cbu3081u8fbcu307fu30ecu30b9u30ddu30f3u30b9u3092OpenAIu5f62u5f0fu306bu5909u63dbu3059u308b
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
    Ollamau306bu30c1u30e3u30c3u30c8u30eau30afu30a8u30b9u30c8u3092u9001u4fe1u3059u308b
    """
    try:
        log_request("chat", ollama_request)
        response = requests.post(OLLAMA_CHAT_URL, json=ollama_request)
        response.raise_for_status()
        ollama_response = response.json()
        log_response("chat", ollama_response)
        return ollama_response, None
    except requests.exceptions.RequestException as e:
        error_msg = f"Ollamau30b5u30fcu30d0u30fcu3078u306eu30eau30afu30a8u30b9u30c8u4e2du306bu30a8u30e9u30fcu304cu767au751fu3057u307eu3057u305f: {str(e)}"
        log_error("chat", error_msg)
        return None, (error_msg, 500)

def send_ollama_embedding_request(ollama_request):
    """
    Ollamau306bu57cbu3081u8fbcu307fu30eau30afu30a8u30b9u30c8u3092u9001u4fe1u3059u308b
    """
    try:
        log_request("embeddings", ollama_request)
        response = requests.post(OLLAMA_EMBEDDING_URL, json=ollama_request)
        response.raise_for_status()
        ollama_response = response.json()
        log_response("embeddings", ollama_response)
        return ollama_response, None
    except requests.exceptions.RequestException as e:
        error_msg = f"Ollamau30b5u30fcu30d0u30fcu3078u306eu30eau30afu30a8u30b9u30c8u4e2du306bu30a8u30e9u30fcu304cu767au751fu3057u307eu3057u305f: {str(e)}"
        log_error("embeddings", error_msg)
        return None, (error_msg, 500)
