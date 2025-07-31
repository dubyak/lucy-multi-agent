"""
Main entry point for Lucy Multi-Agent Crew
"""

def run_lucy_crew(user_input):
    """Run Lucy's crew with the given input"""
    try:
        # Try to import and run the full crew
        from .crew import create_lucy_crew
        crew = create_lucy_crew()
        if crew is None:
            return "Error: Could not create Lucy crew"
        
        result = crew.kickoff(inputs={"customer_message": user_input})
        return result
    except ImportError as e:
        # Fallback for testing without full dependencies
        return f"Lucy Crew Test Mode: Received input: '{user_input}'. Full crew would process this with PhotoVerifier, BusinessCoach, and Underwriter agents. (Import error: {e})"
    except Exception as e:
        return f"Error running Lucy crew: {str(e)}"

if __name__ == "__main__":
    # Test the crew
    test_input = "Hi, I need a loan for my small shop in Nairobi"
    result = run_lucy_crew(test_input)
    print("Lucy's Response:")
    print(result) 