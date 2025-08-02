"""
Main entry point for Lucy Multi-Agent Crew
"""

def main(user_input=""):
    """Main function for CrewAI Cloud deployment"""
    try:
        from .crew import create_lucy_crew
        result = create_lucy_crew(customer_message=user_input)
        return result
    except Exception as e:
        return f"Error running Lucy crew: {str(e)}"

def run_lucy_crew(user_input):
    """Run Lucy's crew with the given input"""
    return main(user_input)

if __name__ == "__main__":
    # Test the crew
    test_input = "Hi, I need a loan for my small shop in Nairobi"
    result = main(test_input)
    print("Lucy's Response:")
    print(result)
