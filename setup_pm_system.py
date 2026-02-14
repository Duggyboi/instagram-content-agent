#!/usr/bin/env python3
"""
Setup script to install dependencies for the PM Initialization System

Run this script to install all required packages:
  python setup_pm_system.py
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and print status"""
    print(f"\n{'='*70}")
    print(f"📦 {description}")
    print(f"{'='*70}")
    print(f"Running: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ {description} - SUCCESS\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e}\n")
        return False

def main():
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║         PM INITIALIZATION SYSTEM - SETUP                           ║
║                                                                    ║
║     Installing dependencies for the PM Agent Framework            ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Upgrade pip
    print("Step 1: Upgrading pip to latest version...")
    run_command(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
        "Upgrade pip"
    )
    
    # Step 2: Install core dependencies
    print("Step 2: Installing core framework dependencies...")
    core_packages = [
        "crewai==0.11.2",
        "langchain>=0.1.0",
        "langchain-community>=0.0.30",
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "requests>=2.31.0",
    ]
    
    run_command(
        [sys.executable, "-m", "pip", "install"] + core_packages,
        "Install core dependencies"
    )
    
    # Step 3: Install development dependencies
    print("Step 3: Installing development dependencies...")
    dev_packages = [
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "black>=23.0.0",
        "flake8>=6.0.0",
        "mypy>=1.0.0",
    ]
    
    run_command(
        [sys.executable, "-m", "pip", "install"] + dev_packages,
        "Install development dependencies"
    )
    
    # Step 4: Verify installation
    print("Step 4: Verifying installation...")
    print(f"{'='*70}")
    print("Checking installed packages...")
    print(f"{'='*70}\n")
    
    try:
        import crewai
        print(f"✅ CrewAI {crewai.__version__ if hasattr(crewai, '__version__') else 'installed'}")
    except ImportError:
        print("❌ CrewAI - NOT FOUND")
    
    try:
        import langchain
        print(f"✅ LangChain installed")
    except ImportError:
        print("❌ LangChain - NOT FOUND")
    
    try:
        import openai
        print(f"✅ OpenAI installed")
    except ImportError:
        print("❌ OpenAI - NOT FOUND")
    
    try:
        import dotenv
        print(f"✅ python-dotenv installed")
    except ImportError:
        print("❌ python-dotenv - NOT FOUND")
    
    try:
        import pytest
        print(f"✅ pytest installed")
    except ImportError:
        print("❌ pytest - NOT FOUND")
    
    # Final instructions
    print(f"\n{'='*70}")
    print("✅ SETUP COMPLETE")
    print(f"{'='*70}\n")
    print("You can now run:")
    print("  python pm_init.py\n")
    print("Or read the quick start guide:")
    print("  cat PM_INIT_QUICKSTART.md\n")

if __name__ == "__main__":
    main()
