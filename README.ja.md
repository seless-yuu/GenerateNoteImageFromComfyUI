# GenerateNoteImageFromComfyUI

ComfyUIとollamaを使用して記事文章から画像を生成するプログラム

## 概要

このプログラムは以下の手順で記事文章から画像を生成します：
1. ollamaを使用して記事を分析し、画像生成用のプロンプトを生成
2. 生成されたプロンプトと固定プロンプトを結合
3. ComfyUIのAPIを使用して画像を生成

## 必要環境

- Python 3.x
- ComfyUI（起動済みであること）
- ollama（未起動の場合は自動的に起動されます）

## インストール

1. このリポジトリをクローン
2. 依存パッケージのインストール：
```bash
pip install -r requirements.txt
```

## 使用方法

```bash
python article_to_image.py \
  --article <記事ファイルのパス.md> \
  --prompt "固定プロンプト {content}" \
  --workflow <ワークフローファイルのパス.json> \
  --clear-cache \
  --ollama-model <モデル名>
```

### パラメータ

- `--article`: Markdown形式の記事ファイルのパス
- `--prompt`: 固定プロンプトのテンプレート。`{content}`の部分に生成されたプロンプトが挿入されます
- `--workflow`: ComfyUIのワークフローJSONファイルのパス
  - ワークフローには"InputPrompt"ノードが含まれている必要があります
- `--clear-cache`: （オプション）生成前にComfyUIのキャッシュをクリア
- `--ollama-model`: （オプション）使用するollamaモデルを指定（デフォルト: gemma3:4b）

### 使用例

```bash
python article_to_image.py \
  --article article.md \
  --prompt "photorealistic, high quality, detailed, {content}" \
  --workflow workflow.json \
  --clear-cache \
  --ollama-model gemma3:4b
```

### 利用可能なモデル

VRAMの容量に応じて以下のollamaモデルを選択できます：
- `gemma3:1b` (VRAM 815MB) - 軽量
- `gemma3:4b` (VRAM 3.3GB) - デフォルト、バランス型
- `gemma3:12b` (VRAM 8.1GB) - 高品質
- `gemma3:27b` (VRAM 17GB) - 最高品質

## 出力

- 生成された画像はWebP形式で保存されます
- 出力ファイル名：`<記事ファイル名>.webp`
- 画像は記事ファイルと同じディレクトリに保存されます

## エラー処理

実行中にエラーが発生した場合、プログラムは停止しエラーメッセージを表示します。

## テスト

`tests`ディレクトリのテストスクリプトを実行：
```bash
cd tests
run_test.bat
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています - 詳細は[LICENSE](LICENSE)ファイルを参照してください。 