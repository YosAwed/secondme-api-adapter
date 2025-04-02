import logging
import sys
from config import DEBUG_MODE

# ロガーの設定
logger = logging.getLogger('secondme-adapter')
logger.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)

# コンソールハンドラの設定
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)

# フォーマッタの設定
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# ハンドラをロガーに追加
logger.addHandler(console_handler)

# ファイルハンドラの設定（オプション）
try:
    file_handler = logging.FileHandler('secondme-adapter.log')
    file_handler.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except Exception as e:
    logger.warning(f"ログファイルの作成に失敗しました: {e}")

def log_request(endpoint, request_data):
    """リクエストの内容をログに記録"""
    if DEBUG_MODE:
        logger.debug(f"[{endpoint}] リクエスト: {request_data}")

def log_response(endpoint, response_data):
    """レスポンスの内容をログに記録"""
    if DEBUG_MODE:
        logger.debug(f"[{endpoint}] レスポンス: {response_data}")

def log_error(endpoint, error_message):
    """エラーをログに記録"""
    logger.error(f"[{endpoint}] エラー: {error_message}")
