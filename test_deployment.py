#!/usr/bin/env python3
"""
Simple test script to validate the deployment structure
"""

import sys
import os

def test_imports():
    """Test basic imports without requiring all dependencies"""
    try:
        # Test that the config structure exists
        from src.config import main
        print("✅ src.config.main imported successfully")
        
        # Test that the crew module exists
        from src.config import crew
        print("✅ src.config.crew imported successfully")
        
        # Test that the config module exists
        from src.config import config
        print("✅ src.config.config imported successfully")
        
        print("✅ All basic imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_structure():
    """Test that the required files exist"""
    required_files = [
        "src/config/__init__.py",
        "src/config/main.py", 
        "src/config/crew.py",
        "src/config/config.py",
        "crewai.yaml",
        "pyproject.toml",
        "requirements.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path} exists")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files exist!")
        return True

if __name__ == "__main__":
    print("Testing deployment structure...")
    
    structure_ok = test_structure()
    imports_ok = test_imports()
    
    if structure_ok and imports_ok:
        print("\n🎉 Deployment structure validation passed!")
        sys.exit(0)
    else:
        print("\n❌ Deployment structure validation failed!")
        sys.exit(1) 