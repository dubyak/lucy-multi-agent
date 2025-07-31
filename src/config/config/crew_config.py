"""
Crew configuration for Lucy Multi-Agent
"""

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_lucy_crew():
    """Create Lucy's multi-agent crew for CrewAI Cloud"""
    
    # Setup LLM based on environment
    llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    if llm_provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=api_key
        )
    elif llm_provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            temperature=0.7,
            api_key=api_key
        )
    elif llm_provider == "gemini":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,
            api_key=api_key
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {llm_provider}")
    
    # Create Lucy's agents
    photo_verifier = Agent(
        name="PhotoVerifier",
        role="Photo Verification Specialist",
        goal="Verify shop photos meet authenticity and quality standards",
        backstory="You are an expert at analyzing business photos for loan applications. You check for authenticity, duplicates, and assess business capacity from visual evidence.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    business_coach = Agent(
        name="BusinessCoach",
        role="Business Development Coach",
        goal="Guide customers through goal-setting and business planning",
        backstory="You are Lucy's business coaching specialist. You help micro-business owners identify specific, measurable outcomes and create actionable plans.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    underwriter = Agent(
        name="Underwriter",
        role="Loan Underwriting Specialist",
        goal="Assess risk and generate appropriate loan offers",
        backstory="You are a conservative loan underwriter following Tala's policies. You analyze business photos, income estimates, and behavioral signals to determine loan amounts and terms.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # Create tasks
    task1 = Task(
        description="Verify shop photos and location. Check for authenticity, non-duplicates, and business capacity assessment.",
        agent=photo_verifier,
        expected_output="Photo verification report with authenticity check and business capacity assessment"
    )

    task2 = Task(
        description="Guide the customer through business goal setting using the outside-in approach. Help define specific goals and identify loan uses.",
        agent=business_coach,
        expected_output="Complete business profile with specific goal and loan use plan"
    )

    task3 = Task(
        description="Generate loan offer based on underwriting analysis. Assess risk and create appropriate loan terms.",
        agent=underwriter,
        expected_output="Complete loan offer with all terms and amounts properly calculated"
    )

    # Create the crew
    lucy_crew = Crew(
        agents=[photo_verifier, business_coach, underwriter],
        tasks=[task1, task2, task3],
        verbose=True
    )
    
    return lucy_crew 