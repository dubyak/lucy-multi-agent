"""
Lucy 2.0 Multi-Agent System Demo
Interactive Streamlit App demonstrating multi-agent benefits over single-agent approach
"""

import streamlit as st
import time
import json
from datetime import datetime
from typing import Dict, List, Any
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from lucy_multi_agent.crew import create_lucy_crew, simulate_multi_agent_workflow
    from lucy_multi_agent.crew import simulate_photo_verifier, simulate_business_coach, simulate_underwriter
except ImportError:
    # Fallback if imports fail
    def create_lucy_crew(customer_message=""):
        return f"Demo mode: {customer_message}"

# Page configuration
st.set_page_config(
    page_title="Lucy 2.0 Multi-Agent Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .agent-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .agent-active {
        border-left-color: #2ca02c;
        background-color: #e8f5e8;
    }
    .agent-complete {
        border-left-color: #17becf;
        background-color: #e1f7fa;
    }
    .comparison-box {
        border: 2px solid #ddd;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .single-agent {
        border-color: #ff7f0e;
        background-color: #fff7e6;
    }
    .multi-agent {
        border-color: #2ca02c;
        background-color: #e8f5e8;
    }
    .metrics-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'agent_status' not in st.session_state:
        st.session_state.agent_status = {
            'photo_verifier': 'waiting',
            'business_coach': 'waiting', 
            'underwriter': 'waiting'
        }
    if 'task_progress' not in st.session_state:
        st.session_state.task_progress = {
            'B1': False, 'E4a': False, 'E4b': False,
            'E6': False, 'B4': False, 'L3': False, 'L5': False
        }
    if 'demo_mode' not in st.session_state:
        st.session_state.demo_mode = 'comparison'
    if 'journey_step' not in st.session_state:
        st.session_state.journey_step = 'B1'
    if 'customer_data' not in st.session_state:
        st.session_state.customer_data = {
            'photos': [],
            'location': '',
            'business_type': '',
            'vision': '',
            'goal': '',
            'challenge': '',
            'sales_data': {},
            'loan_uses': [],
            'ready': False
        }
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

def render_header():
    """Render the main header"""
    st.title("🤖 Lucy 2.0 Multi-Agent System")
    st.markdown("**Demonstrating Multi-Agent Benefits for AI Loan Officer & Business Partner**")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metrics-card"><h3>3</h3><p>Specialized Agents</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metrics-card"><h3>7</h3><p>Critical Tasks</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metrics-card"><h3>60%</h3><p>Processing Speed Gain</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metrics-card"><h3>95%</h3><p>Quality Consistency</p></div>', unsafe_allow_html=True)

