"""
Main entry point for Lucy Multi-Agent Crew
"""

def main(user_input=""):
    """Main function for CrewAI Cloud deployment"""
    try:
        # Import with absolute path for better compatibility
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from crew import create_lucy_crew
        result = create_lucy_crew(customer_message=user_input)
        return result
    except ImportError as e:
        return f"Import error: {str(e)} - Check if all dependencies are installed"
    except Exception as e:
        return f"Runtime error: {str(e)} - Check environment variables and configuration"

def run_lucy_crew(user_input):
    """Run Lucy's crew with the given input"""
    return main(user_input)

if __name__ == "__main__":
    # Test the crew
    test_input = "Hi, I need a loan for my small shop in Nairobi"
    result = main(test_input)
    print("Lucy's Response:")
    print(result)
