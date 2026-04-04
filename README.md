# HuggingFace Daily Papers Slack App

HuggingFace の [Daily Papers](https://huggingface.co/papers) から最新論文を取得し、GPT で日本語要約して Slack に投稿するボット。

平日朝 9 時（JST）に GitHub Actions で自動実行されます。

## 動作イメージ

各論文について以下の形式で Slack に投稿されます：

```
*論文タイトル*
https://huggingface.co/papers/xxxx.xxxxx

*どんなもの？*
...

*先行研究と比べてどこがすごい？*
...

*技術や手法のキモはどこ？*
...

*どうやって有効だと検証した？*
...

*議論はある？*
...

*次に読むべき論文は？*
...
```

## セットアップ

### 必要なもの

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- OpenAI API キー
- Slack Incoming Webhook URL

### インストール

```bash
git clone https://github.com/kazumasa-okamoto/daily-papers-slackapp
cd daily-papers-slackapp
uv venv
source .venv/bin/activate
uv sync
```

### 環境変数の設定

`.env.example` をコピーして `.env` を作成し、値を設定します：

```bash
cp .env.example .env
```

```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx/yyy/zzz
OPENAI_API_KEY=sk-xxxxxxxx
```

### 実行

```bash
uv run python main.py
```

## GitHub Actions による自動実行

`.github/workflows/bot.yml` により、平日（月〜金）の 00:00 UTC（= 朝 9:00 JST）に自動実行されます。

手動実行は Actions タブの `workflow_dispatch` から可能です。

### Secrets の設定

リポジトリの Settings > Secrets and variables > Actions に以下を追加してください：

| Secret 名 | 説明 |
|---|---|
| `SLACK_WEBHOOK_URL` | Slack の Incoming Webhook URL |
| `OPENAI_API_KEY` | OpenAI API キー |
