# GenerateNoteImageFromComfyUI

Generate images from article text using ComfyUI and ollama.

## Overview

This program generates images from article text by:

1. Using ollama to analyze the article and generate image prompts
2. Combining the generated prompts with fixed prompts
3. Using ComfyUI's API to generate images

## Requirements

- Python 3.x
- ComfyUI (running)
- ollama (will be automatically started if not running)

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python article_to_image.py \
  --article <path_to_article.md> \
  --prompt "your_fixed_prompt {content}" \
  --workflow <path_to_workflow.json> \
  --clear-cache \
  --ollama-model <model_name>
```

### Parameters

- `--article`: Path to the Markdown article file
- `--prompt`: Fixed prompt template. Use `{content}` where you want to insert the generated prompt
- `--workflow`: Path to ComfyUI workflow JSON file
  - The workflow must have an "InputPrompt" node to receive the prompt text
- `--clear-cache`: (Optional) Clear ComfyUI cache before generation
- `--ollama-model`: (Optional) Specify ollama model (default: gemma3:4b)

### Example

```bash
python article_to_image.py \
  --article article.md \
  --prompt "photorealistic, high quality, detailed, {content}" \
  --workflow workflow.json \
  --clear-cache \
  --ollama-model gemma3:4b
```

### Available Models

You can choose different ollama models based on your VRAM capacity:

- `gemma3:1b` (815MB VRAM) - Lightweight
- `gemma3:4b` (3.3GB VRAM) - Default, balanced
- `gemma3:12b` (8.1GB VRAM) - High quality
- `gemma3:27b` (17GB VRAM) - Best quality

## Output

- Generated images are saved in WebP format
- Output filename: `<article_filename>.webp`
- Images are saved in the same directory as the article file

## Error Handling

The program will stop and display an error message if any errors occur during execution.

## Testing

Run the test script in the `tests` directory:

```bash
cd tests
run_test.bat
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.