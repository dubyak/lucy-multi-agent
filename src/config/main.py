"""
Main entry point for Lucy Multi-Agent Crew
"""

def run_lucy_crew(user_input):
    """Run Lucy's crew with the given input"""
    try:
        # Try to import and run the full crew
        from src.config.crew import create_lucy_crew
        crew = create_lucy_crew(customer_message=user_input)
        if crew is None:
            return "Error: Could not create Lucy crew"
        
        # Execute the crew with the user input
        result = crew.kickoff()
        return result
    except ImportError as e:
        # Fallback for testing without full dependencies
        return f"""Lucy Crew Test Mode: Received input: '{user_input}'. 

Full crew would process this through:
1. **PhotoVerifier** - Analyze business photos for verification
2. **BusinessCoach** - Help set business goals and loan purposes  
3. **Underwriter** - Assess risk and generate loan offer

(Import error: {e})"""
    except Exception as e:
        return f"Error running Lucy crew: {str(e)}"

if __name__ == "__main__":
    # Test the crew
    test_input = "Hi, I need a loan for my small shop in Nairobi"
    result = run_lucy_crew(test_input)
    print("Lucy's Response:")
    print(result)
