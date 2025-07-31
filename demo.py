#!/usr/bin/env python3
"""
Lucy Multi-Agent Demo
Showcases the complete workflow with realistic conversation
"""

import os
from dotenv import load_dotenv
from simple_lucy import LucyAgent

# Load environment variables
load_dotenv()

def run_demo_conversation():
    """Run a realistic conversation demo with Lucy"""
    
    print("🎭 Lucy Multi-Agent Demo")
    print("=" * 60)
    print("This demo shows Lucy's three specialized agents working together")
    print("to guide a customer through the loan application process.")
    print("=" * 60)
    
    # Initialize Lucy with OpenAI (you can change to "anthropic" or "gemini")
    lucy = LucyAgent("openai")
    
    # Simulate a realistic conversation
    conversation = [
        "Hi, I need a loan for my small shop in Nairobi",
        "I run a grocery store in Gikomba market, been doing it for 2 years",
        "I want to add a fridge to sell cold drinks and expand my inventory",
        "Yesterday I had about 50 customers and made 15,000 KES",
        "My biggest challenge is running out of stock too quickly",
        "I would use the loan to buy more inventory and add the fridge"
    ]
    
    print(f"\n🤖 Using {lucy.llm_config.provider.upper()} as the LLM provider")
    print("\n📝 Conversation Flow:")
    print("-" * 40)
    
    for i, message in enumerate(conversation, 1):
        print(f"\n💬 Customer (Step {i}): {message}")
        print("-" * 40)
        
        # Run the complete Lucy workflow
        result = lucy.run_lucy_workflow(message)
        
        print(f"\n✅ Step {i} completed with all three agents")
        print("=" * 60)

def compare_providers():
    """Compare responses from different LLM providers"""
    
    print("\n🔍 Provider Comparison Demo")
    print("=" * 60)
    
    test_input = "Hi, I need a loan for my small shop in Nairobi"
    providers = ["openai", "anthropic", "gemini"]
    
    for provider in providers:
        print(f"\n📊 {provider.upper()} Response:")
        print("-" * 40)
        
        lucy = LucyAgent(provider)
        result = lucy.run_lucy_workflow(test_input)
        
        print(f"\n✅ {provider.upper()} completed successfully")

if __name__ == "__main__":
    print("🚀 Starting Lucy Multi-Agent Demo")
    print("=" * 60)
    
    # Run the main demo
    run_demo_conversation()
    
    # Optional: Compare providers
    # compare_providers()
    
    print("\n🎉 Demo completed!")
    print("\n📊 Check your Langfuse dashboard for observability data:")
    print("   https://us.cloud.langfuse.com")
    print("\n🔧 To try different providers, edit the provider in demo.py")
    print("   Available: openai, anthropic, gemini") 