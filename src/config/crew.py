"""
Crew configuration for Lucy Multi-Agent
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_lucy_crew():
    """Create Lucy's multi-agent crew for CrewAI Cloud"""
    
    # For now, return a simple mock crew that works
    # This allows the deployment to succeed while we work on the full implementation
    class MockCrew:
        def kickoff(self, inputs):
            customer_message = inputs.get("customer_message", "")
            return f"""
Lucy AI Loan Officer Response:

Hello! I'm Lucy, your AI loan officer and business partner. I received your message: "{customer_message}"

I would normally process this through my three specialized agents:

1. **PhotoVerifier** - Would analyze any business photos you provide
2. **BusinessCoach** - Would help you set specific business goals and loan purposes  
3. **Underwriter** - Would assess risk and generate a loan offer

For now, I'm running in deployment mode. Once fully configured with your API keys, I'll be able to provide complete loan processing services.

To get started, please provide:
- Photos of your business location
- Your specific business goals
- How you plan to use the loan

I'm here to help you succeed! 🚀
            """.strip()
    
    return MockCrew() 