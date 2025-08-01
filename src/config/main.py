"""
Main entry point for Lucy Multi-Agent Crew
"""

def run_lucy_crew(user_input):
    """Run Lucy's crew with the given input"""
    try:
        # Import from the expected location
        from src.config.config.crew import create_lucy_crew
        result = create_lucy_crew(customer_message=user_input)
        return result
    except Exception as e:
        return f"Error running Lucy crew: {str(e)}"

if __name__ == "__main__":
    # Test the crew
    test_input = "Hi, I need a loan for my small shop in Nairobi"
    result = run_lucy_crew(test_input)
    print("Lucy's Response:")
    print(result)
