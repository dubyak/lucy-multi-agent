"""
Main entry point for Lucy Multi-Agent Crew
"""

from .crew import create_lucy_crew

def run_lucy_crew(user_input):
    """Run Lucy's crew with the given input"""
    crew = create_lucy_crew()
    if crew is None:
        return "Error: Could not create Lucy crew"
    
    try:
        result = crew.kickoff(inputs={"customer_message": user_input})
        return result
    except Exception as e:
        return f"Error running Lucy crew: {str(e)}"

if __name__ == "__main__":
    # Test the crew
    test_input = "Hi, I need a loan for my small shop in Nairobi"
    result = run_lucy_crew(test_input)
    print("Lucy's Response:")
    print(result) 