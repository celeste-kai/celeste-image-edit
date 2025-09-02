# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

This is `celeste-image-edit`, a specialized domain package in the Celeste multi-modal AI framework that provides image editing capabilities across multiple providers (OpenAI, Google, Replicate).

### Architecture

- **Package Layout**: Follows src/ layout with `celeste_image_edit/` as the main module
- **Provider Pattern**: Uses factory pattern via `create_image_editor()` function
- **Base Class**: All providers inherit from `BaseImageEditor` (from `celeste-core`)
- **Capability Mapping**: Defined in `mapping.py` linking providers to implementation classes

### Key Components

- `__init__.py`: Main entry point with `create_image_editor()` factory function
- `mapping.py`: Provider-to-implementation mapping and capability definition
- `providers/`: Provider-specific implementations
  - `google.py`: Google Gemini image editing via `genai` client
  - `openai.py`: OpenAI image editing via their API
  - `replicate.py`: Replicate image editing with dynamic input key handling

## Development Commands

### Setup
```bash
uv add -e .                    # Install package in editable mode
```

### Testing
```bash
python example.py              # Run Streamlit demo app
streamlit run example.py       # Alternative way to run demo
```

### Dependencies
- Core dependency: `celeste-core` (via git)
- Provider SDKs: `google-genai`, `replicate`, `openai` (inherited from core)
- Image handling: `Pillow` for image processing

## Provider Implementation Notes

### Google Provider
- Uses `gemini-2.0-flash-preview-image-generation` model by default
- Handles both file paths and raw bytes via PIL
- Returns `ImageArtifact` with model metadata and token usage

### OpenAI Provider  
- Uses `gpt-image-1` model by default
- Requires file-like objects with name attributes for MIME detection
- Supports size and quality parameters
- Returns base64-decoded image data

### Replicate Provider
- Uses `black-forest-labs/flux-kontext-pro` model by default
- Smart input key detection across common parameter names
- Handles various output formats (URLs, file objects, lists)
- Robust fallback mechanism for different model input schemas

## Key Patterns

### ImageArtifact Handling
All providers work with `ImageArtifact` objects that can contain either:
- `path`: File path to image (including HTTP URLs for Replicate)
- `data`: Raw bytes of image data

### Error Handling
- Non-raising validation via `supports()` function from registry
- Providers store `is_supported` flag for caller inspection
- Empty `ImageArtifact` returned when provider fails gracefully

### Async Pattern
All `edit_image()` methods are async, with sync operations wrapped using `asyncio.to_thread()` when needed.