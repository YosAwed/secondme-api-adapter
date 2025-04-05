# Secondme API Adapter

[English](#english) | [日本語](#japanese)

<a id="english"></a>
# Setup Guide for Using Ollama with Second Me

## Overview
This adapter provides OpenAI-compatible API endpoints for Ollama, enabling seamless integration with Second Me.

## Prerequisites
- Ollama installed and running locally
- Llama 3.2 model downloaded in Ollama
- Python installed
- Second Me set up

## Quick Start

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Start the adapter:
```bash
python secondme_api_adapter.py
```

The adapter will start on `http://localhost:8080`.

## Configuration

### Second Me Settings
Update Second Me's configuration to use the adapter:
```
OPENAI_API_BASE=http://localhost:8080
OPENAI_API_KEY=dummy  # Any value works
```

### Model Configuration
Modify `config.py` to change the models:
```python
CHAT_MODEL_NAME = "llama3.2"           # Model for chat
EMBEDDING_MODEL_NAME = "nomic-embed-text"  # Model for embeddings
```

## Troubleshooting

### API Format Issues
Check the conversion logic in `adapters.py` if you encounter response format issues.

### Error Logging
If problems occur:
1. Check the adapter's console output
2. Enable debug mode in `config.py`
3. Test endpoints directly using curl

### Comparison with litellm
Unlike litellm, this adapter is specifically customized for Ollama models, offering better control when needed.

## Advanced Features
Possible enhancements:
- Streaming response support
- Multi-model support
- Accurate token counting
- Enhanced error handling

---

<a id="japanese"></a>
# Second MeでOllamaを使用するためのセットアップガイド

## 概要
このアダプターは、OllamaのAPIをOpenAI互換のエンドポイントとして提供し、Second Meとの連携を可能にします。

## 前提条件
- Ollamaがインストールされており、ローカルで実行されていること
- Llama 3.2モデルがOllamaにダウンロードされていること
- Pythonがインストールされていること
- Second Meがセットアップされていること

## クイックスタート

1. 必要なパッケージをインストール:
```bash
pip install -r requirements.txt
```

2. アダプターを起動:
```bash
python secondme_api_adapter.py
```

アダプターは`http://localhost:8080`で起動します。

## 設定

### Second Meの設定
Second Meの設定を以下のように変更します:
```
OPENAI_API_BASE=http://localhost:8080
OPENAI_API_KEY=dummy  # 任意の値で構いません
```

### モデルの設定
`config.py`でモデルを変更できます:
```python
CHAT_MODEL_NAME = "llama3.2"           # チャット用モデル
EMBEDDING_MODEL_NAME = "nomic-embed-text"  # 埋め込み用モデル
```

## トラブルシューティング

### API形式の問題
レスポンス形式に問題がある場合は、`adapters.py`の変換ロジックを確認してください。

### エラーログ
問題が発生した場合:
1. アダプターのコンソール出力を確認
2. `config.py`でデバッグモードを有効化
3. curlを使用して直接エンドポイントをテスト

### litellmとの比較
litellmと異なり、このアダプターは特定のOllamaモデル用にカスタマイズされており、必要な場合により細かい制御が可能です。

## 高度な機能
実装可能な拡張機能:
- ストリーミングレスポンスのサポート
- 複数モデルのサポート
- トークン数の正確な計算
- エラーハンドリングの改善
