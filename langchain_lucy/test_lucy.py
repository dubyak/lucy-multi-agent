#!/usr/bin/env python3
"""
Test script for Lucy LangChain implementation
Demonstrates seamless customer experience through the critical path: B1→B4→E4b→E6→L3→L5→OFFER
"""

import os
import sys
import json
from typing import Dict, Any

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lucy_ai import LucyAI, LucyState, LucyTask

def test_seamless_customer_flow():
    """Test the complete customer journey"""
    
    # Initialize Lucy (using demo mode if no API key)
    api_key = os.getenv("OPENAI_API_KEY", "demo-key")
    lucy = LucyAI(api_key)
    
    print("🚀 Testing Lucy LangChain Implementation")
    print("=" * 50)
    
    # Track the conversation state
    state = None
    
    # Simulate customer conversation
    test_conversation = [
        {
            "message": "Hi, I need a loan for my shop",
            "photos": None,
            "expected_task": "B1",
            "description": "Initial greeting"
        },
        {
            "message": "I have a small grocery shop in Kawangware Market, Lane 3. Here are my photos.",
            "photos": ["inside_shop.jpg", "outside_shop.jpg"],
            "expected_task": "E4A",
            "description": "B1: Photos and location provided"
        },
        {
            "message": "I run a small grocery kiosk selling household items and food",
            "photos": None,
            "expected_task": "E4B", 
            "description": "E4A: Business type provided"
        },
        {
            "message": "I love helping my community get fresh food at fair prices. It makes me happy to serve my neighbors.",
            "photos": None,
            "expected_task": "B4",
            "description": "E4B: What they love about business"
        },
        {
            "message": "I serve about 25 customers daily and make around 3000 KES per day",
            "photos": None,
            "expected_task": "E6",
            "description": "B4: Sales data provided"
        },
        {
            "message": "My biggest challenge is running out of popular items. Customers come but I don't have enough stock sometimes.",
            "photos": None,
            "expected_task": "L3",
            "description": "E6: Challenge identified"
        },
        {
            "message": "I want to use the loan to buy more stock and inventory for my shop",
            "photos": None,
            "expected_task": "L5",
            "description": "L3: Loan usage specified"
        },
        {
            "message": "Yes, I'm ready to see the offer!",
            "photos": None,
            "expected_task": "OFFER",
            "description": "L5: Ready for loan offer"
        }
    ]
    
    # Run through the conversation
    for i, turn in enumerate(test_conversation, 1):
        print(f"\n📱 **Step {i}: {turn['description']}**")
        print(f"Customer: {turn['message']}")
        if turn['photos']:
            print(f"Photos: {turn['photos']}")
        
        # Get Lucy's response
        try:
            response, state = lucy.chat(
                message=turn['message'],
                photos=turn['photos'],
                state=state
            )
            
            print(f"\n🤖 Lucy: {response}")
            print(f"\n📊 Current Task: {state.current_task.value}")
            print(f"📋 Completed Tasks: {[task.value for task in state.customer_data.completed_tasks]}")
            
            # Verify we're progressing correctly
            if state.current_task.value != turn['expected_task']:
                print(f"⚠️  Expected task {turn['expected_task']}, got {state.current_task.value}")
            else:
                print(f"✅ Task progression correct")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            
        print("-" * 50)
    
    # Final summary
    print(f"\n🎯 **Final Results:**")
    print(f"✅ Completed Tasks: {[task.value for task in state.customer_data.completed_tasks]}")
    print(f"📋 Customer Data Collected:")
    print(f"   - Business: {state.customer_data.business_type}")
    print(f"   - Location: {state.customer_data.location}")
    print(f"   - Daily Sales: {state.customer_data.daily_sales:,} KES")
    print(f"   - Daily Customers: {state.customer_data.daily_customers}")
    print(f"   - Challenge: {state.customer_data.challenge}")
    print(f"   - Loan Uses: {state.customer_data.loan_uses}")
    
    # Check if we reached the end
    if state.current_task == LucyTask.OFFER:
        print("\n🎉 SUCCESS: Complete customer journey achieved!")
        print("🔄 Seamless multi-agent experience - customer never knew about different agents")
    else:
        print(f"\n⚠️  Journey incomplete. Stopped at task: {state.current_task.value}")
    
    return state

def test_agent_specialization():
    """Test that agents are working behind the scenes"""
    
    print("\n🔍 **Testing Agent Specialization**")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY", "demo-key")
    lucy = LucyAI(api_key)
    
    # Test different scenarios
    test_cases = [
        {
            "message": "Here are my shop photos",
            "photos": ["test.jpg"],
            "expected_agent": "photo_verifier",
            "task": LucyTask.B1
        },
        {
            "message": "I love my business",
            "photos": None,
            "expected_agent": "business_coach", 
            "task": LucyTask.E4B
        },
        {
            "message": "I make 2000 KES daily",
            "photos": None,
            "expected_agent": "underwriter",
            "task": LucyTask.B4
        }
    ]
    
    for case in test_cases:
        print(f"\n🧪 Testing: {case['message']}")
        
        # Create state with specific task
        state = LucyState(current_task=case['task'])
        
        # Determine which agent would handle this
        agent = lucy._route_message(case['message'], case['task'])
        print(f"🤖 Agent Selected: {agent}")
        
        if agent == case['expected_agent']:
            print("✅ Correct agent selection")
        else:
            print(f"⚠️  Expected {case['expected_agent']}, got {agent}")

def display_architecture_overview():
    """Display the architecture overview"""
    
    print("\n🏗️  **LangChain Lucy Architecture**")
    print("=" * 50)
    print("""
🎯 **Seamless Customer Experience Design:**

1. **Single Lucy Interface** 
   - Customer always talks to "Lucy"
   - No awareness of multiple agents
   - Consistent personality and tone

2. **Hidden Agent Orchestration**
   - PhotoVerifier: Handles image analysis (B1)
   - BusinessCoach: Manages relationship building (E4a, E4b, E6)  
   - Underwriter: Processes financial data (B4, L3, L5, OFFER)

3. **Smart State Management**
   - Tracks customer data throughout journey
   - Automatic task progression: B1→E4A→E4B→B4→E6→L3→L5→OFFER
   - Context preservation across agent handoffs

4. **Intelligent Routing**
   - Message content analysis
   - Current task awareness
   - Seamless agent transitions

5. **Benefits vs Single Agent:**
   ✅ Specialized expertise per domain
   ✅ Consistent evaluation standards
   ✅ Parallel processing capabilities
   ✅ Easier testing and updates
   ✅ Better traceability and debugging
    """)

if __name__ == "__main__":
    print("🚀 Lucy LangChain Implementation Test Suite")
    print("=========================================")
    
    # Display architecture
    display_architecture_overview()
    
    # Test agent specialization
    test_agent_specialization() 
    
    # Test complete customer flow
    final_state = test_seamless_customer_flow()
    
    print(f"\n✨ **Test Complete!**")
    print("This demonstrates how LangChain enables seamless customer experience")
    print("while maintaining the benefits of specialized multi-agent architecture.")