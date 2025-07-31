#!/usr/bin/env python3
"""
Lucy Multi-Agent for CrewAI Cloud Deployment
Adapted for CrewAI Cloud with proper agent and task structure
"""

import os
from dotenv import load_dotenv
from langfuse import Langfuse

# Load environment variables
load_dotenv()

# Initialize Langfuse for observability
langfuse = Langfuse(
    secret_key="sk-lf-c61c7ea7-0d24-485b-b55b-5aadde7a3b9c",
    public_key="pk-lf-5f4408d4-e2de-4359-b27e-941e12bd687e",
    host="https://us.cloud.langfuse.com"
)

# Import CrewAI components
try:
    from crewai import Agent, Task, Crew
    from langchain_openai import ChatOpenAI
    from langchain_anthropic import ChatAnthropic
    from langchain_google_genai import ChatGoogleGenerativeAI
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    print("CrewAI not available, using simplified version")

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
    
    if not CREWAI_AVAILABLE:
        print("CrewAI not available, cannot create crew")
        return None
    
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
        backstory="""You are an expert at analyzing business photos for loan applications. 
        You check for authenticity, duplicates, and assess business capacity from visual evidence.
        You follow strict protocols to ensure only genuine business photos are accepted.
        
        For each photo, check:
        - Authenticity (no watermarks, stock-image feel, screenshots)
        - Duplicates (exact same image re-sent)
        - Business capacity (stock density, floor area, product mix)
        
        If issues found, request fresh photos. Only proceed with authentic, unique photos.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    business_coach = Agent(
        name="BusinessCoach", 
        role="Business Development Coach",
        goal="Guide customers through goal-setting and business planning",
        backstory="""You are Lucy's business coaching specialist. You help micro-business owners 
        identify specific, measurable outcomes and create actionable plans. You use warmth-first 
        approach, building trust before diving into numbers. You create tangible assets like 
        promo copy, templates, and quick calculations to demonstrate immediate value.
        
        Follow the outside-in approach:
        1. Trust/Identity: Ask about business type, what they love, how long they've been doing it
        2. Ambition: Ask about 1-year vision and 6-month dreams  
        3. Structure: Help define a specific 1-3 month goal
        4. Triangulate: Capture yesterday's sales and customer count
        5. Challenge Sprint: Identify biggest blocker, run collaborative sprint
        6. Loan Uses: Identify top 1-3 loan uses and confirm readiness
        
        Always deliver value before asking for information.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    underwriter = Agent(
        name="Underwriter",
        role="Loan Underwriting Specialist", 
        goal="Assess risk and generate appropriate loan offers",
        backstory="""You are a conservative loan underwriter following Tala's policies. 
        You analyze business photos, income estimates, and behavioral signals to determine 
        loan amounts and terms. You ensure all critical tasks are complete before offering loans.
        You follow strict tenure and amount gates based on loan history.
        
        Underwriting process:
        1. Photo Income Note: Assess stock density, floor area, turnover tier
        2. Behavioral Score: Evaluate willingness, capability, follow-through, integrity
        3. Loan Amount: Calculate based on net monthly income with appropriate caps
        4. Product Selection: Choose tenure based on loan history (15-60 days first loans, 61-180 repeat)
        5. Generate formal offer with all required fields populated
        
        Critical path: B1 → B4 → E4b → E6 → L3 → L5 must be complete before offering.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # Create tasks
    task1 = Task(
        description="""Verify shop photos and location. Check for:
        1. At least 2 authentic, non-duplicate photos
        2. Specific location (market/area or area + street)
        3. Business authenticity from visual evidence
        4. Stock density and floor area assessment
        
        If photos are insufficient, request additional ones.
        Only proceed when both photos and specific location are provided.
        
        Output: Photo verification report with authenticity check, business capacity assessment, and location validation""",
        agent=photo_verifier,
        expected_output="Photo verification report with authenticity check, business capacity assessment, and location validation"
    )

    task2 = Task(
        description="""Guide the customer through business goal setting using the outside-in approach:
        
        Phase 1 - Trust/Identity: Ask about business type, what they love, how long they've been doing it
        Phase 2 - Ambition: Ask about 1-year vision and 6-month dreams  
        Phase 3 - Structure: Help define a specific 1-3 month goal
        Phase 4 - Triangulate: Capture yesterday's sales and customer count
        Phase 5 - Challenge Sprint: Identify biggest blocker, run 5-10 turn collaborative sprint with:
            - 2+ clarifiers
            - 1+ insight/quick calc  
            - 1+ created asset (promo copy, template, etc.)
            - Micro-test commitment
        Phase 6 - Loan Uses: Identify top 1-3 loan uses and confirm readiness
        
        Deliver tangible value before asking for information. Create assets in chat.
        
        Output: Complete business profile with specific goal, challenge analysis, and loan use plan""",
        agent=business_coach,
        expected_output="Complete business profile with specific goal, challenge analysis, and loan use plan"
    )

    task3 = Task(
        description="""Generate loan offer based on underwriting analysis:
        
        1. Photo Income Note: Assess stock density, floor area, turnover tier, and derive conservative net income estimate
        2. Behavioral Score: Evaluate willingness, capability, follow-through, and integrity
        3. Loan Amount: Calculate based on net monthly income with appropriate caps (10k-50k first loans, 10k-150k repeat)
        4. Product Selection: Choose tenure based on loan history and customer needs
        5. Generate formal offer with all required fields populated
        
        Follow all flow guards and ensure critical path completion before offering.
        
        Output: Complete loan offer with all terms, amounts, and due dates properly calculated""",
        agent=underwriter,
        expected_output="Complete loan offer with all terms, amounts, and due dates properly calculated"
    )

    # Create the crew
    lucy_crew = Crew(
        agents=[photo_verifier, business_coach, underwriter],
        tasks=[task1, task2, task3],
        verbose=True,
        memory=True
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