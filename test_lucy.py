#!/usr/bin/env python3
"""
Test script for Lucy's multi-agent setup
Tests different LLM providers and basic functionality
"""

import os
import sys
from crew import run_lucy, LLMConfig

def test_llm_providers():
    """Test different LLM providers"""
    providers = ["openai", "anthropic", "gemini"]
    
    for provider in providers:
        print(f"\n{'='*50}")
        print(f"Testing {provider.upper()} provider")
        print(f"{'='*50}")
        
        # Set environment variables
        os.environ["LLM_PROVIDER"] = provider
        
        if provider == "openai":
            os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
        elif provider == "anthropic":
            os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY", "")
        elif provider == "gemini":
            os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")
        
        try:
            # Test LLM configuration
            llm_config = LLMConfig()
            llm = llm_config.setup_llm()
            print(f"✅ {provider} LLM configured successfully")
            
            # Test basic Lucy functionality
            test_input = "Hi, I need a loan for my small shop in Nairobi"
            print(f"Testing with input: {test_input}")
            
            result = run_lucy(test_input)
            print(f"✅ {provider} test completed")
            print(f"Response length: {len(str(result))} characters")
            
        except Exception as e:
            print(f"❌ {provider} test failed: {str(e)}")

def test_specific_provider(provider="openai"):
    """Test a specific provider with a more detailed conversation"""
    print(f"\n{'='*50}")
    print(f"Detailed test with {provider.upper()}")
    print(f"{'='*50}")
    
    # Set environment variables
    os.environ["LLM_PROVIDER"] = provider
    
    if provider == "openai":
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
    elif provider == "anthropic":
        os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY", "")
    elif provider == "gemini":
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")
    
    try:
        # Test with a more realistic conversation
        conversation_steps = [
            "Hi, I need a loan for my small shop in Nairobi",
            "I run a small grocery store in Gikomba market",
            "I've been running it for 2 years now",
            "I want to expand and add a fridge to sell cold drinks",
            "Yesterday I had about 50 customers and made 15,000 KES",
            "My biggest challenge is running out of stock too quickly",
            "I would use the loan to buy more inventory and add the fridge"
        ]
        
        for i, step in enumerate(conversation_steps, 1):
            print(f"\nStep {i}: {step}")
            result = run_lucy(step)
            print(f"Response: {result[:200]}...")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    print("🧪 Testing Lucy's Multi-Agent Setup")
    print("=" * 50)
    
    # Test all providers
    test_llm_providers()
    
    # Test specific provider in detail
    test_specific_provider("openai")
    
    print("\n✅ Testing completed!")
