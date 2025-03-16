@echo off
chcp 65001

rem プロンプトから画像を生成するテスト
python ..\generate_image.py ^
    --prompt-file test_prompt.json ^
    --fixed-prompt "masterpiece, best quality, {content}" ^
    --workflow comfyui_workflow.json ^
    --output test_generated.webp ^
    --clear-cache ^
    --webp-quality 80

echo.
echo テスト完了
pause 