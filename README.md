# Lucy - AI Loan Officer & Business Partner

Multi-agent prototype using CrewAI with support for multiple LLM providers.

## 🚀 Features

- **Multi-LLM Support**: OpenAI, Anthropic Claude, Google Gemini
- **Observability**: Langfuse integration for tracking and monitoring
- **Three Specialized Agents**: Photo Verifier, Business Coach, Underwriter
- **Complete Workflow**: From photo verification to loan offer generation
- **Flexible Configuration**: Easy switching between LLM providers

## 📋 Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Configure API keys in `.env` file (already configured)
3. Set `LLM_PROVIDER` to your preferred provider (openai, anthropic, gemini)

## 🧪 Testing

Test all providers: `python simple_lucy.py`
Run demo: `python demo.py`

## 📊 Observability

All agent interactions are tracked in Langfuse:
- https://us.cloud.langfuse.com

## 🔧 Usage

```python
from simple_lucy import LucyAgent

# Initialize with your preferred provider
lucy = LucyAgent('openai')  # or 'anthropic', 'gemini'

# Run the complete workflow
result = lucy.run_lucy_workflow('Hi, I need a loan for my shop')
```

## 📁 Project Structure

- `simple_lucy.py` - Main working implementation
- `demo.py` - Interactive demo with conversation flow
- `crew.py` - Original CrewAI implementation (has dependency issues)
- `.env` - API keys configuration
- `requirements.txt` - Python dependencies
