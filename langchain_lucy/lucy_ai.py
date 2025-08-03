"""
Lucy 2.0 - LangChain Multi-Agent Implementation
Seamless customer experience with invisible agent orchestration
"""

from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import json
import os

# Try to import LangChain, fallback to basic types if not available
try:
    from langchain.schema import BaseMessage, SystemMessage, HumanMessage, AIMessage
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema.runnable import Runnable
    from langchain.tools import tool
    LANGCHAIN_AVAILABLE = True
except ImportError:
    # Fallback to basic message types for demo mode
    class BaseMessage:
        def __init__(self, content: str): self.content = content
    class SystemMessage(BaseMessage): pass
    class HumanMessage(BaseMessage): pass  
    class AIMessage(BaseMessage): pass
    class ChatOpenAI:
        def __init__(self, **kwargs): pass
        def invoke(self, messages): 
            return AIMessage("Demo response - LangChain not installed")
    class ChatPromptTemplate:
        @staticmethod
        def from_messages(messages): return ChatPromptTemplate()
        def format_messages(self, **kwargs): return [SystemMessage("Demo")]
    LANGCHAIN_AVAILABLE = False


class LucyTask(Enum):
    """Lucy's critical path tasks"""
    B1 = "B1"  # Photos & Location
    E4A = "E4a"  # Vision Setting  
    E4B = "E4b"  # Goal Structuring
    B4 = "B4"  # Sales Triangulation
    E6 = "E6"  # Collaborative Sprint
    L3 = "L3"  # Loan Structuring
    L5 = "L5"  # Readiness Confirmation
    OFFER = "OFFER"  # Loan Offer


@dataclass
class CustomerData:
    """Track customer data throughout the journey"""
    # B1 Data
    photos: List[str] = field(default_factory=list)
    location: str = ""
    
    # E4a/E4b Data
    business_type: str = ""
    what_they_love: str = ""
    vision: str = ""
    goal: str = ""
    
    # B4 Data
    daily_customers: int = 0
    daily_sales: int = 0
    weekly_sales: int = 0
    expenses: str = ""
    
    # E6 Data
    challenge: str = ""
    created_asset: str = ""
    
    # L3 Data
    loan_uses: List[str] = field(default_factory=list)
    
    # Task completion tracking
    completed_tasks: List[LucyTask] = field(default_factory=list)


@dataclass 
class LucyState:
    """Lucy's conversation state"""
    current_task: LucyTask = LucyTask.B1
    customer_data: CustomerData = field(default_factory=CustomerData)
    conversation_history: List[BaseMessage] = field(default_factory=list)
    session_id: str = ""
    
    def is_task_complete(self, task: LucyTask) -> bool:
        return task in self.customer_data.completed_tasks
    
    def complete_task(self, task: LucyTask):
        if task not in self.customer_data.completed_tasks:
            self.customer_data.completed_tasks.append(task)
            # Call task completion function
            self.mark_task_complete(task.value, len(self.customer_data.completed_tasks), 7)
    
    def mark_task_complete(self, task_id: str, completed_tasks: int, total_tasks: int) -> dict:
        """Simulate the task_complete function call"""
        # In real implementation, this would call the actual function
        return {
            "task_id": task_id,
            "completed_tasks": completed_tasks,
            "total_tasks": total_tasks,
            "completion_percentage": (completed_tasks / total_tasks) * 100
        }
    
    def get_next_task(self) -> Optional[LucyTask]:
        """Get the next task in the critical path"""
        critical_path = [LucyTask.B1, LucyTask.E4A, LucyTask.E4B, LucyTask.B4, 
                        LucyTask.E6, LucyTask.L3, LucyTask.L5, LucyTask.OFFER]
        
        for task in critical_path:
            if not self.is_task_complete(task):
                return task
        return None


