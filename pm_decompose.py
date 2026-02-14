"""
PM Decomposition Script

Phase 2: Project Decomposition

Reads the project brief and breaks it down into objectives, components, 
and milestones. User can review and adjust before moving to Phase 3.

Usage:
    python pm_decompose.py
"""

import sys
from pathlib import Path
from agents.pm_decomposer import create_decomposer_agent
from crewai import Crew, Task
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Phase 2: Project Decomposition"""
    
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║              PHASE 2: PROJECT DECOMPOSITION                        ║
║                                                                    ║
║  Breaking your project into objectives, components,               ║
║  and milestones...                                                ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Check if project brief exists
    brief_path = Path(".project/project_brief.md")
    if not brief_path.exists():
        print("❌ Project brief not found: .project/project_brief.md")
        print("\nPlease run 'python pm_init.py' first to create a project brief.")
        return False
    
    # Read the brief
    print("📖 Reading project brief...")
    with open(brief_path, 'r') as f:
        brief_content = f.read()
    
    print("✓ Brief loaded\n")
    
    # Create decomposer agent
    print("="*70)
    print("Creating Project Decomposer Agent...")
    print("="*70 + "\n")
    
    decomposer = create_decomposer_agent()
    
    # Create decomposition task
    task_description = (
        f"Read this project brief and create a detailed decomposition:\n\n"
        f"---\n{brief_content}\n---\n\n"
        f"Break it down into:\n"
        f"1. OBJECTIVES - The 3-5 core goals we're achieving\n"
        f"2. COMPONENTS - The major parts/phases of the solution\n"
        f"3. MILESTONES - Timeline with key deliverables and checkpoints\n\n"
        f"Consider:\n"
        f"- What must be done first (dependencies)?\n"
        f"- What are natural phases or iterations?\n"
        f"- Where are the risks?\n"
        f"- What's realistic given the timeline/constraints?\n\n"
        f"Present your decomposition and ask the user: "
        f"'Does this breakdown capture your project? Want to adjust anything?'\n"
        f"Wait for their approval.\n\n"
        f"Once approved, save the decomposition to: .project/project_decomposition.md"
    )
    
    decomposition_task = Task(
        description=task_description,
        agent=decomposer,
        expected_output=(
            "A detailed project decomposition saved to .project/project_decomposition.md "
            "containing objectives, components with timelines, and milestone checkpoints. "
            "User has reviewed and approved the decomposition."
        )
    )
    
    # Create crew and execute
    crew = Crew(
        agents=[decomposer],
        tasks=[decomposition_task],
        verbose=True,
    )
    
    print("Starting decomposition session...\n")
    result = crew.kickoff()
    
    print("\n" + "="*70)
    print("PROJECT DECOMPOSITION COMPLETE")
    print("="*70)
    print(f"\n{result}\n")
    
    # Ask if user wants to continue to Phase 3
    print("\n" + "="*70)
    print("What would you like to do next?")
    print("="*70)
    print("""
1. Continue to Phase 3 (Technical Solution Proposal)
2. Review and edit the decomposition first
3. Exit for now

Choice (1/2/3):
    """)
    
    next_choice = input("Your choice: ").strip()
    
    if next_choice == "1":
        print("\n✓ Proceeding to Phase 3...")
        print("\nTo continue with Phase 3 (Solution Architecture), run:")
        print("  python pm_architect.py")
        return True
    elif next_choice == "2":
        print("\n✓ Browse to .project/project_decomposition.md to review and edit.")
        print("\nWhen ready, run:")
        print("  python pm_architect.py")
        return True
    else:
        print("\n✓ Exiting. When ready to continue, run:")
        print("  python pm_architect.py")
        return True


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Decomposition cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error during decomposition: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)
