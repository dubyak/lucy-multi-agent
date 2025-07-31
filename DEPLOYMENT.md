# 🚀 Lucy CrewAI Cloud Deployment Guide

## Prerequisites

1. **CrewAI Cloud Account**: Sign up at [app.crewai.com](https://app.crewai.com)
2. **Working Lucy Setup**: All three LLM providers tested and working
3. **API Keys**: Configured in `.env` file

## Deployment Steps

### 1. Create CrewAI Cloud Account
- Go to [app.crewai.com](https://app.crewai.com)
- Sign up with your email
- Complete device-code authentication

### 2. Install CrewAI CLI (if available)
```bash
pip install crewai-cli
```

### 3. Login to CrewAI Cloud
```bash
crewai login
```

### 4. Deploy Lucy Crew
```bash
# Set your API key
export CREWAI_API_KEY=your_crewai_api_key

# Deploy the crew
crewai deploy create --file crewai_cloud_lucy.py
```

### 5. Alternative: Manual Deployment
If CLI doesn't work, you can:

1. **Upload via Web UI**:
   - Go to [app.crewai.com](https://app.crewai.com)
   - Click "Create New Crew"
   - Upload `crewai_cloud_lucy.py`
   - Configure environment variables

2. **Set Environment Variables**:
   ```
   LLM_PROVIDER=openai
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Testing Your Deployment

### 1. Local Test First
```bash
python crewai_cloud_lucy.py
```

### 2. CrewAI Cloud Test
- Go to your deployment in CrewAI Cloud
- Click "Run"
- Test with: "Hi, I need a loan for my small shop in Nairobi"

## Expected Results

Your Lucy crew should:
1. **Photo Verification Agent**: Request shop photos and location
2. **Business Coach**: Guide through goal-setting process
3. **Underwriter**: Assess eligibility and generate loan offer

## Monitoring

- **CrewAI Cloud**: Built-in tracing and monitoring
- **Langfuse**: Additional observability at https://us.cloud.langfuse.com

## Troubleshooting

### Common Issues:
1. **API Key Errors**: Ensure all API keys are valid
2. **Dependency Issues**: Use `fixed_lucy.py` for local testing
3. **Deployment Failures**: Check CrewAI Cloud logs

### Fallback Options:
- Use `simple_lucy.py` for local development
- Use `fixed_lucy.py` for testing all providers
- Use `demo.py` for interactive testing

## Next Steps

1. **Deploy to CrewAI Cloud**
2. **Test with real conversations**
3. **Monitor performance in Langfuse**
4. **Iterate and improve agents**

## Support

- **CrewAI Documentation**: https://docs.crewai.com
- **Langfuse Dashboard**: https://us.cloud.langfuse.com
- **Local Testing**: Use `python fixed_lucy.py` 