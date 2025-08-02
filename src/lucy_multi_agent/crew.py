"""
Lucy 2.0 Multi-Agent Crew - Demonstrating Specialized Agent Benefits
"""

import os
from typing import Dict, Any, Optional

def create_lucy_crew(customer_message: str = "", customer_photos: list = None, location: str = "") -> str:
    """
    Lucy 2.0 Multi-Agent Workflow - CrewAI Cloud Compatible
    """
    
    # Try to use actual CrewAI first, fallback to demonstration
    try:
        # Check if we can import CrewAI properly
        from crewai import Crew
        import os
        
        # Check for required environment variables
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found")
        
        # Try to create actual CrewAI crew
        crew = Crew(
            agents_config='config/agents.yaml',
            tasks_config='config/tasks.yaml',
            verbose=True
        )
        
        # Run the crew with inputs
        inputs = {
            'customer_message': customer_message,
            'customer_photos': customer_photos or [],
            'location': location
        }
        
        result = crew.kickoff(inputs=inputs)
        return f"🤖 **CrewAI Multi-Agent Result:**\n\n{str(result)}"
        
    except Exception as e:
        # Fallback to demonstration mode
        return simulate_multi_agent_workflow(
            customer_message=customer_message,
            customer_photos=customer_photos or [],
            location=location,
            error_info=str(e)
        )

def simulate_multi_agent_workflow(customer_message: str, customer_photos: list, location: str, error_info: str = "") -> str:
    """Simulate the multi-agent workflow benefits"""
    
    # Simulate agent specialization
    photo_analysis = simulate_photo_verifier(customer_photos)
    coaching_insights = simulate_business_coach(customer_message) 
    underwriting_assessment = simulate_underwriter(customer_message)
    
    return f"""🤖 **Lucy 2.0 Multi-Agent System Demo**

📧 **Customer Message:** "{customer_message}"

---

## 🔍 **Agent Specialization in Action**

### 📸 **PhotoVerifier Agent** - Task B1 Analysis
{photo_analysis}

### 💡 **BusinessCoach Agent** - Tasks E4a/E4b/E6  
{coaching_insights}

### 📊 **Underwriter Agent** - Tasks B4/L3/L5
{underwriting_assessment}

---

## 🌟 **Multi-Agent Benefits Demonstrated:**

✅ **Specialized Context**: Each agent maintains domain-specific expertise
✅ **Parallel Processing**: Photo analysis concurrent with interview questions
✅ **Quality Consistency**: Dedicated agents ensure uniform evaluation standards  
✅ **Modular Architecture**: Easy to update individual agent capabilities
✅ **Traceability**: Clear attribution of decisions to specific agents

**Next Steps**: Configure API keys to activate full CrewAI functionality with Langfuse tracing.

{f"**Debug Info**: {error_info}" if error_info else ""}

---
*Lucy 2.0 Multi-Agent System - Powered by CrewAI*
"""

def simulate_photo_verifier(photos: list) -> str:
    """Simulate PhotoVerifier agent capabilities"""
    
    if not photos:
        return """
**Status**: Waiting for photos
**Task B1 Requirements**: 
- ≥2 authentic business photos (inside + outside view)
- Specific location (market/area/street)
**Specialization**: Authenticity detection, stock density assessment, Photo Income Note generation
**Benefits**: Consistent visual evaluation standards, automated duplicate detection
        """
    
    return """
**Photo Analysis Complete** ✅
- **Authenticity**: Photos verified as genuine business images
- **Stock Density**: Medium (moderate shelf fullness, visible back-stock)
- **Floor Area**: Small (<8m²) typical Kenyan micro-business setup
- **Turnover Assessment**: Medium based on product variety and arrangement
- **Photo Income Note**: Conservative estimate 15,000-25,000 KES monthly gross
**Agent Benefits**: Specialized computer vision expertise, consistent evaluation criteria
    """

def simulate_business_coach(message: str) -> str:
    """Simulate BusinessCoach agent approach"""
    
    return f"""
**Outside-In Coaching Approach** 🎯
- **Identity First**: "What do you love about your business?"
- **Vision Setting**: Long-term aspirations before financial details  
- **Asset Creation**: Ready to generate WhatsApp promos, expense trackers, layout sketches
- **Micro-Tests**: Design 1-3 day experiments for immediate action
**Agent Benefits**: Pure coaching focus, behavioral psychology expertise, consistent relationship-building
**Current Focus**: Establishing trust and understanding motivations before discussing money
    """

def simulate_underwriter(message: str) -> str:
    """Simulate Underwriter agent analysis"""
    
    return f"""
**Risk Assessment Framework** 📋
- **Critical Path**: B1→B4→E4b→E6→L3→L5 completion required
- **Behavioral Scoring**: Willingness, Capability, Follow-through, Integrity pillars
- **Loan Structuring**: 0.6% daily (≤60 days) or 0.2% daily (61-180 days repeat)
- **Photo Income Note Integration**: Anchoring decisions to visual business assessment
**Agent Benefits**: Financial expertise focus, consistent underwriting standards, risk modeling specialization
**Status**: Awaiting completion of coaching tasks before loan structuring
    """

def generate_fallback_response(customer_message: str, error_info: str) -> str:
    """Fallback response for deployment stability"""
    
    return f"""Lucy AI Loan Officer Response:

Hello! I'm Lucy, your AI loan officer and business partner. I received your message: "{customer_message}"

I'm currently running my multi-agent demonstration system with three specialized agents:

1. **PhotoVerifier** - Analyzes business photos for Task B1 (authenticity, Photo Income Notes)
2. **BusinessCoach** - Handles relationship building and goal setting (Tasks E4a, E4b, E6)  
3. **Underwriter** - Manages risk assessment and loan structuring (Tasks B4, L3, L5)

🔧 **Status**: System ready for full activation with API keys configured.

To begin the Lucy 2.0 workflow:
- Share 2 business photos (inside and outside views)
- Provide your specific business location
- Tell me what you love about your business

I'm here to demonstrate how multi-agent specialization improves loan processing! 🚀

*Debug info: {error_info}*
"""
