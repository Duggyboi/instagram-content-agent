"""
Framework Health Check Module

Validates that all framework dependencies and structure are in place.
Generates a checklist if anything is missing.
"""

import os
import sys
from pathlib import Path
from typing import Tuple, List, Dict
import importlib.util
import logging

logger = logging.getLogger(__name__)


class FrameworkHealthCheck:
    """Validate framework setup and dependencies"""
    
    def __init__(self, framework_root: str = "."):
        self.framework_root = Path(framework_root)
        self.issues = []
        self.warnings = []
        self.checks_passed = 0
        self.checks_total = 0
    
    def run_all_checks(self) -> Tuple[bool, str]:
        """
        Run all health checks.
        
        Returns:
            Tuple of (success: bool, report: str)
        """
        print("\n" + "="*70)
        print("FRAMEWORK HEALTH CHECK")
        print("="*70 + "\n")
        
        # Run checks in order
        self._check_python_version()
        self._check_directories()
        self._check_dependencies()
        self._check_env_file()
        self._check_git()
        
        # Generate report
        report = self._generate_report()
        
        # If issues, generate checklist
        if self.issues:
            self._generate_checklist()
            return False, report
        
        return True, report
    
    def _check_python_version(self):
        """Check Python 3.10+"""
        self.checks_total += 1
        version = sys.version_info
        if version.major >= 3 and version.minor >= 10:
            print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
            self.checks_passed += 1
        else:
            self.issues.append(f"Python 3.10+ required (have {version.major}.{version.minor})")
            print(f"✗ Python {version.major}.{version.minor} (need 3.10+)")
    
    def _check_directories(self):
        """Check required directories exist"""
        required_dirs = [
            "agents",
            "skills", 
            "templates",
            "logs",
            "src",
            "tests",
            "docs",
        ]
        
        for dirname in required_dirs:
            self.checks_total += 1
            dirpath = self.framework_root / dirname
            if dirpath.exists():
                print(f"✓ {dirname}/ exists")
                self.checks_passed += 1
            else:
                self.issues.append(f"Missing directory: {dirname}/")
                print(f"✗ {dirname}/ missing")
    
    def _check_dependencies(self):
        """Check Python package dependencies"""
        required_packages = [
            ("crewai", "CrewAI"),
            ("langchain", "LangChain"),
            ("pytest", "pytest"),
            ("black", "Black"),
            ("flake8", "Flake8"),
            ("dotenv", "python-dotenv"),
        ]
        
        for package_name, display_name in required_packages:
            self.checks_total += 1
            if self._is_package_installed(package_name):
                print(f"✓ {display_name} installed")
                self.checks_passed += 1
            else:
                self.issues.append(f"Missing package: {display_name}")
                print(f"✗ {display_name} not installed")
    
    def _check_env_file(self):
        """Check .env file exists and has critical keys"""
        self.checks_total += 1
        env_path = self.framework_root / ".env"
        
        if env_path.exists():
            print(f"✓ .env file exists")
            self.checks_passed += 1
            
            # Check for at least one API key
            self.checks_total += 1
            with open(env_path, 'r') as f:
                content = f.read()
            
            if "API_KEY" in content or "LLM" in content:
                print(f"✓ API credentials configured")
                self.checks_passed += 1
            else:
                self.warnings.append("No API keys found in .env (some features may not work)")
                print(f"⚠ No API keys found in .env")
        else:
            self.issues.append(".env file not found (copy from .env.example)")
            print(f"✗ .env file not found")
    
    def _check_git(self):
        """Check git repository is initialized"""
        self.checks_total += 1
        git_dir = self.framework_root / ".git"
        
        if git_dir.exists():
            print(f"✓ Git repository initialized")
            self.checks_passed += 1
        else:
            self.warnings.append("Git repository not initialized (run: git init)")
            print(f"⚠ Git repository not initialized")
    
    def _is_package_installed(self, package_name: str) -> bool:
        """Check if a Python package is installed"""
        spec = importlib.util.find_spec(package_name)
        return spec is not None
    
    def _generate_report(self) -> str:
        """Generate health check report"""
        total = self.checks_total
        passed = self.checks_passed
        failed = total - passed
        
        report = f"\n{'='*70}\n"
        report += f"HEALTH CHECK RESULT: {passed}/{total} checks passed\n"
        report += f"{'='*70}\n"
        
        if self.issues:
            report += f"\n❌ ISSUES FOUND ({len(self.issues)}):\n"
            for issue in self.issues:
                report += f"  - {issue}\n"
        
        if self.warnings:
            report += f"\n⚠️  WARNINGS ({len(self.warnings)}):\n"
            for warning in self.warnings:
                report += f"  - {warning}\n"
        
        if not self.issues and not self.warnings:
            report += "\n✅ All checks passed! Framework is ready.\n"
        
        report += f"\n{'='*70}\n"
        
        return report
    
    def _generate_checklist(self):
        """Generate a checklist file for missing items"""
        checklist_path = self.framework_root / ".framework" / "framework_checklist.md"
        
        checklist = "# Framework Setup Checklist\n\n"
        checklist += "Your framework is missing some components. Complete this checklist:\n\n"
        
        checklist += "## Required Items\n\n"
        for i, issue in enumerate(self.issues, 1):
            checklist += f"- [ ] {issue}\n"
        
        if self.warnings:
            checklist += "\n## Recommended Items\n\n"
            for i, warning in enumerate(self.warnings, 1):
                checklist += f"- [ ] {warning}\n"
        
        checklist += "\n## Installation Commands\n\n"
        checklist += "```bash\n"
        checklist += "# Install missing dependencies\n"
        checklist += "pip install -r requirements.txt\n"
        checklist += "\n# Setup environment\n"
        checklist += "cp .env.example .env\n"
        checklist += "# Edit .env and add your API keys\n"
        checklist += "\n# Initialize git (if needed)\n"
        checklist += "git init\n"
        checklist += "git add .\n"
        checklist += "git commit -m 'Initial commit'\n"
        checklist += "```\n"
        
        # Write checklist
        os.makedirs(checklist_path.parent, exist_ok=True)
        with open(checklist_path, 'w') as f:
            f.write(checklist)
        
        print(f"\n📋 Checklist generated: .framework/framework_checklist.md")
        print("Complete the checklist above to proceed.\n")


def run_health_check(framework_root: str = ".") -> Tuple[bool, str]:
    """
    Run framework health check.
    
    Args:
        framework_root: Path to framework root directory
        
    Returns:
        Tuple of (success: bool, report: str)
    """
    checker = FrameworkHealthCheck(framework_root)
    return checker.run_all_checks()


if __name__ == "__main__":
    success, report = run_health_check()
    print(report)
    
    if not success:
        sys.exit(1)