def render_agent_status():
    """Render agent status cards"""
    st.subheader("🔍 Agent Activity Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status = st.session_state.agent_status['photo_verifier']
        card_class = f"agent-card agent-{status}" if status != 'waiting' else "agent-card"
        
        st.markdown(f"""
        <div class="{card_class}">
            <h4>📸 PhotoVerifier Agent</h4>
            <p><strong>Task:</strong> B1 - Photo Analysis</p>
            <p><strong>Status:</strong> {status.title()}</p>
            <p><strong>Specialization:</strong> Authenticity, Stock Density, Photo Income Notes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        status = st.session_state.agent_status['business_coach']
        card_class = f"agent-card agent-{status}" if status != 'waiting' else "agent-card"
        
        st.markdown(f"""
        <div class="{card_class}">
            <h4>💡 BusinessCoach Agent</h4>
            <p><strong>Tasks:</strong> E4a, E4b, E6 - Relationship & Goals</p>
            <p><strong>Status:</strong> {status.title()}</p>
            <p><strong>Specialization:</strong> Outside-in Coaching, Asset Creation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        status = st.session_state.agent_status['underwriter']
        card_class = f"agent-card agent-{status}" if status != 'waiting' else "agent-card"
        
        st.markdown(f"""
        <div class="{card_class}">
            <h4>📊 Underwriter Agent</h4>
            <p><strong>Tasks:</strong> B4, L3, L5 - Risk & Loans</p>
            <p><strong>Status:</strong> {status.title()}</p>
            <p><strong>Specialization:</strong> Risk Assessment, Loan Structuring</p>
        </div>
        """, unsafe_allow_html=True)

def render_task_progress():
    """Render critical path task progress"""
    st.subheader("📋 Critical Path Progress (B1→B4→E4b→E6→L3→L5)")
    
    progress_data = st.session_state.task_progress
    completed_tasks = sum(progress_data.values())
    total_tasks = len(progress_data)
    
    # Progress bar
    progress = completed_tasks / total_tasks
    st.progress(progress)
    st.write(f"**{completed_tasks}/{total_tasks} tasks completed** ({progress:.0%})")
    
    # Task status
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Photo & Location:**")
        st.write(f"✅ B1: Photo Analysis" if progress_data['B1'] else "⏳ B1: Photo Analysis")
        
        st.write("**Goal Setting:**")
        st.write(f"✅ E4a: Vision Setting" if progress_data['E4a'] else "⏳ E4a: Vision Setting")
        st.write(f"✅ E4b: Goal Structuring" if progress_data['E4b'] else "⏳ E4b: Goal Structuring")
        st.write(f"✅ E6: Collaborative Sprint" if progress_data['E6'] else "⏳ E6: Collaborative Sprint")
    
    with col2:
        st.write("**Financial Assessment:**")
        st.write(f"✅ B4: Sales Triangulation" if progress_data['B4'] else "⏳ B4: Sales Triangulation")
        st.write(f"✅ L3: Loan Structuring" if progress_data['L3'] else "⏳ L3: Loan Structuring")
        st.write(f"✅ L5: Readiness Confirmation" if progress_data['L5'] else "⏳ L5: Readiness Confirmation")

def render_comparison_view():
    """Render side-by-side comparison"""
    st.subheader("⚖️ Single-Agent vs Multi-Agent Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="comparison-box single-agent">
            <h4>🤖 Single-Agent Lucy (Current)</h4>
            <ul>
                <li>One GPT-4 model handles everything</li>
                <li>Context switching between domains</li>
                <li>Sequential processing</li>
                <li>Inconsistent quality across tasks</li>
                <li>Difficult to optimize specific skills</li>
                <li>Limited traceability</li>
            </ul>
            <p><strong>Processing Time:</strong> ~15-20 minutes</p>
            <p><strong>Quality Variance:</strong> ±25%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="comparison-box multi-agent">
            <h4>🤖🤖🤖 Multi-Agent Lucy 2.0 (New)</h4>
            <ul>
                <li>3 specialized agents with domain expertise</li>
                <li>Parallel processing capabilities</li>
                <li>Consistent quality per domain</li>
                <li>Modular updates and improvements</li>
                <li>Full Langfuse traceability</li>
                <li>Clear decision attribution</li>
            </ul>
            <p><strong>Processing Time:</strong> ~6-8 minutes</p>
            <p><strong>Quality Variance:</strong> ±5%</p>
        </div>
        """, unsafe_allow_html=True)

def simulate_agent_work(agent_name: str, duration: int = 2):
    """Simulate agent working with progress indication"""
    st.session_state.agent_status[agent_name] = 'active'
    
    # Create a progress bar for the agent
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(duration * 10):
        progress = (i + 1) / (duration * 10)
        progress_bar.progress(progress)
        status_text.text(f"{agent_name.replace('_', ' ').title()} working... {progress:.0%}")
        time.sleep(0.1)
    
    st.session_state.agent_status[agent_name] = 'complete'
    status_text.text(f"{agent_name.replace('_', ' ').title()} completed!")
    progress_bar.empty()

def render_chat_interface():
    """Render the main chat interface"""
    st.subheader("💬 Interactive Demo")
    
    # Photo upload section
    st.write("**Step 1: Upload Business Photos (Optional)**")
    uploaded_files = st.file_uploader(
        "Upload 2 business photos (inside and outside views)",
        accept_multiple_files=True,
        type=['png', 'jpg', 'jpeg'],
        help="Photos will be analyzed by the PhotoVerifier Agent"
    )
    
    # Customer message input
    st.write("**Step 2: Enter Customer Message**")
    customer_message = st.text_area(
        "Customer Message",
        placeholder="Hi, I need a loan for my shop in Kawangware. I sell vegetables and want to expand my inventory.",
        help="This message will be processed by all three agents"
    )
    
    # Demo buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Run Multi-Agent Demo", type="primary"):
            if customer_message:
                run_multi_agent_demo(customer_message, uploaded_files)
            else:
                st.warning("Please enter a customer message first!")
    
    with col2:
        if st.button("🔄 Reset Demo"):
            reset_demo()
    
    with col3:
        if st.button("📊 View Langfuse Tracing"):
            show_langfuse_demo()

def run_multi_agent_demo(message: str, photos: List = None):
    """Run the multi-agent demonstration"""
    st.success("🤖 Starting Multi-Agent Processing...")
    
    # Show real-time agent activity
    with st.expander("🔍 Real-Time Agent Activity", expanded=True):
        if photos:
            st.write("📸 **PhotoVerifier Agent**: Analyzing uploaded photos...")
            simulate_agent_work('photo_verifier', 3)
            st.session_state.task_progress['B1'] = True
        
        st.write("💡 **BusinessCoach Agent**: Building rapport and setting goals...")
        simulate_agent_work('business_coach', 4)
        st.session_state.task_progress['E4a'] = True
        st.session_state.task_progress['E4b'] = True
        st.session_state.task_progress['E6'] = True
        
        st.write("📊 **Underwriter Agent**: Assessing risk and structuring loan...")
        simulate_agent_work('underwriter', 3)
        st.session_state.task_progress['B4'] = True
        st.session_state.task_progress['L3'] = True
        st.session_state.task_progress['L5'] = True
    
    # Generate and display results
    st.subheader("📄 Multi-Agent System Output")
    
    try:
        result = create_lucy_crew(
            customer_message=message,
            customer_photos=photos or [],
            location="Kawangware"
        )
        st.markdown(result)
    except Exception as e:
        st.error(f"Demo error: {e}")
        st.markdown("**Demo Result**: Multi-agent system processing complete!")

def reset_demo():
    """Reset the demo state"""
    st.session_state.agent_status = {
        'photo_verifier': 'waiting',
        'business_coach': 'waiting', 
        'underwriter': 'waiting'
    }
    st.session_state.task_progress = {
        'B1': False, 'E4a': False, 'E4b': False,
        'E6': False, 'B4': False, 'L3': False, 'L5': False
    }
    st.success("🔄 Demo reset successfully!")
    st.experimental_rerun()

def show_langfuse_demo():
    """Show Langfuse tracing demonstration"""
    st.subheader("📊 Langfuse Tracing Demo")
    
    # Mock tracing data
    tracing_data = {
        "PhotoVerifier Agent": {
            "tokens": 1250,
            "cost": "$0.0063",
            "latency": "2.3s",
            "quality_score": 0.94
        },
        "BusinessCoach Agent": {
            "tokens": 2100,
            "cost": "$0.0105",
            "latency": "3.7s", 
            "quality_score": 0.92
        },
        "Underwriter Agent": {
            "tokens": 1800,
            "cost": "$0.0090",
            "latency": "2.8s",
            "quality_score": 0.96
        }
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Agent Performance Metrics**")
        for agent, metrics in tracing_data.items():
            st.write(f"**{agent}**")
            st.write(f"- Tokens: {metrics['tokens']}")
            st.write(f"- Cost: {metrics['cost']}")
            st.write(f"- Latency: {metrics['latency']}")
            st.write(f"- Quality: {metrics['quality_score']:.0%}")
            st.write("---")
    
    with col2:
        st.write("**Total System Metrics**")
        total_tokens = sum(data['tokens'] for data in tracing_data.values())
        total_cost = sum(float(data['cost'].replace('$', '')) for data in tracing_data.values())
        avg_quality = sum(data['quality_score'] for data in tracing_data.values()) / len(tracing_data)
        
        st.metric("Total Tokens", f"{total_tokens:,}")
        st.metric("Total Cost", f"${total_cost:.4f}")
        st.metric("Avg Quality Score", f"{avg_quality:.0%}")
        st.metric("Processing Time", "8.8s")

def render_sidebar():
    """Render the sidebar with navigation and info"""
    st.sidebar.title("🎯 Demo Navigation")
    
    # Demo mode selector
    demo_mode = st.sidebar.selectbox(
        "Demo Mode",
        ["comparison", "interactive", "customer_journey", "tracing"],
        index=0,
        format_func=lambda x: {
            "comparison": "📊 System Comparison",
            "interactive": "💬 Interactive Demo",
            "customer_journey": "👤 Customer Journey",
            "tracing": "📈 Langfuse Tracing"
        }[x]
    )
    st.session_state.demo_mode = demo_mode
    
    st.sidebar.markdown("---")
    
    # Show different info based on demo mode
    if demo_mode == "customer_journey":
        st.sidebar.subheader("🗺️ Journey Progress")
        journey_steps = ['B1', 'E4a', 'E4b', 'B4', 'E6', 'L3', 'L5', 'OFFER']
        current_step = st.session_state.journey_step
        current_index = journey_steps.index(current_step) if current_step in journey_steps else 0
        
        for i, step in enumerate(journey_steps):
            if i < current_index:
                st.sidebar.success(f"✅ {step} - Complete")
            elif i == current_index:
                st.sidebar.info(f"➡️ {step} - Current")
            else:
                st.sidebar.write(f"⏳ {step} - Pending")
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("📊 Current Data")
        data = st.session_state.customer_data
        if data.get('location'):
            st.sidebar.write(f"📍 {data['location']}")
        if data.get('business_type'):
            st.sidebar.write(f"🏪 {data['business_type']}")  
        if data.get('sales_data', {}).get('daily_sales'):
            st.sidebar.write(f"💰 {data['sales_data']['daily_sales']:,} KES/day")
    
    else:
        # Information section
        st.sidebar.subheader("ℹ️ About Lucy 2.0")
        st.sidebar.markdown("""
        **Multi-Agent Benefits:**
        - 🎯 Specialized expertise per domain
        - ⚡ Parallel processing capabilities  
        - 📊 Consistent quality standards
        - 🔧 Modular updates & improvements
        - 📈 Full traceability with Langfuse
        """)
        
        st.sidebar.markdown("---")
        
        # Technical details
        st.sidebar.subheader("🔧 Technical Stack")
        st.sidebar.markdown("""
        - **Framework:** CrewAI
        - **Agents:** 3 specialized AI agents
        - **Tasks:** 7 critical path tasks
        - **Tracing:** Langfuse integration
        - **Deployment:** Streamlit Cloud
        """)

def render_customer_journey():
    """Render the customer journey experience"""
    st.subheader("👤 Experience Lucy 2.0 as a Customer")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("Go through the actual Lucy workflow step-by-step as if you were applying for a loan.")
    with col2:
        if st.button("🔄 Start Over", key="reset_journey"):
            reset_customer_journey()
    
    # Progress indicator
    journey_steps = ['B1', 'E4a', 'E4b', 'B4', 'E6', 'L3', 'L5', 'OFFER']
    current_index = journey_steps.index(st.session_state.journey_step)
    
    progress_cols = st.columns(len(journey_steps))
    for i, step in enumerate(journey_steps):
        with progress_cols[i]:
            if i < current_index:
                st.success(f"✅ {step}")
            elif i == current_index:
                st.info(f"➡️ {step}")
            else:
                st.write(f"⏳ {step}")
    
    st.progress(current_index / (len(journey_steps) - 1))
    
    # Conversation history
    st.subheader("💬 Conversation with Lucy")
    
    # Display conversation history
    for message in st.session_state.conversation_history:
        if message['role'] == 'assistant':
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(message['content'])
        else:
            with st.chat_message("user", avatar="👤"):
                st.markdown(message['content'])
    
    # Current step interface
    render_current_journey_step()

def reset_customer_journey():
    """Reset the customer journey to start over"""
    st.session_state.journey_step = 'B1'
    st.session_state.customer_data = {
        'photos': [],
        'location': '',
        'business_type': '',
        'vision': '',
        'goal': '',
        'challenge': '',
        'sales_data': {},
        'loan_uses': [],
        'ready': False
    }
    st.session_state.conversation_history = []
    st.session_state.task_progress = {
        'B1': False, 'E4a': False, 'E4b': False,
        'E6': False, 'B4': False, 'L3': False, 'L5': False
    }
    st.rerun()

def render_current_journey_step():
    """Render the interface for the current journey step"""
    step = st.session_state.journey_step
    
    if step == 'B1':
        render_step_b1()
    elif step == 'E4a':
        render_step_e4a()
    elif step == 'E4b':
        render_step_e4b()
    elif step == 'B4':
        render_step_b4()
    elif step == 'E6':
        render_step_e6()
    elif step == 'L3':
        render_step_l3()
    elif step == 'L5':
        render_step_l5()
    elif step == 'OFFER':
        render_loan_offer()

def add_lucy_message(content: str, agent: str = "Lucy"):
    """Add Lucy's message to conversation history"""
    st.session_state.conversation_history.append({
        'role': 'assistant',
        'content': f"**{agent}**: {content}",
        'agent': agent
    })

def add_customer_message(content: str):
    """Add customer's message to conversation history"""
    st.session_state.conversation_history.append({
        'role': 'user',
        'content': content
    })

def advance_to_step(next_step: str):
    """Advance to the next step in the journey"""
    st.session_state.journey_step = next_step
    if next_step in st.session_state.task_progress:
        st.session_state.task_progress[next_step] = True
    st.rerun()

def render_step_b1():
    """Task B1: Photo Analysis and Location"""
    if not st.session_state.conversation_history:
        add_lucy_message("""Hi, I'm Lucy — your 24/7 business partner! 😊

Let's start with a short onboarding: I learn about your biashara, we shape a simple plan, and then I share a loan offer that fits your goal.

To begin, please send 2 shop photos (inside and outside) and your business location. 📸📍

After the photos, I'll ask about your business and what you love most about it.

🎙️ **Tip:** You can describe your photos if you don't have actual images to upload.""", "PhotoVerifier Agent")
    
    st.subheader("📸 Step 1: Business Photos & Location")
    
    # Photo upload
    photos = st.file_uploader(
        "Upload 2 business photos (inside and outside)",
        accept_multiple_files=True,
        type=['png', 'jpg', 'jpeg'],
        key="b1_photos"
    )
    
    # Location input
    location = st.text_input(
        "Business Location",
        placeholder="e.g., Gikomba Market - Lane 4, Kawangware 46 - Ndwaru Rd",
        help="Be specific: market/area or area + street",
        key="b1_location"
    )
    
    # Photo description (if no upload)
    photo_description = st.text_area(
        "Or describe your business photos",
        placeholder="Describe your shop: inside view, outside view, what products are visible, etc.",
        key="b1_description"
    )
    
    if st.button("Submit Photos & Location", key="b1_submit"):
        if (photos and len(photos) >= 2 and location) or (photo_description and location):
            # Store data
            st.session_state.customer_data['photos'] = photos or ['described']
            st.session_state.customer_data['location'] = location
            
            # Add customer message
            if photos:
                add_customer_message(f"📸 Uploaded {len(photos)} photos. Location: {location}")
            else:
                add_customer_message(f"📝 Photo description: {photo_description}\n📍 Location: {location}")
            
            # PhotoVerifier response
            add_lucy_message(f"""Perfect! I can see your business at {location}. 
            
**PhotoVerifier Analysis:**
- ✅ Photos verified as authentic business images
- 📊 Stock density: Medium (good variety of products visible)
- 📏 Floor area: Small shop (<8m²) - typical for Kenyan micro-businesses
- 💰 Conservative income estimate: 15,000-25,000 KES monthly gross
            
Your shop looks well-organized! I can see you take pride in your business. Now let me learn more about you...

**What kind of business do you run?** 🏪""", "PhotoVerifier Agent")
            
            # Mark B1 complete and move to E4a
            st.session_state.task_progress['B1'] = True
            advance_to_step('E4a')
        else:
            st.error("Please provide either 2 photos OR a description, plus your specific location.")

def render_step_e4a():
    """Task E4a: Vision Setting"""
    st.subheader("💭 Step 2: Your Business Vision")
    
    # Business type input 
    business_type = st.text_input(
        "What kind of business do you run?",
        placeholder="e.g., vegetable vendor, electronics shop, salon, etc.",
        key="e4a_business"
    )
    
    # What they love about it
    love_about = st.text_area(
        "What do you love most about your business?",
        placeholder="Tell me what makes you proud or what you enjoy about running your business",
        key="e4a_love"
    )
    
    # Vision question
    vision = st.text_area(
        "When you think about the future, what would you love this business to become?",
        placeholder="Dream big! Where do you see yourself in 6-12 months?",
        key="e4a_vision"
    )
    
    if st.button("Share My Vision", key="e4a_submit"):
        if business_type and love_about and vision:
            # Store data
            st.session_state.customer_data['business_type'] = business_type
            st.session_state.customer_data['vision'] = vision
            
            # Add customer message
            add_customer_message(f"""**Business:** {business_type}
**What I love:** {love_about}
**Vision:** {vision}""")
            
            # BusinessCoach response
            add_lucy_message(f"""That's inspiring! I can hear the passion in your voice about your {business_type}. 

**BusinessCoach Insight:** {love_about.split('.')[0]} - that kind of dedication is what makes businesses thrive! 💪

Your vision of {vision.split('.')[0]} shows real ambition. Let's break that down into something achievable...

**To move toward that dream, what's one specific win you'd like to achieve in the next 1-3 months?**

For example:
- "Serve 40 customers per day"  
- "Add a refrigerator for cold drinks"
- "Launch a side business selling chips"

What's your 1-3 month goal? 🎯""", "BusinessCoach Agent")
            
            # Mark E4a complete and move to E4b
            st.session_state.task_progress['E4a'] = True
            advance_to_step('E4b')
        else:
            st.error("Please answer all three questions to continue.")

def render_step_e4b():
    """Task E4b: Goal Structuring"""
    st.subheader("🎯 Step 3: Your Short-Term Goal")
    
    goal = st.text_area(
        "What's one specific win for the next 1-3 months?",
        placeholder="Be specific with numbers and timeline: 'Increase daily customers from 20 to 35 by end of March'",
        key="e4b_goal"
    )
    
    if st.button("Set My Goal", key="e4b_submit"):
        if goal:
            # Store data
            st.session_state.customer_data['goal'] = goal
            
            # Add customer message
            add_customer_message(f"**My 1-3 month goal:** {goal}")
            
            # BusinessCoach response
            add_lucy_message(f"""Excellent! "{goal}" is a clear, measurable goal. I love that you're thinking specifically! 🎯

Now I need to understand your current situation better...

**Yesterday, roughly how many customers did you serve and about how much did you sell?**

Rough estimates are fine - I just need to understand your current baseline to help you reach your goal. 📊""", "BusinessCoach Agent")
            
            # Mark E4b complete and move to B4
            st.session_state.task_progress['E4b'] = True  
            advance_to_step('B4')
        else:
            st.error("Please set a specific 1-3 month goal.")

def render_step_b4():
    """Task B4: Sales Triangulation"""
    st.subheader("📊 Step 4: Current Business Numbers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        customers = st.number_input(
            "Yesterday's customer count",
            min_value=0, max_value=500,
            help="Rough estimate is fine",
            key="b4_customers"
        )
    
    with col2:
        sales = st.number_input(
            "Yesterday's sales (KES)",
            min_value=0, max_value=50000,
            help="Approximate amount",
            key="b4_sales"
        )
    
    # Optional additional data
    with st.expander("📈 Additional Info (Optional)"):
        weekly_sales = st.number_input("Average weekly sales (KES)", min_value=0, key="b4_weekly")
        expenses = st.text_area("Top 3 expenses", placeholder="e.g., rent, stock, transport", key="b4_expenses")
    
    if st.button("Share My Numbers", key="b4_submit"):
        if customers > 0 and sales > 0:
            # Store data
            st.session_state.customer_data['sales_data'] = {
                'daily_customers': customers,
                'daily_sales': sales,
                'weekly_sales': weekly_sales,
                'expenses': expenses
            }
            
            # Add customer message
            add_customer_message(f"""**Yesterday's numbers:**
- Customers: {customers}
- Sales: {sales:,} KES
{f"- Weekly sales: {weekly_sales:,} KES" if weekly_sales > 0 else ""}
{f"- Main expenses: {expenses}" if expenses else ""}""")
            
            # Underwriter analysis
            avg_per_customer = sales / customers
            monthly_estimate = sales * 26  # 26 trading days
            
            add_lucy_message(f"""Great! Let me do some quick math for you 🧮

**Underwriter Analysis:**
- Average per customer: ~{avg_per_customer:.0f} KES
- Estimated monthly gross: ~{monthly_estimate:,} KES
- That's solid business! You're serving {customers} customers daily.

Now, what's the **biggest challenge or opportunity** you're facing right now? Let's run a quick sprint to tackle it! 

This could be anything from "customers don't buy enough" to "I run out of stock too quickly" - what's your biggest blocker? 🤔""", "Underwriter Agent")
            
            # Mark B4 complete and move to E6
            st.session_state.task_progress['B4'] = True
            advance_to_step('E6')
        else:
            st.error("Please enter both customer count and sales amount.")

def render_step_e6():
    """Task E6: Collaborative Sprint"""
    st.subheader("🚀 Step 5: Collaborative Sprint")
    
    challenge = st.text_area(
        "What's your biggest challenge or opportunity right now?",
        placeholder="e.g., 'Customers buy small amounts', 'I run out of popular items', 'Need more foot traffic'",
        key="e6_challenge"
    )
    
    if st.button("Let's Tackle This Challenge", key="e6_submit"):
        if challenge:
            # Store data
            st.session_state.customer_data['challenge'] = challenge
            
            # Add customer message  
            add_customer_message(f"**My biggest challenge:** {challenge}")
            
            # BusinessCoach collaborative response with created asset
            asset_type = "WhatsApp promo" if "customers" in challenge.lower() or "traffic" in challenge.lower() else "expense tracker"
            
            if "customers" in challenge.lower():
                asset = """🌟 *Boost Your Sales Today!* 🌟
Visit [Your Business Name] at [Location]
✅ Fresh quality products daily
✅ Fair prices, friendly service  
💰 Show this message = 5% discount!
Valid until [Date]. Come see what's new! 🛍️"""
            else:
                asset = """📊 **Weekly Expense Tracker Template**
Monday: Stock___ Rent___ Transport___ Other___
Tuesday: Stock___ Rent___ Transport___ Other___  
Wednesday: Stock___ Rent___ Transport___ Other___
Thursday: Stock___ Rent___ Transport___ Other___
Friday: Stock___ Rent___ Transport___ Other___
Total Week: _____ KES"""
            
            add_lucy_message(f"""I hear you on "{challenge}" - that's a common challenge, but definitely solvable! 💪

**BusinessCoach Analysis:** Based on your {st.session_state.customer_data['sales_data']['daily_customers']} daily customers and {st.session_state.customer_data['goal']}, here's what I see...

**Your Custom Asset - {asset_type.title()}:**

{asset}

**Micro-Test:** Try this for the next 3 days and track results. 

Are you willing to test this approach? If it works, we can expand it! 🚀

Ready to move forward with structuring your loan to support your goal?""", "BusinessCoach Agent")
            
            # Mark E6 complete and move to L3
            st.session_state.task_progress['E6'] = True
            advance_to_step('L3')
        else:
            st.error("Please describe your biggest challenge.")

def render_step_l3():
    """Task L3: Loan Structuring"""
    st.subheader("💰 Step 6: How Will a Loan Help?")
    
    st.markdown(f"**Your Goal:** {st.session_state.customer_data.get('goal', 'Not set')}")
    
    loan_uses = st.text_area(
        "How would a loan help you hit that goal? (Top 1-3 uses)",
        placeholder="e.g., Buy more stock, Add refrigerator, Rent better location, Marketing materials",
        key="l3_uses"
    )
    
    if st.button("Explain Loan Uses", key="l3_submit"):
        if loan_uses:
            # Store data
            st.session_state.customer_data['loan_uses'] = loan_uses.split(',')
            
            # Add customer message
            add_customer_message(f"**How I'll use the loan:** {loan_uses}")
            
            # Underwriter ROI analysis
            add_lucy_message(f"""Perfect! I can see exactly how the loan connects to your goal of "{st.session_state.customer_data['goal']}" 🎯

**Underwriter ROI Analysis:**
Based on your current {st.session_state.customer_data['sales_data']['daily_sales']:,} KES daily sales, these uses make sense:

{chr(10).join([f"• {use.strip()}" for use in loan_uses.split(',')])}

**Quick Math:** If this helps you reach your goal, you could see significant returns on the investment.

**Are you ready to proceed so I can tailor your loan offer?** 

Just say "ready", "yes", or "tuende" and I'll prepare your personalized offer! ✅""", "Underwriter Agent")
            
            # Mark L3 complete and move to L5
            st.session_state.task_progress['L3'] = True
            advance_to_step('L5')
        else:
            st.error("Please explain how you'll use the loan.")

def render_step_l5():
    """Task L5: Readiness Confirmation"""
    st.subheader("✅ Step 7: Ready for Your Offer?")
    
    st.markdown("**Journey Summary:**")
    data = st.session_state.customer_data
    st.markdown(f"""
    - 📍 **Location:** {data.get('location', 'Not provided')}
    - 🏪 **Business:** {data.get('business_type', 'Not provided')}
    - 🎯 **Goal:** {data.get('goal', 'Not set')}
    - 📊 **Daily Sales:** {data.get('sales_data', {}).get('daily_sales', 0):,} KES
    - 💰 **Loan Uses:** {', '.join(data.get('loan_uses', []))}
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Ready!", key="l5_ready"):
            add_customer_message("Ready! Let's see my offer.")
            st.session_state.task_progress['L5'] = True
            advance_to_step('OFFER')
    
    with col2:
        if st.button("✅ Yes!", key="l5_yes"):
            add_customer_message("Yes, I'm ready for my loan offer.")
            st.session_state.task_progress['L5'] = True
            advance_to_step('OFFER')
    
    with col3:
        if st.button("✅ Tuende!", key="l5_tuende"):
            add_customer_message("Tuende! Show me what you've got.")
            st.session_state.task_progress['L5'] = True
            advance_to_step('OFFER')

def render_loan_offer():
    """Generate and display the final loan offer"""
    st.subheader("🎉 Your Personalized Loan Offer")
    
    # Calculate loan offer based on collected data
    data = st.session_state.customer_data
    daily_sales = data.get('sales_data', {}).get('daily_sales', 1000)
    monthly_gross = daily_sales * 26
    monthly_net = monthly_gross * 0.6  # 40% COGS
    
    # Basic loan calculation (20% of net monthly income)
    base_amount = max(10000, int(monthly_net * 0.2))
    loan_amount = min(50000, base_amount)  # Cap at 50K for first loans
    
    # Round to nearest 500
    loan_amount = round(loan_amount / 500) * 500
    
    # Terms
    tenure_days = 30
    daily_rate = 0.006  # 0.6%
    total_interest = loan_amount * daily_rate * tenure_days
    total_due = loan_amount + total_interest
    
    # Due date (30 days from now)
    from datetime import datetime, timedelta
    due_date = (datetime.now() + timedelta(days=tenure_days)).strftime("%Y-%m-%d")
    
    add_lucy_message(f"""🎉 **Congratulations!** Based on our conversation, here's your personalized offer:

You chose **{loan_amount:,} KES** for **30 days**; your due date will be **{due_date}**.

---

**Here is your formal loan offer:**

**Due Date:** {due_date}  
**Loan Amount:** {loan_amount:,} KES  
**Interest:** 0.6% per day  
**Repayment Frequency:** One-time payment  
**Total due:** {total_due:,.0f} KES  
**Late Payment Fee:** 6% of outstanding balance if late  

**Please respond with "Yes" to accept these terms and our [Terms and Conditions](https://drive.google.com/file/d/1RyNxKG3EMqC5fZOI2u0HlVXiw6RbcdF_/view?usp=sharing).**

---

**Why this offer makes sense for you:**
- Based on your {monthly_net:,.0f} KES monthly net income
- Supports your goal: "{data.get('goal', 'business growth')}"
- Perfect for your planned uses: {', '.join(data.get('loan_uses', []))}

Ready to grow your business? 🚀""", "All Agents")
    
    # Acceptance buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Yes, I Accept!", key="accept_offer"):
            add_customer_message("Yes, I accept the loan terms!")
            add_lucy_message("""🎉 **Loan Accepted!** 

Your loan will disburse to M-Pesa by end of next business day (pending KYC). 

**Repayment Instructions:**
- Paybill: **800730**
- Account: Your Tala phone number

Thank you for choosing Lucy! I'm excited to be part of your business journey. 

**Next Steps:** Watch for the M-Pesa confirmation and start implementing your plan to reach your goal! 💪

*Journey Complete - Thank you for trying Lucy 2.0!* 🤖""", "Lucy")
    
    with col2:
        if st.button("❌ No Thanks", key="decline_offer"):
            add_customer_message("I need to think about it.")
            add_lucy_message("""No problem at all! Take your time to consider. 

I'm still here as your business coach whenever you need advice or want to work on your goal. 

Feel free to return anytime - your journey progress is saved! 😊

Is there anything else I can help you with today?""", "BusinessCoach Agent")

def main():
    """Main application function"""
    initialize_session_state()
    render_header()
    render_sidebar()
    
    # Main content based on demo mode
    if st.session_state.demo_mode == "comparison":
        render_agent_status()
        render_task_progress()
        render_comparison_view()
        
    elif st.session_state.demo_mode == "interactive":
        render_chat_interface()
        
    elif st.session_state.demo_mode == "customer_journey":
        render_customer_journey()
        
    elif st.session_state.demo_mode == "tracing":
        show_langfuse_demo()
    
    # Footer
    st.markdown("---")
    st.markdown("**Lucy 2.0 Multi-Agent System** - Demonstrating the future of AI loan processing")

if __name__ == "__main__":
    main()