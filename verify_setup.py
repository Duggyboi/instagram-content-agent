#!/usr/bin/env python
"""
Streamlit MVP Setup Verification
Checks that all dependencies and configurations are in place
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_python_version():
    """Check Python version."""
    print("✓ Checking Python version...")
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"  Python {version}")
    if sys.version_info >= (3, 8):
        print("  ✓ Version OK (3.8+)")
        return True
    else:
        print("  ✗ Version too old (need 3.8+)")
        return False

def check_package(package_name):
    """Check if a package is installed."""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def check_dependencies():
    """Check all required dependencies."""
    print("✓ Checking dependencies...")
    
    required_packages = {
        "streamlit": "Web UI framework",
        "crewai": "Agent framework",
        "langchain": "LLM integration",
        "pydantic": "Data validation",
        "requests": "HTTP requests",
        "python_dotenv": "Environment variables",
        "cv2": "OpenCV (video processing)",
        "pandas": "Data frames",
    }
    
    missing = []
    for package, description in required_packages.items():
        if check_package(package):
            print(f"  ✓ {package:20} - {description}")
        else:
            print(f"  ✗ {package:20} - MISSING")
            missing.append(package)
    
    return len(missing) == 0, missing

def check_directory_structure():
    """Check that required directories exist."""
    print("✓ Checking directory structure...")
    
    required_dirs = [
        "src",
        "src/agents",
        "src/config",
        "src/skills",
        "src/tools",
        "src/utils",
        "src/analysis",
        ".streamlit",
    ]
    
    missing = []
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ - MISSING")
            missing.append(dir_name)
    
    return len(missing) == 0, missing

def check_files():
    """Check that key files exist."""
    print("✓ Checking required files...")
    
    required_files = [
        "streamlit_app.py",
        "requirements.txt",
        ".streamlit/config.toml",
        "src/analysis/pipeline.py",
        "src/config/app_config.py",
        "src/utils/streamlit_utils.py",
        "run_streamlit.bat",
        ".env.example",
    ]
    
    missing = []
    for file_name in required_files:
        file_path = Path(file_name)
        if file_path.exists():
            print(f"  ✓ {file_name}")
        else:
            print(f"  ✗ {file_name} - MISSING")
            missing.append(file_name)
    
    return len(missing) == 0, missing

def check_imports():
    """Test that main imports work."""
    print("✓ Checking imports...")
    
    try:
        import streamlit as st
        print("  ✓ streamlit imported")
    except ImportError as e:
        print(f"  ✗ streamlit import failed: {e}")
        return False
    
    try:
        from src.analysis.pipeline import AnalysisPipeline
        print("  ✓ AnalysisPipeline imported")
    except ImportError as e:
        print(f"  ✗ AnalysisPipeline import failed: {e}")
        return False
    
    try:
        from src.config.app_config import AppConfig, get_config
        print("  ✓ AppConfig imported")
    except ImportError as e:
        print(f"  ✗ AppConfig import failed: {e}")
        return False
    
    try:
        from src.utils.streamlit_utils import export_results_as_markdown
        print("  ✓ streamlit_utils imported")
    except ImportError as e:
        print(f"  ✗ streamlit_utils import failed: {e}")
        return False
    
    return True

def check_environment_files():
    """Check environment configuration."""
    print("✓ Checking environment setup...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("  ✓ .env file found")
    else:
        print("  ~ .env file not found (using defaults)")
    
    if env_example.exists():
        print("  ✓ .env.example file found")
    else:
        print("  ~ .env.example file not found")
    
    return True

def print_summary(checks):
    """Print summary of all checks."""
    print_header("Verification Summary")
    
    all_passed = all(checks.values())
    
    for check_name, passed in checks.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:8} - {check_name}")
    
    print()
    
    if all_passed:
        print("✅ ALL CHECKS PASSED!")
        print("\nYou can now run the app with:")
        print("  streamlit run streamlit_app.py")
        return True
    else:
        print("❌ SOME CHECKS FAILED")
        print("\nPlease install missing dependencies:")
        print("  pip install -r requirements.txt")
        return False

def main():
    """Run all verification checks."""
    print_header("Streamlit MVP Setup Verification")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    checks = {}
    
    # Run checks
    checks["Python Version"] = check_python_version()
    
    deps_ok, missing_deps = check_dependencies()
    checks["Dependencies"] = deps_ok
    
    dirs_ok, missing_dirs = check_directory_structure()
    checks["Directory Structure"] = dirs_ok
    
    files_ok, missing_files = check_files()
    checks["Required Files"] = files_ok
    
    checks["Imports"] = check_imports()
    
    checks["Environment"] = check_environment_files()
    
    # Print summary
    success = print_summary(checks)
    
    print(f"\nVerification completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
