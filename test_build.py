#!/usr/bin/env python3
"""
Test script to verify the build process
"""

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import crewai
        print("✅ crewai imported successfully")
    except Exception as e:
        print(f"❌ crewai import failed: {e}")
        return False
    
    try:
        from langchain_openai import ChatOpenAI
        print("✅ langchain_openai imported successfully")
    except Exception as e:
        print(f"❌ langchain_openai import failed: {e}")
        return False
    
    try:
        from langchain_anthropic import ChatAnthropic
        print("✅ langchain_anthropic imported successfully")
    except Exception as e:
        print(f"❌ langchain_anthropic import failed: {e}")
        return False
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ langchain_google_genai imported successfully")
    except Exception as e:
        print(f"❌ langchain_google_genai import failed: {e}")
        return False
    
    return True

def test_crew():
    """Test that the crew can be created"""
    try:
        from src.config.main import run_lucy_crew
        result = run_lucy_crew("Test message")
        print("✅ Crew creation and execution successful")
        return True
    except Exception as e:
        print(f"❌ Crew test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing build compatibility...")
    imports_ok = test_imports()
    crew_ok = test_crew()
    
    if imports_ok and crew_ok:
        print("🎉 All tests passed! Build should succeed.")
    else:
        print("❌ Some tests failed. Build may fail.")
