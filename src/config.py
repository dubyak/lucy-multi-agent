"""
Configuration for Lucy Multi-Agent Crew
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Crew configuration
CREW_NAME = "lucy-multi-agent"
CREW_DESCRIPTION = "Lucy - AI Loan Officer & Business Partner with multi-agent workflow"

# Environment variables
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Agent configurations
AGENTS = {
    "photo_verifier": {
        "name": "PhotoVerifier",
        "role": "Photo Verification Specialist",
        "goal": "Verify shop photos meet authenticity and quality standards",
        "backstory": "You are an expert at analyzing business photos for loan applications. You check for authenticity, duplicates, and assess business capacity from visual evidence."
    },
    "business_coach": {
        "name": "BusinessCoach",
        "role": "Business Development Coach", 
        "goal": "Guide customers through goal-setting and business planning",
        "backstory": "You are Lucy's business coaching specialist. You help micro-business owners identify specific, measurable outcomes and create actionable plans."
    },
    "underwriter": {
        "name": "Underwriter",
        "role": "Loan Underwriting Specialist",
        "goal": "Assess risk and generate appropriate loan offers", 
        "backstory": "You are a conservative loan underwriter following Tala's policies. You analyze business photos, income estimates, and behavioral signals to determine loan amounts and terms."
    }
}

# Task configurations
TASKS = {
    "photo_verification": {
        "description": "Verify shop photos and location. Check for authenticity, non-duplicates, and business capacity assessment.",
        "expected_output": "Photo verification report with authenticity check and business capacity assessment"
    },
    "business_coaching": {
        "description": "Guide the customer through business goal setting using the outside-in approach. Help define specific goals and identify loan uses.",
        "expected_output": "Complete business profile with specific goal and loan use plan"
    },
    "loan_underwriting": {
        "description": "Generate loan offer based on underwriting analysis. Assess risk and create appropriate loan terms.",
        "expected_output": "Complete loan offer with all terms and amounts properly calculated"
    }
} 