class PhotoVerifierAgent:
    """Specialized agent for photo analysis and income estimation"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are Lucy's PhotoVerifier specialist. You analyze business photos with expertise in Kenyan micro-business environments.

Your job:
1. Assess authenticity (flag watermarks, stock images, screenshots)
2. Evaluate stock density (low/medium/high)
3. Determine floor area tier (small <8m², medium 8-20m², large >20m²)
4. Generate conservative income estimates
5. Create Photo Income Notes

Always respond as Lucy - customers don't know you're a separate agent.
Be warm, professional, and use emojis appropriately."""),
            ("human", "{input}")
        ])
        
    def analyze_photos(self, photos: List[str], location: str) -> str:
        """Analyze photos and return Lucy's response"""
        
        # Only analyze if photos are actually provided
        if not photos or len(photos) == 0:
            return f"""Thanks for sharing your location: {location}! 📍

I'd love to see your business to better understand your setup. Could you please share 2 photos of your shop:
1️⃣ **Inside view** - showing your products/stock
2️⃣ **Outside view** - showing your shop front

This helps me assess your business and create the perfect loan offer for you! 📸"""
        
        if not LANGCHAIN_AVAILABLE:
            # Demo mode response - but only when photos are provided
            return f"""Great photos! I can see your business at {location} 📸

**Photo Analysis:**
✅ **Authenticity**: Photos verified as genuine business images
✅ **Stock Density**: Medium - good variety of products visible
✅ **Floor Area**: Small to medium typical micro-business setup  
✅ **Business Assessment**: Active retail operation with regular turnover

Based on what I see, this looks like a solid business! The location and setup suggest monthly income potential of 15,000-25,000 KES.

Now, tell me more about your business - what type of products do you mainly sell? 🛍️"""
        
        # Simulate photo analysis (in real implementation, this would use vision models)
        analysis_prompt = f"""
        A customer has shared {len(photos)} business photos and says their location is: {location}
        
        Please provide Lucy's warm response that includes:
        1. Acknowledge the photos and location
        2. Photo analysis results (authenticity, stock density, floor area)
        3. Conservative income estimate 
        4. Smooth transition to asking about their business type
        
        Keep it conversational and encouraging.
        """
        
        response = self.llm.invoke([
            SystemMessage(content=self.prompt.format_messages(input=analysis_prompt)[0].content),
            HumanMessage(content=analysis_prompt)
        ])
        
        return response.content


