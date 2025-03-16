@echo off
chcp 65001

rem 記事からプロンプトを生成するテスト
python ..\summarize_article.py ^
    --article test_article.md ^
    --output test_prompt.json ^
    --ollama-model gemma3:4b

echo.
echo テスト完了
pause 