#!/usr/bin/env python3
"""
FastAPI backend for Lucy LangChain implementation
Provides REST API for seamless customer-facing chat experience
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import json
import uuid
from datetime import datetime

from lucy_ai import LucyAI, LucyState, LucyTask

# Initialize FastAPI app
app = FastAPI(
    title="Lucy AI - Loan Officer & Business Partner",
    description="Seamless customer experience with multi-agent backend",
    version="2.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Lucy AI system
lucy_ai = None
try:
    api_key = os.getenv("OPENAI_API_KEY", "demo-key")
    print(f"Initializing Lucy AI with API key: {'***' + api_key[-4:] if len(api_key) > 4 else 'demo-key'}")
    lucy_ai = LucyAI(api_key)
    print("Lucy AI initialized successfully")
except Exception as e:
    print(f"Warning: Lucy AI initialization failed: {e}")
    # Initialize anyway for demo mode
    lucy_ai = LucyAI("demo-key")

# In-memory session storage (use Redis in production)
sessions: Dict[str, LucyState] = {}

# Pydantic models for API
class ChatMessage(BaseModel):
    message: str
    photos: Optional[List[str]] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    current_task: str
    completed_tasks: List[str]
    customer_data: Dict[str, Any]
    agent_used: Optional[str] = None

class SessionInfo(BaseModel):
    session_id: str
    current_task: str
    completed_tasks: List[str]
    created_at: str
    customer_data: Dict[str, Any]

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Lucy AI - LangChain Implementation",
        "version": "2.0.0",
        "status": "operational",
        "features": [
            "Seamless customer experience",
            "Multi-agent backend",
            "Critical path: B1→B4→E4b→E6→L3→L5→OFFER",
            "Specialized agents: PhotoVerifier, BusinessCoach, Underwriter"
        ],
        "endpoints": {
            "chat": "/chat",
            "demo": "/demo (POST)",
            "frontend": "/app",
            "docs": "/docs"
        }
    }

@app.get("/app")
async def get_frontend():
    """Serve the frontend application"""
    return FileResponse("index.html", media_type="text/html")

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Main chat endpoint - customer sends message, gets Lucy's response"""
    
    print(f"Received chat message: {message.message[:50]}...")
    
    if not lucy_ai:
        print("Lucy AI system not available")
        raise HTTPException(status_code=503, detail="Lucy AI system not available")
    
    try:
        # Get or create session
        session_id = message.session_id or str(uuid.uuid4())
        state = sessions.get(session_id)
        
        print(f"Session ID: {session_id}, Existing state: {state is not None}")
        
        # Chat with Lucy
        response, updated_state = lucy_ai.chat(
            message=message.message,
            photos=message.photos,
            state=state
        )
        
        print(f"Lucy response: {response[:100]}...")
        print(f"Current task: {updated_state.current_task.value}")
        
        # Save updated state
        sessions[session_id] = updated_state
        
        # Determine which agent was used (for analytics)
        agent_used = lucy_ai._route_message(message.message, updated_state.current_task)
        
        return ChatResponse(
            response=response,
            session_id=session_id,
            current_task=updated_state.current_task.value,
            completed_tasks=[task.value for task in updated_state.customer_data.completed_tasks],
            customer_data={
                "business_type": updated_state.customer_data.business_type,
                "location": updated_state.customer_data.location,
                "what_they_love": updated_state.customer_data.what_they_love,
                "daily_customers": updated_state.customer_data.daily_customers,
                "daily_sales": updated_state.customer_data.daily_sales,
                "challenge": updated_state.customer_data.challenge,
                "loan_uses": updated_state.customer_data.loan_uses,
                "photos_count": len(updated_state.customer_data.photos)
            },
            agent_used=agent_used
        )
        
    except Exception as e:
        print(f"Chat error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Chat processing error: {str(e)}")

@app.get("/session/{session_id}", response_model=SessionInfo)
async def get_session(session_id: str):
    """Get session information"""
    
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    state = sessions[session_id]
    
    return SessionInfo(
        session_id=session_id,
        current_task=state.current_task.value,
        completed_tasks=[task.value for task in state.customer_data.completed_tasks],
        created_at=datetime.now().isoformat(),  # In production, store actual creation time
        customer_data={
            "business_type": state.customer_data.business_type,
            "location": state.customer_data.location,
            "what_they_love": state.customer_data.what_they_love,
            "daily_customers": state.customer_data.daily_customers,
            "daily_sales": state.customer_data.daily_sales,
            "challenge": state.customer_data.challenge,
            "loan_uses": state.customer_data.loan_uses,
            "photos_count": len(state.customer_data.photos)
        }
    )

