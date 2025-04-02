import requests
import json
import argparse

def test_chat_completion(base_url="http://localhost:8080"):
    """
    チャット完了APIのテスト
    """
    print("\n=== チャット完了APIのテスト ===")
    
    # テストリクエスト
    test_request = {
        "model": "gpt-3.5-turbo",  # 実際にはOllamaのモデルが使用される
        "messages": [
            {"role": "system", "content": "あなたは役立つアシスタントです。"},
            {"role": "user", "content": "こんにちは、自己紹介してください。"}
        ],
        "temperature": 0.7
    }
    
    # リクエスト送信
    try:
        response = requests.post(
            f"{base_url}/v1/chat/completions",
            json=test_request,
            headers={"Content-Type": "application/json"}
        )
        
        # レスポンスの確認
        if response.status_code == 200:
            result = response.json()
            print("✅ 成功: チャット完了APIが正常に応答しました")
            print(f"モデル: {result.get('model')}")
            print(f"応答内容: {result.get('choices', [{}])[0].get('message', {}).get('content', '')}")
        else:
            print(f"❌ エラー: ステータスコード {response.status_code}")
            print(f"エラー内容: {response.text}")
    except Exception as e:
        print(f"❌ 例外が発生しました: {str(e)}")

def test_embeddings(base_url="http://localhost:8080"):
    """
    埋め込みAPIのテスト
    """
    print("\n=== 埋め込みAPIのテスト ===")
    
    # テストリクエスト
    test_request = {
        "model": "text-embedding-ada-002",  # 実際にはOllamaのモデルが使用される
        "input": "これは埋め込みテスト用のテキストです。"
    }
    
    # リクエスト送信
    try:
        response = requests.post(
            f"{base_url}/v1/embeddings",
            json=test_request,
            headers={"Content-Type": "application/json"}
        )
        
        # レスポンスの確認
        if response.status_code == 200:
            result = response.json()
            embedding = result.get('data', [{}])[0].get('embedding', [])
            embedding_length = len(embedding)
            print("✅ 成功: 埋め込みAPIが正常に応答しました")
            print(f"モデル: {result.get('model')}")
            print(f"埋め込みベクトルの長さ: {embedding_length}")
            if embedding_length > 0:
                print(f"最初の5つの値: {embedding[:5]}")
        else:
            print(f"❌ エラー: ステータスコード {response.status_code}")
            print(f"エラー内容: {response.text}")
    except Exception as e:
        print(f"❌ 例外が発生しました: {str(e)}")

def test_health(base_url="http://localhost:8080"):
    """
    ヘルスチェックAPIのテスト
    """
    print("\n=== ヘルスチェックAPIのテスト ===")
    
    # リクエスト送信
    try:
        response = requests.get(f"{base_url}/health")
        
        # レスポンスの確認
        if response.status_code == 200:
            result = response.json()
            print("✅ 成功: ヘルスチェックAPIが正常に応答しました")
            print(f"ステータス: {result.get('status')}")
            print(f"メッセージ: {result.get('message')}")
        else:
            print(f"❌ エラー: ステータスコード {response.status_code}")
            print(f"エラー内容: {response.text}")
    except Exception as e:
        print(f"❌ 例外が発生しました: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Secondme API Adapterのテスト')
    parser.add_argument('--url', default='http://localhost:8080', help='アダプターのベースURL')
    parser.add_argument('--test', choices=['all', 'chat', 'embeddings', 'health'], default='all', help='実行するテスト')
    
    args = parser.parse_args()
    
    print(f"Secondme API Adapter ({args.url}) のテストを開始します...")
    
    if args.test in ['all', 'health']:
        test_health(args.url)
    
    if args.test in ['all', 'chat']:
        test_chat_completion(args.url)
    
    if args.test in ['all', 'embeddings']:
        test_embeddings(args.url)
    
    print("\nテスト完了")

if __name__ == "__main__":
    main()