class BusinessCoachAgent:
    """Specialized agent for relationship building and goal setting"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are Lucy's BusinessCoach specialist. You excel at the "outside-in" approach:
- Start with identity and dreams before numbers
- Ask ONE question at a time
- Create tangible assets (WhatsApp promos, expense trackers, layout sketches)
- Design micro-tests customers can complete in 1-3 days

You understand Kenyan micro-business challenges and speak the customer's language mix.
Always respond as Lucy - customers don't know you're a separate agent.
Be warm, encouraging, and use emojis appropriately."""),
            ("human", "{input}")
        ])
    
    def build_rapport(self, customer_data: CustomerData, current_task: LucyTask, user_message: str = "") -> str:
        """Handle relationship building tasks"""
        
        # Handle direct questions about Lucy's role
        message_lower = user_message.lower()
        if any(phrase in message_lower for phrase in ["what is your job", "who are you", "what do you do"]):
            return """I'm Lucy, your AI business partner and loan officer! 🤖

My job is to:
- Learn about your business and goals
- Help you grow through coaching and tips
- Structure the perfect loan offer for your needs

I'm here to make getting business credit simple and personal. Now, let's focus on **your** business - what kind of business do you run? 💼"""
        
        # Handle questions about what business Lucy sees
        if any(phrase in message_lower for phrase in ["what business", "what do you see", "see my business"]):
            if not customer_data.photos:
                return """I don't see any photos yet! 📸 

Could you please share 2 photos of your business so I can better understand your setup:
1️⃣ Inside view - showing your products/stock
2️⃣ Outside view - showing your shop front

Once I see your business, I can give you much better insights and loan recommendations! 🏪"""
            else:
                return f"""From your photos, I can see you have a business at {customer_data.location}. I'd love to learn more details from you directly!

What type of business do you run? (grocery shop, restaurant, salon, etc.) 

And what do you **love most** about running your business? 💫"""
        
        if not LANGCHAIN_AVAILABLE:
            # Demo mode responses - but more contextual
            if current_task == LucyTask.E4A:
                return """Perfect! Now I'd love to learn more about you and your business. 

What kind of business do you run? And more importantly - what do you **love most** about it? 

I find that the best business partnerships start with understanding what drives you as an entrepreneur! 💼✨"""
            
            elif current_task == LucyTask.E4B:
                passion = customer_data.what_they_love if customer_data.what_they_love else "your business"
                return f"""I love that! It's clear you're passionate about {passion} 🌟

That passion is exactly what makes businesses succeed. Now, let's think about the future:

What's your biggest **goal** for your business in the next 1-3 months? What would you love to achieve or improve? 

This helps me understand how a loan could support your vision! 🎯"""
            
            elif current_task == LucyTask.E6:
                return f"""That's a fantastic goal! I can see you have a clear vision for growth. 

Now, what's the **biggest challenge or obstacle** you're facing right now that's preventing you from reaching that goal?

Once I understand this, I might even be able to create a helpful resource or tool for you! 🛠️"""
            
            else:
                return "Let me help you with the next step in our conversation! 😊"
        
        if current_task == LucyTask.E4A:
            prompt = "Ask the customer what kind of business they run and what they love about it. Be warm and encouraging."
        elif current_task == LucyTask.E4B:
            prompt = f"The customer loves: '{customer_data.what_they_love}' about their {customer_data.business_type}. Now ask about their 1-3 month goal."
        elif current_task == LucyTask.E6:
            prompt = f"The customer's goal is: '{customer_data.goal}'. Ask about their biggest challenge and offer to create a helpful asset."
        else:
            prompt = "Continue the coaching conversation naturally."
            
        response = self.llm.invoke([
            SystemMessage(content=self.prompt.format_messages(input=prompt)[0].content),
            HumanMessage(content=prompt)
        ])
        
        return response.content
    
    def create_asset(self, challenge: str, business_type: str) -> Tuple[str, str]:
        """Create a tangible asset based on the challenge"""
        
        # Simple asset creation logic
        if "customers" in challenge.lower() or "traffic" in challenge.lower():
            asset_type = "WhatsApp Promo"
            asset = f"""🌟 *Boost Your {business_type} Today!* 🌟
Visit [Your Business Name] at [Location]
✅ Fresh quality products daily
✅ Fair prices, friendly service  
💰 Show this message = 5% discount!
Valid until [Date]. Come see what's new! 🛍️"""
        else:
            asset_type = "Expense Tracker"
            asset = """📊 **Weekly Expense Tracker Template**
Monday: Stock___ Rent___ Transport___ Other___
Tuesday: Stock___ Rent___ Transport___ Other___  
Wednesday: Stock___ Rent___ Transport___ Other___
Thursday: Stock___ Rent___ Transport___ Other___
Friday: Stock___ Rent___ Transport___ Other___
Total Week: _____ KES"""
        
        return asset_type, asset
    
    def give_business_tip(self, business_type: str = "business") -> str:
        """Give instant business tips like in the UI screenshots"""
        
        tips = [
            {
                "tip": "Ask your regular customers what other products they wish you had in your shop. Sometimes, small requests (like a certain snack or mixer) can turn into big sales if you listen and act fast! 👂📝",
                "follow_up": "Would you like another tip, or do you want to try a different feature like tracking your daily sales (2) or planning for new products (3)? Just reply with the number or let me know!"
            },
            {
                "tip": "Keep track of your best-selling hours! Notice when most customers come (morning rush, lunch time, evening). Then make sure you're fully stocked during those peak times! ⏰📈",
                "follow_up": "Want more tips? Reply (1) for more tips, (2) to track daily sales, or (3) for product planning advice!"
            },
            {
                "tip": "Create a simple 'customer loyalty' system - every 10th purchase gets a small discount. Word spreads fast about good deals! 🎯💰",
                "follow_up": "What would help you most? (1) Another tip, (2) Sales tracking, or (3) Product planning? Just send the number!"
            }
        ]
        
        import random
        selected_tip = random.choice(tips)
        
        return f"""Great choice! 🚀

Here's a quick business tip to help increase your sales:

**Tip:**
{selected_tip['tip']}

{selected_tip['follow_up']}"""


