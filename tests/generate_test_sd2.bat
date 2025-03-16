@echo off
chcp 65001

rem プロンプトから画像を生成するテスト
python ..\generate_image.py ^
    --prompt-file test_prompt.json ^
    --fixed-prompt "masterpiece, best quality, amazing quality, very aesthetic, high resolution, absurdres, scenery, (anime style, faily style:1), beautiful adult 1girl, silver hair, medium hair, bob cut, blue eyes, medium breasts, BREAK, {content}" ^
    --workflow comfyui_workflow.json ^
    --output test_generated.webp ^
    --clear-cache ^
    --webp-quality 80

rem 生成した画像をリサイズ
python ..\resize_image.py ^
    --input test_generated.webp ^
    --output test_generated_1280x670.webp ^
    --width 1280 ^
    --height 670 ^
    --quality 80

echo.
echo テスト完了
pause 