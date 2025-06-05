<h1 align="center">Claude Code MCP Server</h1>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.12+-blue.svg" alt="Python Version"/>
    <img src="https://img.shields.io/badge/MCP-Protocol-green.svg" alt="MCP Protocol"/>
    <img src="https://img.shields.io/badge/Claude-Code-orange.svg" alt="Claude Code"/>
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"/>
</p>

<p align="center">
    Claude Code を MCP (Model Context Protocol) サーバーとしてラップし、Claude などのMCPクライアントから利用可能にします。
</p>

## 🚀 機能

このMCPサーバーは以下のツールを提供します：

- **`claude_code_query`**: Claude Code にプロンプトを送り、コード生成・説明・デバッグなどを実行
- **`claude_code_status`**: Claude Code のインストール状況やバージョン確認

## 🔌 サポートモード

- **SSE モードのみ対応**: Server-Sent Events を使用（Web API用）

## 📋 前提条件

1. **Claude Code**: 
   ```bash
   pip install --upgrade anthropic[code]
   # または公式ドキュメント参照
   ```

2. **Python 3.12以上**

3. **環境設定**: `.env.example` を `.env` にコピーして設定を行ってください（必要に応じて）

## 🛠️ インストール

### 1. リポジトリのクローン
```bash
git clone https://github.com/Tomatio13/claude-code-mcp.git
cd claude-code-mcp
```

### 2. セットアップ
```bash
./setup.sh
```

### 3. サーバーの起動

#### SSE モード（Web API用）
```bash
./run_sse.sh [ポート] [ホスト]

# 例:
./run_sse.sh 8080 0.0.0.0  # ポート8080、全てのインターフェースでリッスン
./run_sse.sh              # デフォルト: localhost:8000
```

#### 手動起動
```bash
python claude_code_server.py --mode sse --port 8000 --host localhost
```

### 手動インストール
```bash
pip install -e .
python claude_code_server.py
```

## 💡 使用方法

Claude Code MCPサーバーが起動したら、MCPクライアント（例: Claude Desktop, Web UI等）から以下のようにツールを利用できます：

### 基本的なクエリ
```
@claude-code claude_code_query prompt="このコードベースの構造を説明して"
```

### モデルや出力形式の指定
```
@claude-code claude_code_query prompt="PythonでREST APIを作成" model="opus" output_format="json"
```

### ステータス確認
```
@claude-code claude_code_status
```

## 🎯 パラメータ例

- `prompt` : Claude Code への指示文
- `model` : 使用するモデル（例: sonnet, opus, claude-sonnet-4-20250514 など）
- `output_format` : 出力形式（text, json, stream-json）

## 🛡️ セキュリティ

- ファイル操作やコマンド実行はClaude Code の仕様に準拠
- サーバーはSSEモードのみ対応
- ファイル操作は作業ディレクトリ内に制限

## 🐛 トラブルシューティング

### よくある問題

1. **"claude command not found"**
   ```bash
   pip install --upgrade anthropic[code]
   # または公式ドキュメント参照
   ```

2. **スクリプトの実行権限エラー**
   ```bash
   chmod +x *.sh
   ```

3. **Pythonバージョンの問題**
   - Python 3.12以上がインストールされていることを確認
   - 仮想環境を使用: `python3 -m venv venv && source venv/bin/activate`

4. **MCP接続の問題**
   - クライアント設定ファイルの構文を確認
   - ファイルパスが絶対パスであることを確認
   - 設定変更後にクライアントを再起動

## 📝 ライセンス

MIT License with Attribution - 詳細は [LICENSE](LICENSE) ファイルをご覧ください。

## 🤝 貢献

貢献を歓迎します！プルリクエストをお気軽に送信してください。

## 📞 サポート

問題が発生した場合や質問がある場合は、GitHubでissueを開いてください。

---

<p align="center">
    Claude + Claude Code コミュニティのために ❤️ で作成
</p>

# Check if claude CLI is available
if ! command -v claude &> /dev/null; then
    echo "❌ Error: 'claude' command not found"
    echo "Please install Claude Code:"
    echo "  pip install --upgrade anthropic[code]"
    exit 1
fi