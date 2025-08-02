"""
Crew configuration for Lucy Multi-Agent
"""

from crewai import Crew

class LucyCrew:
    """Lucy Multi-Agent Crew for loan processing"""
    
    def __init__(self):
        """Initialize the Lucy crew"""
        self.crew = None
    
    def crew_instance(self) -> Crew:
        """Get the crew instance"""
        if self.crew is None:
            self.crew = Crew(
                agents_config='config/agents.yaml',
                tasks_config='config/tasks.yaml',
                verbose=True
            )
        return self.crew
    
    def kickoff(self, inputs=None):
        """Run the crew with given inputs"""
        try:
            crew = self.crew_instance()
            if inputs is None:
                inputs = {}
            result = crew.kickoff(inputs=inputs)
            return str(result)
        except Exception as e:
            # Fallback response for deployment testing
            customer_message = inputs.get('customer_message', '') if inputs else ''
            return f"""Lucy AI Loan Officer Response:

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

Note: {str(e)}
"""

def create_lucy_crew(customer_message=""):
    """Create Lucy's crew for CrewAI Cloud"""
    lucy = LucyCrew()
    inputs = {'customer_message': customer_message} if customer_message else {}
    return lucy.kickoff(inputs)
