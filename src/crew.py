#!/usr/bin/env python3
"""
Lucy Multi-Agent Crew for CrewAI Cloud
Main entry point for CrewAI Cloud deployment
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import CrewAI components
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

class LLMConfig:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.llm = None
        
    def setup_llm(self):
        """Setup LLM based on environment configuration"""
        try:
            if self.provider == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY environment variable is required")
                self.llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0.7,
                    api_key=api_key
                )
                
            elif self.provider == "anthropic":
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key:
                    raise ValueError("ANTHROPIC_API_KEY environment variable is required")
                self.llm = ChatAnthropic(
                    model="claude-3-5-sonnet-20241022",
                    temperature=0.7,
                    api_key=api_key
                )
                
            elif self.provider == "gemini":
                api_key = os.getenv("GOOGLE_API_KEY")
                if not api_key:
                    raise ValueError("GOOGLE_API_KEY environment variable is required")
                self.llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    temperature=0.7,
                    api_key=api_key
                )
                
            else:
                raise ValueError(f"Unsupported LLM provider: {self.provider}")
            
            return self.llm
            
        except Exception as e:
            print(f"Error setting up LLM: {str(e)}")
            return None

def create_lucy_crew():
    """Create Lucy's multi-agent crew for CrewAI Cloud"""
    
    # Setup LLM
    llm_config = LLMConfig()
    llm = llm_config.setup_llm()
    
    if llm is None:
        print("Failed to setup LLM")
        return None
    
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

def run_lucy_crew(user_input):
    """Run Lucy's crew with the given input"""
    crew = create_lucy_crew()
    if crew is None:
        return "Error: Could not create Lucy crew"
    
    try:
        result = crew.kickoff(inputs={"customer_message": user_input})
        return result
    except Exception as e:
        return f"Error running Lucy crew: {str(e)}"

if __name__ == "__main__":
    # Test the crew
    test_input = "Hi, I need a loan for my small shop in Nairobi"
    result = run_lucy_crew(test_input)
    print("Lucy's Response:")
    print(result) 