class UnderwriterAgent:
    """Specialized agent for risk assessment and loan structuring"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are Lucy's Underwriter specialist. You have deep knowledge of Kenyan micro-business cash flows and follow exact underwriting policy:

- Photo Income Notes anchor decisions
- Behavioral scoring (willingness/capability/follow-through/integrity)
- Loan pricing: 0.6% daily (≤60 days) or 0.2% daily (61-180 days for repeat)
- Critical path: B1→B4→E4b→E6→L3→L5 must be complete

Always respond as Lucy - customers don't know you're a separate agent.
Be professional but warm, and show your math clearly."""),
            ("human", "{input}")
        ])
    
    def analyze_financials(self, customer_data: CustomerData) -> str:
        """Analyze customer's financial data"""
        
        if customer_data.daily_sales and customer_data.daily_customers:
            avg_per_customer = customer_data.daily_sales / customer_data.daily_customers
            monthly_estimate = customer_data.daily_sales * 26
            
            analysis = f"""Great! Let me do some quick math for you 🧮

**My Analysis:**
- Average per customer: ~{avg_per_customer:.0f} KES
- Estimated monthly gross: ~{monthly_estimate:,} KES
- That's solid business! You're serving {customer_data.daily_customers} customers daily.

Now, what's the **biggest challenge or opportunity** you're facing right now?"""
            
            return analysis
        else:
            return "I need your sales numbers to help structure the right loan for you."
    
    def generate_loan_offer(self, customer_data: CustomerData) -> str:
        """Generate final loan offer using the proper function"""
        
        # Calculate loan offer parameters
        monthly_gross = customer_data.daily_sales * 26 if customer_data.daily_sales else 20000
        monthly_net = monthly_gross * 0.6  # 40% COGS
        
        # Basic loan calculation (20% of net monthly income)
        base_amount = max(10000, int(monthly_net * 0.2))
        loan_amount = min(50000, base_amount)  # Cap at 50K for first loans
        loan_amount = round(loan_amount / 500) * 500  # Round to nearest 500
        
        # Terms
        tenure_days = 30
        daily_rate = 0.006  # 0.6%
        loan_type = "SHORT_TERM" if tenure_days <= 60 else "LONG_TERM"
        
        # Create underwriting summary
        underwriting_summary = {
            "offer_sequence": 1,
            "estimated_monthly_income": monthly_net,
            "income_justification": f"Based on daily sales of {customer_data.daily_sales} KES with {customer_data.daily_customers} customers",
            "behavioral_scores": {
                "willingness_score": 4,
                "capability_score": 4,
                "follow_through_score": 4,
                "integrity_score": 4,
                "total_score": 16
            },
            "score_justifications": {
                "willingness": "Customer actively seeking growth capital and engaged in conversation",
                "capability": "Demonstrates clear business understanding and goal articulation",
                "follow_through": "Completed full onboarding process with detailed responses",
                "integrity": "Provided authentic business information and photos"
            },
            "loan_amount_offered": loan_amount,
            "tenure": tenure_days,
            "interest_rate": daily_rate,
            "decision_summary": f"Approved based on estimated monthly income of {monthly_net:,.0f} KES, strong behavioral scores (16/20), and clear business growth plan. Loan amount represents conservative 20% of monthly net income to ensure repayment capacity.",
            "offer_status": "initial",
            "improvement_reason": "First loan offer based on initial assessment",
            "photoIncomeNote": f"• Stock: Medium density • Floor: <8m² typical micro-business • Net: {monthly_net:,.0f} KES/month • Cross-check: Daily sales align with visual assessment • Decision: Approve conservative amount"
        }
        
        # Calculate total due
        total_interest = loan_amount * daily_rate * tenure_days
        total_due = loan_amount + total_interest
        
        # Due date
        from datetime import datetime, timedelta
        due_date = (datetime.now() + timedelta(days=tenure_days)).strftime("%Y-%m-%d")
        
        # Call the loan calculation function (simulated)
        loan_result = self.calculate_loan_offer(
            interestRate=daily_rate,
            loanAmount=loan_amount,
            tenure=tenure_days,
            loanType=loan_type,
            underwritingSummary=underwriting_summary
        )
        
        offer = f"""🎉 **Congratulations!** Based on our conversation, here's your personalized offer:

**Here is your formal loan offer:**

**Due Date:** {due_date}  
**Loan Amount:** {loan_amount:,} KES  
**Interest:** 0.6% per day  
**Repayment Frequency:** One-time payment  
**Total due:** {total_due:,.0f} KES  
**Late Payment Fee:** 6% of outstanding balance if late  

**Why this offer makes sense for you:**
- Based on your {monthly_net:,.0f} KES monthly net income
- Supports your goal for growth
- Perfect for: {', '.join(customer_data.loan_uses)}

**Please respond with "Yes" to accept these terms.**

Ready to grow your business? 🚀"""

        return offer
    
    def calculate_loan_offer(self, interestRate: float, loanAmount: int, tenure: int, loanType: str, underwritingSummary: dict) -> dict:
        """Simulate the calculate_loan_offer function call"""
        # In real implementation, this would call the actual function
        # For now, return structured data
        return {
            "loan_amount": loanAmount,
            "interest_rate": interestRate,
            "tenure": tenure,
            "loan_type": loanType,
            "total_interest": loanAmount * interestRate * tenure,
            "total_due": loanAmount + (loanAmount * interestRate * tenure),
            "underwriting": underwritingSummary
        }