@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    del sessions[session_id]
    
    return {"message": f"Session {session_id} deleted successfully"}

@app.get("/sessions")
async def list_sessions():
    """List all active sessions"""
    
    session_list = []
    for session_id, state in sessions.items():
        session_list.append({
            "session_id": session_id,
            "current_task": state.current_task.value,
            "completed_tasks": len(state.customer_data.completed_tasks),
            "business_type": state.customer_data.business_type or "Not specified"
        })
    
    return {"sessions": session_list, "total": len(session_list)}

@app.get("/analytics")
async def get_analytics():
    """Get system analytics"""
    
    if not sessions:
        return {"message": "No sessions yet"}
    
    # Basic analytics
    task_distribution = {}
    agent_usage = {"photo_verifier": 0, "business_coach": 0, "underwriter": 0}
    
    for state in sessions.values():
        task = state.current_task.value
        task_distribution[task] = task_distribution.get(task, 0) + 1
        
        # Estimate agent usage based on task
        if state.current_task in [LucyTask.B1]:
            agent_usage["photo_verifier"] += 1
        elif state.current_task in [LucyTask.E4A, LucyTask.E4B, LucyTask.E6]:
            agent_usage["business_coach"] += 1
        elif state.current_task in [LucyTask.B4, LucyTask.L3, LucyTask.L5, LucyTask.OFFER]:
            agent_usage["underwriter"] += 1
    
    return {
        "total_sessions": len(sessions),
        "task_distribution": task_distribution,
        "agent_usage": agent_usage,
        "completion_stats": {
            "reached_offer": sum(1 for s in sessions.values() if s.current_task == LucyTask.OFFER),
            "avg_completed_tasks": sum(len(s.customer_data.completed_tasks) for s in sessions.values()) / len(sessions)
        }
    }

@app.post("/demo")
async def run_demo():
    """Run a demonstration of the complete customer journey"""
    
    if not lucy_ai:
        raise HTTPException(status_code=503, detail="Lucy AI system not available")
    
    # Simulate a complete customer conversation
    demo_conversation = [
        {"message": "Hi, I need a loan for my shop", "photos": None},
        {"message": "I have a grocery shop in Kawangware Market, Lane 3", "photos": ["demo1.jpg", "demo2.jpg"]},
        {"message": "I run a small grocery selling household items", "photos": None},
        {"message": "I love helping my community with fresh food at fair prices", "photos": None},
        {"message": "I serve 25 customers daily and make 3000 KES per day", "photos": None},
        {"message": "My challenge is running out of popular items", "photos": None},
        {"message": "I want to use the loan for more stock and inventory", "photos": None},
        {"message": "Yes, I'm ready for the offer!", "photos": None}
    ]
    
    demo_session_id = f"demo_{uuid.uuid4()}"
    state = None
    conversation_log = []
    
    try:
        for i, turn in enumerate(demo_conversation):
            response, state = lucy_ai.chat(
                message=turn["message"],
                photos=turn["photos"],
                state=state
            )
            
            conversation_log.append({
                "step": i + 1,
                "customer": turn["message"],
                "lucy": response,
                "current_task": state.current_task.value,
                "completed_tasks": [task.value for task in state.customer_data.completed_tasks]
            })
        
        # Store demo session
        sessions[demo_session_id] = state
        
        return {
            "demo_session_id": demo_session_id,
            "conversation": conversation_log,
            "final_state": {
                "current_task": state.current_task.value,
                "completed_tasks": [task.value for task in state.customer_data.completed_tasks],
                "customer_data": {
                    "business_type": state.customer_data.business_type,
                    "location": state.customer_data.location,
                    "daily_sales": state.customer_data.daily_sales,
                    "loan_uses": state.customer_data.loan_uses
                }
            },
            "success": state.current_task == LucyTask.OFFER
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    # Railway provides PORT environment variable
    port = int(os.getenv("PORT", 8000))
    host = "0.0.0.0"  # Must bind to 0.0.0.0 for Railway
    
    print(f"🚀 Starting Lucy AI LangChain Backend on {host}:{port}")
    print("📋 Available endpoints:")
    print("  POST /chat - Main chat interface")
    print("  GET /session/{id} - Session info")
    print("  GET /sessions - List sessions")
    print("  GET /analytics - System analytics")
    print("  POST /demo - Run complete demo")
    
    uvicorn.run(app, host=host, port=port, log_level="info")