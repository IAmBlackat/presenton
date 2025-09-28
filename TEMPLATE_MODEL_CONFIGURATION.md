# Template Model Configuration

This document explains the new template model configuration feature that allows you to choose between using local/self-hosted models or API-based models for slide template generation.

> **Customized by [FutureForge Studios Private Limited](https://ffstudios.io)**

## Overview

Previously, Presento only supported using OpenAI's GPT-5 Responses API for generating custom slide templates from uploaded files. Now, you can choose to use the same local/self-hosted model that you're using for content generation, or continue using the API-based approach.

## Configuration Options

### Environment Variable

You can set the `TEMPLATE_LLM_PROVIDER` environment variable to control template generation:

```bash
# Use local model (same as content generation)
TEMPLATE_LLM_PROVIDER=local

# Use API model (OpenAI GPT-5)
TEMPLATE_LLM_PROVIDER=api
```

### Default Behavior

- If `TEMPLATE_LLM_PROVIDER` is not set:
  - **Local models** (Ollama, Custom): Defaults to using the same local model
  - **API models** (OpenAI, Google, Anthropic): Defaults to using OpenAI GPT-5 for templates

### UI Configuration

You can also configure this through the Presento settings UI:

1. Go to Settings → LLM Configuration
2. Scroll down to the "Template Generation Model" section
3. Choose between:
   - **Use same model as content generation**: Uses your configured LLM provider
   - **Always use OpenAI GPT-5 (API)**: Forces API-based template generation

## How It Works

### Template Generation Process

When you upload a file to create a custom template, Presento goes through these steps:

1. **Slide Extraction**: Extracts slides from your PDF/PPTX file
2. **HTML Generation**: Converts each slide to HTML using the configured model
3. **React Component Generation**: Converts HTML to React components using the configured model
4. **Template Creation**: Saves the components as a reusable template

### Model Selection Details

**For Local Models (Ollama/Custom):**
- Uses the **exact model you have installed** (e.g., `llama3.1`, `qwen2.5`, `mistral`, etc.)
- The model name is retrieved from your configuration (`OLLAMA_MODEL` or `CUSTOM_MODEL`)
- Template generation will use the same model instance as content generation
- If you change your model configuration, template generation will automatically use the new model

**For API Models:**
- Uses OpenAI's GPT-5 Responses API regardless of your content generation model
- Provides consistent, high-quality results for template generation
- Requires internet connectivity and API key

### Model Selection Logic

The system uses the following logic to determine which model to use:

```python
def get_template_llm_provider():
    template_provider_setting = get_template_llm_provider_env()
    content_provider = get_llm_provider()
    
    # If explicitly set to use API (OpenAI GPT-5 Responses API)
    if template_provider_setting == "api":
        return LLMProvider.OPENAI
    
    # If explicitly set to use local model
    if template_provider_setting == "local":
        return content_provider
    
    # Default behavior: use local if content generation uses local, otherwise use API
    if content_provider in [LLMProvider.OLLAMA, LLMProvider.CUSTOM]:
        return content_provider
    else:
        return LLMProvider.OPENAI
```

## Use Cases

### When to Use Local Models

- **Privacy**: Keep your slide content private and not send it to external APIs
- **Cost**: Avoid API costs for template generation
- **Consistency**: Use the same model for both content and template generation
- **Offline**: Work without internet connectivity
- **Specific Model**: Uses the exact model you have installed and configured (e.g., `llama3.1`, `qwen2.5`, etc.)

### When to Use API Models

- **Speed**: OpenAI GPT-5 is typically faster for complex template generation
- **Quality**: May provide better results for complex slide layouts
- **Reliability**: More stable for production use

## Performance Considerations

### Local Models
- **Pros**: Privacy, cost-effective, consistent with content generation
- **Cons**: May be slower, requires sufficient local resources
- **Time**: Template generation can take 5+ minutes per slide

### API Models
- **Pros**: Faster, potentially better quality, more reliable
- **Cons**: Requires internet, API costs, data sent to external service
- **Time**: Typically faster than local models

## Configuration Examples

### Example 1: Full Local Setup
```bash
# Use Ollama for everything
LLM=ollama
OLLAMA_MODEL=llama3.1
TEMPLATE_LLM_PROVIDER=local
```

### Example 2: Hybrid Setup
```bash
# Use local model for content, API for templates
LLM=ollama
OLLAMA_MODEL=llama3.1
TEMPLATE_LLM_PROVIDER=api
```

### Example 3: Full API Setup
```bash
# Use OpenAI for everything
LLM=openai
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4
TEMPLATE_LLM_PROVIDER=api
```

## Technical Implementation

### Backend Changes

1. **New Configuration**: Added `TEMPLATE_LLM_PROVIDER` to user configuration
2. **Utility Functions**: Created `template_llm_provider.py` for model selection logic
3. **LLM Client Integration**: Modified template generation to use the flexible LLM client
4. **Fallback Support**: Maintains backward compatibility with existing API-based approach

### Frontend Changes

1. **UI Configuration**: Added template model selection to settings
2. **Type Definitions**: Updated TypeScript interfaces
3. **User Experience**: Clear explanation of options and implications

### API Endpoints Modified

- `/api/v1/ppt/slide-to-html/`: Now supports both local and API models
- `/api/v1/ppt/html-to-react/`: Now supports both local and API models

## Migration Guide

### From Previous Version

No migration is required. The system defaults to the most appropriate model based on your current configuration:

- If using local models: Templates will use local models by default
- If using API models: Templates will use OpenAI GPT-5 by default

### Changing Configuration

1. **Via Environment Variables**: Set `TEMPLATE_LLM_PROVIDER` and restart the application
2. **Via UI**: Use the settings interface to change the configuration
3. **Via Configuration File**: Update the user configuration file directly

## Troubleshooting

### Common Issues

1. **Template Generation Fails with Local Model**
   - Ensure your local model supports vision/image processing
   - Check that the model has sufficient context length
   - Verify the model is running and accessible

2. **Slow Template Generation**
   - This is normal for local models (5+ minutes per slide)
   - Consider using API models for faster generation
   - Ensure your system has sufficient resources

3. **API Errors with Local Configuration**
   - Check that `TEMPLATE_LLM_PROVIDER` is set correctly
   - Verify your local model configuration
   - Check logs for specific error messages

### Debug Information

The system logs which model is being used for template generation:

```
Using local model for template generation
Making LLM request for HTML generation using model: llama3.1
```

or

```
Using API model (OpenAI GPT-5) for template generation
Making Responses API request for HTML generation...
```

## Future Enhancements

Potential future improvements:

1. **Model-Specific Optimizations**: Optimize prompts for different model types
2. **Quality Metrics**: Compare template quality between different models
3. **Batch Processing**: Process multiple slides in parallel
4. **Caching**: Cache generated templates to avoid regeneration
5. **Model Recommendations**: Suggest optimal models based on slide complexity

## Support

If you encounter issues with template model configuration:

1. Check the application logs for error messages
2. Verify your model configuration is correct
3. Test with a simple slide first
4. Consider switching between local and API models to isolate issues

For additional support, please refer to the main Presento documentation or create an issue in the project repository.
