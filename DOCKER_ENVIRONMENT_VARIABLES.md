# Docker Environment Variables for Presento

This document lists all environment variables that can be configured for Presento when deploying with Docker, Docker Compose, or Coolify.

> **Template Model Configuration customized by [FutureForge Studios Private Limited](https://ffstudios.io)**

## Required Environment Variables

### Core Configuration
- `CAN_CHANGE_KEYS` - Set to `false` to hide API keys in the UI (recommended for production)
- `DATABASE_URL` - Database connection string (optional, defaults to SQLite)

## LLM Provider Configuration

### Main LLM Provider
- `LLM` - Choose your LLM provider: `openai`, `google`, `anthropic`, `ollama`, or `custom`

### OpenAI Configuration
- `OPENAI_API_KEY` - Your OpenAI API key (required if `LLM=openai`)
- `OPENAI_MODEL` - OpenAI model to use (default: `gpt-4o`)

### Google Configuration
- `GOOGLE_API_KEY` - Your Google API key (required if `LLM=google`)
- `GOOGLE_MODEL` - Google model to use (default: `models/gemini-2.0-flash`)

### Anthropic Configuration
- `ANTHROPIC_API_KEY` - Your Anthropic API key (required if `LLM=anthropic`)
- `ANTHROPIC_MODEL` - Anthropic model to use (default: `claude-3-5-sonnet-20241022`)

### Ollama Configuration (Local Models)
- `OLLAMA_URL` - Ollama server URL (default: `http://localhost:11434`)
- `OLLAMA_MODEL` - Ollama model to use (e.g., `llama3.1`, `qwen2.5`, `mistral`)

### Custom LLM Configuration
- `CUSTOM_LLM_URL` - Your custom OpenAI-compatible API URL (required if `LLM=custom`)
- `CUSTOM_LLM_API_KEY` - API key for your custom LLM (if required)
- `CUSTOM_MODEL` - Model name for your custom LLM

## Template Generation Configuration

### Template Model Provider
- `TEMPLATE_LLM_PROVIDER` - Choose template generation model:
  - `local` - Use the same model as content generation (default for local models)
  - `api` - Always use OpenAI GPT-5 for template generation (default for API models)

## Image Generation Configuration

### Image Provider
- `IMAGE_PROVIDER` - Choose image provider: `pexels`, `pixabay`, `gemini_flash`, or `dall-e-3`
- `PEXELS_API_KEY` - Pexels API key (required if using Pexels)
- `PIXABAY_API_KEY` - Pixabay API key (required if using Pixabay)

## Advanced LLM Configuration

### Tool Calls and Reasoning
- `TOOL_CALLS` - Enable/disable tool calls for custom LLMs (`true`/`false`)
- `DISABLE_THINKING` - Disable thinking mode for custom LLMs (`true`/`false`)
- `EXTENDED_REASONING` - Enable extended reasoning (`true`/`false`)

### Web Search
- `WEB_GROUNDING` - Enable web search for OpenAI, Google, and Anthropic models (`true`/`false`)

## Optional Configuration

### Tracking
- `DISABLE_ANONYMOUS_TRACKING` - Disable anonymous usage tracking (`true`/`false`)

## Example Docker Compose Configuration

```yaml
version: '3.8'

services:
  presenton:
    build: .
    ports:
      - "5000:80"
    volumes:
      - ./app_data:/app_data
    environment:
      # Core Configuration
      CAN_CHANGE_KEYS: false
      DATABASE_URL: sqlite:///app_data/presenton.db
      
      # LLM Configuration (choose one)
      LLM: ollama
      OLLAMA_MODEL: llama3.1
      OLLAMA_URL: http://localhost:11434
      
      # Template Generation
      TEMPLATE_LLM_PROVIDER: local
      
      # Image Generation
      IMAGE_PROVIDER: dall-e-3
      
      # Advanced Options
      WEB_GROUNDING: false
      DISABLE_ANONYMOUS_TRACKING: true
```

> **Note**: The project includes both `docker-compose.yml` (legacy format) and `docker-compose.yaml` (modern format) files. Use `docker-compose.yaml` for new deployments.

## Example Coolify Environment Variables

When deploying with Coolify, set these environment variables in your project settings:

### For Local Ollama Setup:
```
LLM=ollama
OLLAMA_MODEL=llama3.1
OLLAMA_URL=http://ollama:11434
TEMPLATE_LLM_PROVIDER=local
CAN_CHANGE_KEYS=false
```

### For OpenAI Setup:
```
LLM=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
TEMPLATE_LLM_PROVIDER=api
CAN_CHANGE_KEYS=false
```

### For Custom LLM Setup:
```
LLM=custom
CUSTOM_LLM_URL=https://your-custom-llm-api.com/v1
CUSTOM_LLM_API_KEY=your_api_key_here
CUSTOM_MODEL=your-model-name
TEMPLATE_LLM_PROVIDER=local
CAN_CHANGE_KEYS=false
```

## Template Generation Behavior

### Default Behavior
- **Local Models** (Ollama/Custom): Automatically uses the same model for template generation
- **API Models** (OpenAI/Google/Anthropic): Uses OpenAI GPT-5 for template generation

### Explicit Configuration
- `TEMPLATE_LLM_PROVIDER=local`: Forces use of the same model as content generation
- `TEMPLATE_LLM_PROVIDER=api`: Forces use of OpenAI GPT-5 for template generation

## Performance Considerations

### Local Models
- **Pros**: Privacy, no API costs, consistent with content generation
- **Cons**: Slower template generation (5+ minutes per slide), requires sufficient resources
- **Best for**: Privacy-focused deployments, cost-sensitive environments

### API Models
- **Pros**: Faster template generation, potentially better quality
- **Cons**: API costs, requires internet connectivity, data sent to external service
- **Best for**: Production deployments, when speed is important

## Troubleshooting

### Common Issues

1. **Template Generation Fails**
   - Ensure your local model supports vision/image processing
   - Check that the model has sufficient context length
   - Verify the model is running and accessible

2. **Environment Variables Not Working**
   - Ensure variables are set in the correct format
   - Check for typos in variable names
   - Restart the container after changing environment variables

3. **Model Not Found**
   - For Ollama: Ensure the model is installed (`ollama pull model-name`)
   - For Custom: Verify the model name matches your API configuration

### Debug Information

The application logs which model is being used:
```
Using local model for template generation
Making LLM request for HTML generation using model: llama3.1
```

or

```
Using API model (OpenAI GPT-5) for template generation
Making Responses API request for HTML generation...
```

## Security Notes

- Set `CAN_CHANGE_KEYS=false` in production to prevent API key exposure
- Use environment variables instead of hardcoding sensitive information
- Consider using Docker secrets for sensitive data in production
- Regularly rotate API keys and update environment variables

## Support

For issues with Docker deployment:
1. Check container logs for error messages
2. Verify all required environment variables are set
3. Ensure your model is properly installed and accessible
4. Test with a simple configuration first

For additional support, refer to the main Presento documentation or create an issue in the project repository.
