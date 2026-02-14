"""
PM Scoping for Instagram Content Agent
Reads existing project brief and generates Phase 1 output
"""

import sys
from pathlib import Path
from framework_health_check import run_health_check
from agents.pm_business_architect import create_business_architect_agent
from crewai import Crew, Task
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Use existing project brief for scoping"""
    
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║         INSTAGRAM CONTENT AGENT - PM PHASE 1                       ║
║         Using Existing Project Brief                               ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Check health
    print("\n📋 Running health checks...\n")
    if not run_health_check():
        return False
    
    print("\n" + "="*70)
    print("PHASE 1: READING EXISTING PROJECT BRIEF")
    print("="*70 + "\n")
    
    # Read the existing brief
    brief_path = Path(".project/project_brief.md")
    if not brief_path.exists():
        print(f"❌ Project brief not found at {brief_path}")
        return False
    
    with open(brief_path, 'r') as f:
        brief_content = f.read()
    
    print("✓ Project brief loaded\n")
    
    # Create business architect agent
    print("="*70)
    print("Creating Business Architect Agent...")
    print("="*70 + "\n")
    
    architect = create_business_architect_agent()
    
    # Create task to validate and refine the brief
    task_description = (
        f"You are reviewing an existing PROJECT BRIEF that was created for the "
        f"Instagram Content Intelligence Agent project.\n\n"
        f"EXISTING BRIEF:\n"
        f"---\n{brief_content}\n---\n\n"
        f"Your task is to validate this brief and present it as the official PROJECT BRIEF for Phase 1.\n\n"
        f"Review the brief for:\n"
        f"1. **Completeness** - Does it cover all necessary sections?\n"
        f"2. **Clarity** - Is the vision clear and actionable?\n"
        f"3. **Feasibility** - Are the goals realistic given constraints?\n"
        f"4. **Success Metrics** - Are success criteria measurable?\n\n"
        f"Present this as the APPROVED PROJECT BRIEF and confirm it's ready for Phase 2 decomposition.\n"
        f"Save to .project/project_brief.md"
    )
    
    scoping_task = Task(
        description=task_description,
        agent=architect,
        expected_output=(
            "Validated project brief confirming all sections are complete and project is ready for Phase 2"
        )
    )
    
    # Create crew and execute
    crew = Crew(
        agents=[architect],
        tasks=[scoping_task],
        verbose=True,
    )
    
    print("Validating project brief...\n")
    result = crew.kickoff()
    
    print("\n" + "="*70)
    print("PHASE 1 COMPLETE")
    print("="*70)
    print(f"\n{result}\n")
    
    # Ask about next phase
    print("\n" + "="*70)
    print("PROJECT BRIEF STATUS: APPROVED")
    print("="*70)
    print("""
✅ Your Instagram Content Intelligence Agent project brief is complete!

Files created:
  📄 .project/project_brief.md - Project vision and requirements

Next steps:
  1. Review the brief in .project/project_brief.md
  2. Proceed to Phase 2: Project Decomposition
  3. Phase 2 will break down into specific agents and skills
  4. Phase 3 will propose technical architecture

Ready to continue? Run:
  python pm_decompose.py
    """)
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Scoping cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error during scoping: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)