class LucyAI:
    """Main Lucy AI system - seamless customer experience with multi-agent backend"""
    
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=openai_api_key,
            temperature=0.7
        )
        
        # Initialize specialized agents
        self.photo_verifier = PhotoVerifierAgent(self.llm)
        self.business_coach = BusinessCoachAgent(self.llm)
        self.underwriter = UnderwriterAgent(self.llm)
        
        # Router for determining which agent to use
        self.router_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are Lucy's internal router. Analyze the customer message and current state to determine which agent should handle the response.

Current task priorities:
- B1: PhotoVerifier handles photos and location
- E4a/E4b: BusinessCoach handles vision and goals  
- B4: Underwriter handles sales data
- E6: BusinessCoach handles challenges and asset creation
- L3: Underwriter handles loan uses
- L5/OFFER: Underwriter handles final offer

Return only: "photo_verifier", "business_coach", or "underwriter" """),
            ("human", "Current task: {current_task}\nCustomer message: {message}")
        ])
    
    def chat(self, message: str, photos: List[str] = None, state: LucyState = None) -> Tuple[str, LucyState]:
        """Main chat interface - customer sends message, gets Lucy's response"""
        
        if state is None:
            state = LucyState(session_id=str(datetime.now().timestamp()))
        
        # Add customer message to history
        state.conversation_history.append(HumanMessage(content=message))
        
        # Handle initial greeting
        if not state.conversation_history or len(state.conversation_history) == 1:
            response = self._initial_greeting()
            state.conversation_history.append(AIMessage(content=response))
            return response, state
        
        # Route to appropriate agent
        agent_choice = self._route_message(message, state.current_task)
        
        # Process with chosen agent
        response = self._process_with_agent(agent_choice, message, photos, state)
        
        # Update state based on response
        self._update_state(response, message, photos, state)
        
        # Add response to history
        state.conversation_history.append(AIMessage(content=response))
        
        return response, state
    
    def _initial_greeting(self) -> str:
        """Lucy's initial greeting - matching UI screenshots"""
        return """Hi 👋 I'm Lucy - your business partner, powered by Tala!

I help hardworking Kenyan entrepreneurs like you grow your business AND access smart credit. Over the next 2-3 days, I'll learn about your business, help you set clear goals, and understand how the right loan can accelerate your success.

What I need: Real photos, honest answers, and your business dreams! What you'll get: Instant business tips, personalized coaching, and potentially a loan designed for you to scale.

Ready to get started? Send me 2 photos of your business (inside and outside) and tell me your location! 📸📍"""
    
    def _route_message(self, message: str, current_task: LucyTask) -> str:
        """Route message to appropriate agent"""
        
        # Simple routing logic based on current task
        if current_task in [LucyTask.B1]:
            return "photo_verifier"
        elif current_task in [LucyTask.E4A, LucyTask.E4B, LucyTask.E6]:
            return "business_coach"  
        elif current_task in [LucyTask.B4, LucyTask.L3, LucyTask.L5, LucyTask.OFFER]:
            return "underwriter"
        else:
            return "business_coach"  # Default to business coach
    
    def _process_with_agent(self, agent: str, message: str, photos: List[str], state: LucyState) -> str:
        """Process message with the chosen agent"""
        
        # Route to appropriate specialized agent based on current task
        if agent == "photo_verifier":
            if photos or "photo" in message.lower():
                return self.photo_verifier.analyze_photos(photos or [], message)
            else:
                return self._get_photo_prompt()
        
        elif agent == "business_coach":
            return self.business_coach.build_rapport(state.customer_data, state.current_task, message)
        
        elif agent == "underwriter":
            if state.current_task == LucyTask.B4:
                # Check if we have sales data to analyze
                if state.customer_data.daily_sales > 0:
                    return self.underwriter.analyze_financials(state.customer_data)
                else:
                    return self._get_sales_prompt()
            elif state.current_task == LucyTask.L3:
                return self._get_loan_use_prompt()
            elif state.current_task == LucyTask.L5:
                return self._get_readiness_prompt(state.customer_data)
            elif state.current_task == LucyTask.OFFER:
                # Check if they're responding to the offer
                if any(word in message.lower() for word in ["yes", "accept", "agree", "take"]):
                    return self._get_acceptance_response(True)
                elif any(word in message.lower() for word in ["no", "reject", "decline"]):
                    return self._get_acceptance_response(False)
                else:
                    return self.underwriter.generate_loan_offer(state.customer_data)
            else:
                return "Let me gather some more information to help you better."
        
        else:
            return self._get_fallback_response(state.current_task)
    
    def _get_photo_prompt(self) -> str:
        """Prompt for photos when none provided"""
        return """Perfect! To get started, I'll need to see your business. 📸

Please share 2 photos of your shop:
1️⃣ **Inside view** - showing your products/stock
2️⃣ **Outside view** - showing your shop front

And let me know your **exact location** (market name, lane/section, area).

*Tip: If you can't share actual photos right now, you can describe your shop to me and we'll continue!*"""
    
    def _get_sales_prompt(self) -> str:
        """Prompt for sales data"""
        return """Great! Now I need to understand your business performance. 📊

Can you share with me:
- How many customers do you serve **per day** on average?
- What's your typical **daily sales** amount in KES?

For example: "I serve about 20 customers and make around 2,500 KES daily"

This helps me understand your cash flow and suggest the right loan amount! 💰"""
    
    def _get_loan_use_prompt(self) -> str:
        """Prompt for loan usage"""
        return """Perfect! Now, what would you use the loan for? 🎯

Some common uses:
• **Stock/Inventory** - Buy more products to sell
• **Equipment** - New tools or appliances for your business  
• **Expansion** - Grow your business or add new products
• **Working Capital** - Cover daily expenses while you grow

What's your main goal with this loan? This helps me structure the perfect amount and terms for you! 🚀"""
    
    def _get_readiness_prompt(self, customer_data: CustomerData) -> str:
        """Confirm readiness for loan offer"""
        return f"""Excellent! Let me summarize what we've discussed:

✅ **Your Business**: {customer_data.business_type} at {customer_data.location}
✅ **What You Love**: {customer_data.what_they_love}
✅ **Daily Performance**: ~{customer_data.daily_customers} customers, {customer_data.daily_sales:,} KES daily
✅ **Challenge**: {customer_data.challenge}
✅ **Loan Purpose**: {', '.join(customer_data.loan_uses)}

I'm ready to create your personalized loan offer! Are you ready to see what I can offer you? 

Just say **"Yes, I'm ready!"** and I'll generate your loan terms. 🎉"""
    
    def _get_fallback_response(self, current_task: LucyTask) -> str:
        """Fallback response based on current task"""
        task_prompts = {
            LucyTask.B1: "I'd love to see your business! Please share 2 photos and your location.",
            LucyTask.E4A: "Tell me about your business - what type do you run?",
            LucyTask.E4B: "What do you love most about your business?",
            LucyTask.B4: "What are your daily sales numbers?",
            LucyTask.E6: "What's your biggest business challenge right now?",
            LucyTask.L3: "What would you use the loan for?",
            LucyTask.L5: "Are you ready to see your loan offer?",
            LucyTask.OFFER: "Here's your loan offer!"
        }
        
        return task_prompts.get(current_task, "I'm here to help with your business loan! Tell me more about what you need.")
    
    def _get_acceptance_response(self, accepted: bool) -> str:
        """Response when customer accepts or rejects loan offer"""
        
        if accepted:
            return """🎉 **Fantastic! Congratulations on taking this big step for your business!** 

Your loan has been **APPROVED** and the disbursement process is starting now. Here's what happens next:

✅ **Loan Status:** Approved & Processing  
✅ **Disbursement:** Funds will be sent to your registered mobile money account  
✅ **Timeline:** You should receive the money within the next few hours  
✅ **SMS Confirmation:** You'll get a text message once the funds are sent  

**What you can do now:**
🏪 Start planning how to use the funds for your business growth  
📱 Keep your phone nearby for the disbursement confirmation  
📊 Begin tracking how the loan helps increase your sales  

**Need help?** I'm always here if you have questions about managing your loan or growing your business!

**Welcome to the Tala family - let's grow your business together!** 🚀💰"""
        else:
            return """I understand! Taking a loan is a big decision and it's completely okay to think it through more.

**No pressure at all!** Here's what you can do:

💡 **Take some time** - Think about your business needs and goals  
📊 **Track your sales** - Monitor your daily income for a few more days  
🤝 **I'm still here** - Come back anytime you want to discuss options  

**Would you like:**
1️⃣ Some business tips to help grow your current sales?  
2️⃣ Help setting up a simple sales tracking system?  
3️⃣ Just chat about your business goals?

I'm your business partner whether you take a loan or not! What would be most helpful for you right now? 😊"""
    
    def _update_state(self, response: str, message: str, photos: List[str], state: LucyState):
        """Update state based on the interaction"""
        
        # Comprehensive state updates for seamless flow
        if state.current_task == LucyTask.B1:
            # Extract location from any message
            if message and len(message.strip()) > 0:
                potential_location = self._extract_location(message)
                if potential_location:
                    state.customer_data.location = potential_location
            
            # Only complete B1 if we have both photos AND location
            if photos and len(photos) > 0:
                state.customer_data.photos = photos
                if state.customer_data.location:  # Only advance if we have location too
                    state.complete_task(LucyTask.B1)
                    state.current_task = LucyTask.E4A
        
        elif state.current_task == LucyTask.E4A:
            if any(word in message.lower() for word in ["business", "shop", "sell", "kiosk", "market"]):
                state.customer_data.business_type = self._extract_business_type(message)
                state.complete_task(LucyTask.E4A)
                state.current_task = LucyTask.E4B
        
        elif state.current_task == LucyTask.E4B:
            if any(word in message.lower() for word in ["love", "enjoy", "like", "passion"]):
                state.customer_data.what_they_love = message
                state.complete_task(LucyTask.E4B)
                state.current_task = LucyTask.B4
        
        elif state.current_task == LucyTask.B4:
            sales_data = self._extract_sales_data(message)
            if sales_data:
                state.customer_data.daily_customers = sales_data.get('customers', 0)
                state.customer_data.daily_sales = sales_data.get('sales', 0)
                state.customer_data.weekly_sales = sales_data.get('weekly_sales', 0)
                state.customer_data.expenses = sales_data.get('expenses', '')
                state.complete_task(LucyTask.B4)
                state.current_task = LucyTask.E6
        
        elif state.current_task == LucyTask.E6:
            # More flexible challenge detection
            if (any(word in message.lower() for word in ["challenge", "problem", "difficult", "struggle", "need", "want", "lack", "require"]) 
                or "loan" in message.lower() or len(message.split()) >= 2):
                state.customer_data.challenge = message if len(message) > 10 else "Need capital for business growth"
                state.complete_task(LucyTask.E6)
                state.current_task = LucyTask.L3
        
        elif state.current_task == LucyTask.L3:
            loan_uses = self._extract_loan_uses(message)
            if loan_uses:
                state.customer_data.loan_uses = loan_uses
                state.complete_task(LucyTask.L3)
                state.current_task = LucyTask.L5
        
        elif state.current_task == LucyTask.L5:
            if any(word in message.lower() for word in ["yes", "ready", "confirm", "proceed"]):
                state.complete_task(LucyTask.L5)
                state.current_task = LucyTask.OFFER
        
        elif state.current_task == LucyTask.OFFER:
            if any(word in message.lower() for word in ["yes", "accept", "agree", "take"]):
                # Customer accepted the loan offer
                self._handle_loan_acceptance(state.customer_data, True)
                state.complete_task(LucyTask.OFFER)
            elif any(word in message.lower() for word in ["no", "reject", "decline"]):
                # Customer rejected the loan offer  
                self._handle_loan_acceptance(state.customer_data, False)
    
    def _extract_location(self, message: str) -> str:
        """Extract location from customer message"""
        # More flexible location detection
        message_lower = message.lower()
        
        # Common location indicators
        location_indicators = ["market", "lane", "street", "road", "avenue", "in", "at", "near", "area", "estate", "mall"]
        
        # If it contains location indicators, return the whole message
        if any(indicator in message_lower for indicator in location_indicators):
            return message.strip()
        
        # If it's a reasonably short message (likely a place name), accept it
        if len(message.split()) <= 4 and len(message.strip()) > 2:
            return message.strip()
        
        return ""
    
    def _extract_business_type(self, message: str) -> str:
        """Extract business type from message"""
        business_types = ["shop", "kiosk", "restaurant", "salon", "grocery", "boutique", "hardware"]
        for business in business_types:
            if business in message.lower():
                return business
        return message
    
    def _extract_sales_data(self, message: str) -> Dict[str, Any]:
        """Extract sales data from customer message"""
        import re
        
        # Look for numbers in the message
        numbers = re.findall(r'\d+', message)
        if not numbers:
            return {}
        
        # Handle different patterns
        message_lower = message.lower()
        
        # Pattern: "30 customers, 800 KES" or "30, 800"
        if len(numbers) >= 2:
            # First number is likely customers, second is sales
            customers = int(numbers[0])
            sales = int(numbers[1])
            
            # If second number is very small, might be in thousands
            if sales < 100 and sales > 0:
                sales = sales * 1000  # Convert 8 to 8000
                
            return {
                'customers': customers,
                'sales': sales,
                'weekly_sales': sales * 7
            }
        elif len(numbers) == 1:
            # Single number - determine if it's customers or sales based on context
            num = int(numbers[0])
            if 'customer' in message_lower:
                return {
                    'customers': num,
                    'sales': 0  # Will need to ask for sales
                }
            elif 'kes' in message_lower or 'shilling' in message_lower or num > 50:
                # Likely sales amount
                if num < 100:
                    num = num * 1000  # Convert 8 to 8000
                return {
                    'customers': 20,  # Default assumption
                    'sales': num
                }
        return {}
    
    def _extract_loan_uses(self, message: str) -> List[str]:
        """Extract loan use cases from message"""
        uses = []
        loan_keywords = {
            "stock": "Purchase inventory/stock",
            "inventory": "Purchase inventory/stock", 
            "expand": "Business expansion",
            "equipment": "Buy equipment",
            "rent": "Pay rent",
            "supplies": "Buy supplies",
            "meat": "Add new product lines",
            "products": "Expand product range",
            "grow": "Business growth",
            "capital": "Working capital",
            "money": "Working capital"
        }
        
        message_lower = message.lower()
        for keyword, use in loan_keywords.items():
            if keyword in message_lower:
                uses.append(use)
        
        # If no specific use found but it's a loan-related message
        if not uses and ("loan" in message_lower or len(message) > 3):
            uses = ["Business expansion and growth"]
        
        return uses if uses else ["General business needs"]
    
    def _handle_loan_acceptance(self, customer_data: CustomerData, accepted: bool):
        """Handle loan acceptance or rejection"""
        
        # Calculate loan parameters
        monthly_gross = customer_data.daily_sales * 26 if customer_data.daily_sales else 20000
        monthly_net = monthly_gross * 0.6
        base_amount = max(10000, int(monthly_net * 0.2))
        loan_amount = min(50000, base_amount)
        loan_amount = round(loan_amount / 500) * 500
        
        # Store customer acceptance
        self.store_customer_acceptance(
            loanAmount=loan_amount,
            tenure=30,  # days converted to months would be 1
            repaymentFrequency="One-time",  # Matches the 30-day term
            accepted=accepted,
            interestRate=0.006,  # 0.6% daily
            loanType="SHORT_TERM"
        )
    
    def store_customer_acceptance(self, loanAmount: int, tenure: int, repaymentFrequency: str, 
                                 accepted: bool, interestRate: float, loanType: str) -> dict:
        """Simulate the store_customer_acceptance function call"""
        # In real implementation, this would call the actual function and trigger disbursement
        return {
            "loan_amount": loanAmount,
            "tenure": tenure,
            "repayment_frequency": repaymentFrequency,
            "accepted": accepted,
            "interest_rate": interestRate,
            "loan_type": loanType,
            "status": "disbursement_initiated" if accepted else "offer_declined",
            "timestamp": datetime.now().isoformat()
        }


# Example usage
if __name__ == "__main__":
    # Initialize Lucy
    lucy = LucyAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    # Simulate customer conversation
    state = None
    
    # Customer starts conversation
    response, state = lucy.chat("Hi, I need a loan for my shop")
    print("Lucy:", response)
    
    # Customer provides photos and location
    response, state = lucy.chat("Kawangware Market, Lane 3", photos=["shop1.jpg", "shop2.jpg"])
    print("Lucy:", response)