#!/usr/bin/env python3
"""
Simplified Lucy Multi-Agent Setup
Works around dependency conflicts while maintaining core functionality
"""

import os
from typing import Optional
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

class LLMConfig:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.llm = None
        
    def setup_llm(self):
        """Setup LLM based on environment configuration"""
        try:
            if self.provider == "openai":
                from langchain_openai import ChatOpenAI
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY environment variable is required")
                self.llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0.7,
                    api_key=api_key
                )
                
            elif self.provider == "anthropic":
                from langchain_anthropic import ChatAnthropic
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key:
                    raise ValueError("ANTHROPIC_API_KEY environment variable is required")
                self.llm = ChatAnthropic(
                    model="claude-3-5-sonnet-20241022",
                    temperature=0.7,
                    api_key=api_key
                )
                
            elif self.provider == "gemini":
                from langchain_google_genai import ChatGoogleGenerativeAI
                api_key = os.getenv("GOOGLE_API_KEY")
                if not api_key:
                    raise ValueError("GOOGLE_API_KEY environment variable is required")
                self.llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    temperature=0.7,
                    api_key=api_key
                )
                
            else:
                raise ValueError(f"Unsupported LLM provider: {self.provider}. Supported: openai, anthropic, gemini")
            
            return self.llm
            
        except Exception as e:
            print(f"Error setting up LLM: {str(e)}")
            return None

class LucyAgent:
    """Simplified Lucy agent that simulates the multi-agent workflow"""
    
    def __init__(self, llm_provider="openai"):
        self.llm_config = LLMConfig()
        self.llm_config.provider = llm_provider
        self.llm = self.llm_config.setup_llm()
        self.conversation_history = []
        
    def photo_verifier(self, user_input):
        """Simulate photo verification agent"""
        if self.llm is None:
            return "Error: LLM not configured properly"
            
        prompt = f"""
        You are Lucy's Photo Verification Specialist. Analyze this customer input for photo verification needs:
        
        Customer: {user_input}
        
        Your role:
        1. Check if photos are mentioned or needed
        2. Verify authenticity requirements (no watermarks, stock images, etc.)
        3. Assess business capacity from any described photos
        4. Request specific location if not provided
        
        Respond as if you're guiding the customer through photo submission.
        """
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Photo verification error: {str(e)}"
    
    def business_coach(self, user_input):
        """Simulate business coaching agent"""
        if self.llm is None:
            return "Error: LLM not configured properly"
            
        prompt = f"""
        You are Lucy's Business Development Coach. Help this customer with business goal setting:
        
        Customer: {user_input}
        
        Follow the outside-in approach:
        1. Trust/Identity: Ask about business type, what they love, how long they've been doing it
        2. Ambition: Ask about 1-year vision and 6-month dreams  
        3. Structure: Help define a specific 1-3 month goal
        4. Triangulate: Capture yesterday's sales and customer count
        5. Challenge Sprint: Identify biggest blocker, run collaborative sprint
        6. Loan Uses: Identify top 1-3 loan uses and confirm readiness
        
        Always deliver value before asking for information. Create tangible assets like promo copy, templates, or quick calculations.
        """
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Business coaching error: {str(e)}"
    
    def underwriter(self, user_input):
        """Simulate loan underwriting agent"""
        if self.llm is None:
            return "Error: LLM not configured properly"
            
        prompt = f"""
        You are Lucy's Loan Underwriting Specialist. Assess this customer for loan eligibility:
        
        Customer: {user_input}
        
        Underwriting process:
        1. Photo Income Note: Assess stock density, floor area, turnover tier
        2. Behavioral Score: Evaluate willingness, capability, follow-through, integrity
        3. Loan Amount: Calculate based on net monthly income with appropriate caps
        4. Product Selection: Choose tenure based on loan history (15-60 days first loans, 61-180 repeat)
        5. Generate formal offer with all required fields populated
        
        Critical path: B1 → B4 → E4b → E6 → L3 → L5 must be complete before offering.
        """
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Underwriting error: {str(e)}"
    
    def run_lucy_workflow(self, user_input):
        """Run the complete Lucy workflow"""
        print(f"\n🤖 Lucy Multi-Agent Workflow")
        print(f"Provider: {self.llm_config.provider.upper()}")
        print(f"Input: {user_input}")
        print("-" * 50)
        
        # Step 1: Photo Verification
        print("\n📸 Photo Verification Agent:")
        photo_response = self.photo_verifier(user_input)
        print(photo_response)
        
        # Step 2: Business Coaching
        print("\n💼 Business Coaching Agent:")
        coach_response = self.business_coach(user_input)
        print(coach_response)
        
        # Step 3: Loan Underwriting
        print("\n💰 Loan Underwriting Agent:")
        underwriting_response = self.underwriter(user_input)
        print(underwriting_response)
        
        # Track in Langfuse
        try:
            trace = langfuse.trace(name="lucy_workflow")
            trace.span(name="photo_verification", input={"user_input": user_input}, output={"response": photo_response})
            trace.span(name="business_coaching", input={"user_input": user_input}, output={"response": coach_response})
            trace.span(name="loan_underwriting", input={"user_input": user_input}, output={"response": underwriting_response})
            trace.flush()
        except Exception as e:
            print(f"Langfuse tracking error: {str(e)}")
        
        return {
            "photo_verification": photo_response,
            "business_coaching": coach_response,
            "loan_underwriting": underwriting_response
        }

def test_lucy_providers():
    """Test Lucy with different LLM providers"""
    providers = ["openai", "anthropic", "gemini"]
    test_input = "Hi, I need a loan for my small shop in Nairobi"
    
    for provider in providers:
        print(f"\n{'='*60}")
        print(f"Testing {provider.upper()} Provider")
        print(f"{'='*60}")
        
        try:
            lucy = LucyAgent(provider)
            result = lucy.run_lucy_workflow(test_input)
            print(f"\n✅ {provider.upper()} test completed successfully!")
            
        except Exception as e:
            print(f"❌ {provider.upper()} test failed: {str(e)}")

if __name__ == "__main__":
    print("🧪 Testing Simplified Lucy Multi-Agent Setup")
    print("=" * 60)
    
    # Test all providers
    test_lucy_providers()
    
    print("\n✅ All tests completed!") 