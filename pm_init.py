"""
PM Initialization Script

Main entry point for PM Agent initialization flow.
Runs health check, greets user, and starts Phase 1: Scoping.

Usage:
    python pm_init.py
"""

import sys
from pathlib import Path
from framework_health_check import run_health_check
import logging

# Try to import CrewAI components
try:
    from agents.pm_business_architect import create_business_architect_agent
    from crewai import Crew, Task
    CREWAI_AVAILABLE = True
except ImportError as e:
    CREWAI_AVAILABLE = False
    IMPORT_ERROR = str(e)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main PM initialization flow"""
    
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║            AGENTIC INFRASTRUCTURE FRAMEWORK                        ║
║            PM Agent Initialization                                 ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Check if CrewAI is available
    if not CREWAI_AVAILABLE:
        print("\n" + "="*70)
        print("❌ MISSING DEPENDENCY")
        print("="*70)
        print(f"\nError: {IMPORT_ERROR}")
        print("\nCrewAI is required but not installed.")
        print("\nTo fix this, run:")
        print("  pip install crewai langchain openai python-dotenv pydantic requests")
        print("\nOr install from requirements.txt:")
        print("  pip install -r requirements.txt")
        print("\n" + "="*70 + "\n")
        return False
    
    # Phase 0: Health Check
    print("\n📋 Running health checks...\n")
    success, report = run_health_check()
    print(report)
    
    if not success:
        print("\n❌ Framework health check failed.")
        print("Please complete the checklist in .framework/framework_checklist.md")
        print("Then run this script again.\n")
        return False
    
    # Health check passed - proceed to greeting
    print("\n" + "="*70)
    print("PHASE 1: PROJECT SCOPING")
    print("="*70)
    
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║  Welcome! I'm your Project Manager Agent.                         ║
║                                                                    ║
║  I'm ready to help you define your project scope, create a        ║
║  project brief, decompose it into objectives and milestones,      ║
║  and propose a technical solution to achieve your goals.          ║
║                                                                    ║
║  Let's start by understanding what you want to build.             ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Phase 1: Scoping with Business Architect
    print("\nPhase 1: Business Solution Architect Mode")
    print("-" * 70)
    print("""
I'll help you define your project. You can either:

  A) Describe your project idea (I'll ask follow-up questions)
  B) Paste an existing project brief (I'll refine it with questions)

Which approach would you prefer? (A or B)
    """)
    
    choice = input("Your choice (A/B): ").strip().upper()
    
    if choice not in ['A', 'B']:
        print("❌ Invalid choice. Please run again and select A or B")
        return False
    
    # ===== PHASE 1A: INTERACTIVE DISCOVERY =====
    print("\n" + "="*70)
    print("PHASE 1A: DISCOVERY QUESTIONNAIRE")
    print("="*70)
    print("Let's gather information about your project idea.\n")
    
    if choice == 'A':
        # Directly ask the user questions and collect answers
        print("📝 Answer these questions about your project:\n")
        
        problem = input("1️⃣  What problem are you solving? What's the pain point?\n   > ").strip()
        users = input("\n2️⃣  Who are the primary users / stakeholders?\n   > ").strip()
        outcome = input("\n3️⃣  What should be different after this project? What's success?\n   > ").strip()
        metrics = input("\n4️⃣  How will you know this succeeded? (What are measurable indicators?)\n   > ").strip()
        constraints = input("\n5️⃣  Any constraints? (timeline, budget, technical, team size)\n   > ").strip()
        context = input("\n6️⃣  Anything else we should know?\n   > ").strip()
        
        # Build discovery summary
        discovery_summary = f"""
PROJECT DISCOVERY SUMMARY
==========================

PROBLEM STATEMENT:
{problem}

TARGET USERS/STAKEHOLDERS:
{users}

DESIRED OUTCOME:
{outcome}

SUCCESS METRICS:
{metrics}

CONSTRAINTS & REQUIREMENTS:
{constraints if constraints else "(No constraints mentioned)"}

ADDITIONAL CONTEXT:
{context if context else "(No additional context)"}
        """
        
        print("\n" + "="*70)
        print("✓ Thank you! Now let me create your project brief...")
        print("="*70 + "\n")
        
    else:  # choice == 'B'
        print("Please paste your project brief (press Enter twice when done):\n")
        lines = []
        empty_count = 0
        while empty_count < 1:
            line = input()
            if line == "":
                empty_count += 1
            else:
                empty_count = 0
                lines.append(line)
        
        discovery_summary = "\n".join(lines)
    
    # ===== PHASE 1B: CREATE PROJECT BRIEF =====
    print("\n" + "="*70)
    print("PHASE 1B: CREATING PROJECT BRIEF")
    print("="*70 + "\n")
    
    # Create business architect agent
    architect = create_business_architect_agent()
    
    # Create task with the user's answers (no agent-generated conversation)
    task_description = (
        f"You are reviewing a project discovery summary and creating a professional PROJECT BRIEF.\n\n"
        f"DISCOVERY SUMMARY:\n"
        f"---\n{discovery_summary}\n---\n\n"
        f"Create a well-structured PROJECT BRIEF with these sections:\n"
        f"1. **Problem Statement** - The core problem being solved\n"
        f"2. **Target Users** - Who will benefit from this\n"
        f"3. **Desired Outcomes** - What success looks like\n"
        f"4. **Success Metrics** - Measurable indicators of success\n"
        f"5. **Scope & Features** - What's included and what's not\n"
        f"6. **Constraints** - Timeline, budget, technical, team constraints\n"
        f"7. **Dependencies** - What needs to be true for this to work\n"
        f"8. **Risks & Assumptions** - Key risks and mitigation strategies\n\n"
        f"Make the brief clear, concise, and actionable. Save it to .project/project_brief.md"
    )
    
    scoping_task = Task(
        description=task_description,
        agent=architect,
        expected_output=(
            "A professional project brief saved to .project/project_brief.md with all 8 sections"
        )
    )
    
    # Create crew and execute
    crew = Crew(
        agents=[architect],
        tasks=[scoping_task],
        verbose=True,
    )
    
    # Ensure .project directory exists
    project_dir = Path(".project")
    project_dir.mkdir(exist_ok=True)
    
    print("Creating project brief...\n")
    result = crew.kickoff()
    
    print("\n" + "="*70)
    print("PROJECT BRIEF CREATED")
    print("="*70)
    print(f"\n{result}\n")
    
    # Ask if user wants to continue to next phase
    print("\n" + "="*70)
    print("What would you like to do next?")
    print("="*70)
    print("""
1. Continue to Phase 2 (Project Decomposition)
2. Review and edit the brief first
3. Exit for now

Choice (1/2/3):
    """)
    
    next_choice = input("Your choice: ").strip()
    
    if next_choice == "1":
        print("\n✓ Proceeding to Phase 2...")
        print("\nTo continue with Phase 2 (Decomposition), run:")
        print("  python pm_decompose.py")
        return True
    elif next_choice == "2":
        print("\n✓ Browse to .project/project_brief.md to review and edit.")
        print("\nWhen ready, run:")
        print("  python pm_decompose.py")
        return True
    else:
        print("\n✓ Exiting. When ready to continue, run:")
        print("  python pm_decompose.py")
        return True


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Initialization cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error during initialization: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)
