"""
Crew configuration for Lucy Multi-Agent
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Load environment variables
load_dotenv()

def get_llm():
    """Get the appropriate LLM based on environment configuration"""
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    try:
        if provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment")
            return ChatAnthropic(
                model="claude-3-5-sonnet-20241022",
                api_key=api_key
            )
        elif provider == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment")
            return ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key
            )
        else:  # default to OpenAI
            from langchain_openai import ChatOpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment")
            return ChatOpenAI(
                model="gpt-4o-mini",
                api_key=api_key
            )
    except Exception as e:
        print(f"Error setting up LLM: {e}")
        return None

def create_lucy_crew(customer_message=""):
    """Create Lucy's multi-agent crew for CrewAI Cloud"""
    
    # Get LLM
    llm = get_llm()
    if not llm:
        raise ValueError("Could not initialize LLM. Please check your API keys.")
    
    # Initialize Langfuse for observability (optional)
    langfuse = None
    try:
        from langfuse import Langfuse
        langfuse = Langfuse(
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            host=os.getenv("LANGFUSE_HOST", "https://us.cloud.langfuse.com")
        )
    except Exception as e:
        print(f"Warning: Could not initialize Langfuse: {e}")
    
    # Create specialized agents
    photo_verifier = Agent(
        role="Photo Verification Specialist",
        goal="Analyze business photos to verify business legitimacy and assess visual risk factors",
        backstory="""You are an expert in analyzing business photographs to verify business legitimacy. 
        You can identify business locations, assess visual risk factors, and determine if photos support 
        loan applications. You're trained to spot red flags and validate business claims through visual evidence.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    business_coach = Agent(
        role="Business Development Coach",
        goal="Help customers set specific business goals and determine optimal loan purposes",
        backstory="""You are an experienced business coach who helps small business owners clarify their goals 
        and determine the best use of loan funds. You ask probing questions to understand business needs, 
        help set SMART goals, and ensure loan purposes align with business growth strategies.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    underwriter = Agent(
        role="Loan Underwriter",
        goal="Assess credit risk and generate appropriate loan offers based on business analysis",
        backstory="""You are a senior loan underwriter with expertise in small business lending. 
        You analyze business information, assess risk factors, and generate loan offers that balance 
        customer needs with risk management. You're known for fair assessments and creative solutions.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Create tasks with customer message context
    photo_analysis_task = Task(
        description=f"""Customer message: "{customer_message}"
        
        Analyze any business photos provided by the customer. 
        Look for:
        - Business location verification
        - Visual evidence of business operations
        - Potential risk factors
        - Quality and professionalism indicators
        
        Provide a detailed analysis with risk assessment.""",
        agent=photo_verifier,
        expected_output="Detailed photo analysis with risk assessment and business verification findings"
    )
    
    business_coaching_task = Task(
        description=f"""Customer message: "{customer_message}"
        
        Help the customer clarify their business goals and loan purpose.
        Ask probing questions about:
        - Specific business needs
        - How the loan will be used
        - Expected business outcomes
        - Timeline for implementation
        
        Help them set SMART goals and ensure loan purpose aligns with business strategy.""",
        agent=business_coach,
        expected_output="Clear business goals, loan purpose, and implementation plan"
    )
    
    underwriting_task = Task(
        description=f"""Customer message: "{customer_message}"
        
        Based on all available information (customer details, photo analysis, business goals), 
        assess the loan application and generate an appropriate loan offer.
        Consider:
        - Risk factors from photo analysis
        - Business viability and goals
        - Appropriate loan amount and terms
        - Risk mitigation strategies
        
        Provide a comprehensive loan offer with reasoning.""",
        agent=underwriter,
        expected_output="Comprehensive loan offer with amount, terms, and risk assessment"
    )
    
    # Create the crew
    crew = Crew(
        agents=[photo_verifier, business_coach, underwriter],
        tasks=[photo_analysis_task, business_coaching_task, underwriting_task],
        process=Process.sequential,
        verbose=True,
        langfuse=langfuse
    )
    
    return crew 