"""
PM Solution Architecture Script

Phase 3: Technical Solution Proposal

Reads the project decomposition and proposes a technical solution including
tools, frameworks, agent architecture, and skills. Declares project ready.

Usage:
    python pm_architect.py
"""

import sys
from pathlib import Path
from agents.pm_solution_architect import create_solution_architect_agent
from crewai import Crew, Task
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Phase 3: Technical Solution Proposal"""
    
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║         PHASE 3: TECHNICAL SOLUTION PROPOSAL                       ║
║                                                                    ║
║  Designing the technical architecture for your project...          ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Check if decomposition exists
    decomp_path = Path(".project/project_decomposition.md")
    if not decomp_path.exists():
        print("❌ Project decomposition not found: .project/project_decomposition.md")
        print("\nPlease run 'python pm_decompose.py' first to create a decomposition.")
        return False
    
    # Check if brief exists too (for full context)
    brief_path = Path(".project/project_brief.md")
    brief_content = ""
    if brief_path.exists():
        with open(brief_path, 'r') as f:
            brief_content = f.read()
    
    # Read the decomposition
    print("📖 Reading project decomposition...")
    with open(decomp_path, 'r') as f:
        decomp_content = f.read()
    
    print("✓ Decomposition loaded\n")
    
    # Create solution architect agent
    print("="*70)
    print("Creating Solution Architect Agent...")
    print("="*70 + "\n")
    
    architect = create_solution_architect_agent()
    
    # Create architecture task
    context = f"Project Brief:\n---\n{brief_content}\n---\n\n" if brief_content else ""
    
    task_description = (
        f"{context}"
        f"Project Decomposition:\n"
        f"---\n{decomp_content}\n---\n\n"
        f"Design a technical solution for this project. Propose:\n"
        f"1. TECH STACK - Frameworks, languages, tools needed\n"
        f"2. AGENT ARCHITECTURE - What agents are needed? What do they do?\n"
        f"3. SKILLS - What capabilities does each agent need?\n"
        f"4. IMPLEMENTATION STRATEGY - How to build this in phases\n\n"
        f"Consider:\n"
        f"- How does CrewAI help us build this?\n"
        f"- What specialized agents (PM, Dev, QA, DevOps) do we need?\n"
        f"- What custom skills accelerate development?\n"
        f"- What's the critical path?\n"
        f"- How do we validate at each milestone?\n\n"
        f"Create a comprehensive TECHNICAL PROPOSAL document.\n"
        f"When done, declare the project ready for development:\n"
        f"'Your project is fully defined and ready for implementation!'\n\n"
        f"Save the proposal to: .project/technical_proposal.md"
    )
    
    architecture_task = Task(
        description=task_description,
        agent=architect,
        expected_output=(
            "A detailed technical proposal saved to .project/technical_proposal.md "
            "containing tech stack, agent architecture, required skills, and "
            "implementation strategy. Project is declared ready for development."
        )
    )
    
    # Create crew and execute
    crew = Crew(
        agents=[architect],
        tasks=[architecture_task],
        verbose=True,
    )
    
    print("Starting architecture design session...\n")
    result = crew.kickoff()
    
    print("\n" + "="*70)
    print("TECHNICAL PROPOSAL COMPLETE")
    print("="*70)
    print(f"\n{result}\n")
    
    # Show project status
    print("\n" + "="*70)
    print("PROJECT STATUS: READY FOR IMPLEMENTATION")
    print("="*70)
    print("""
✅ Your project is fully defined!

Files created:
  📄 .project/project_brief.md - Project vision and requirements
  📄 .project/project_decomposition.md - Objectives, components, milestones
  📄 .project/technical_proposal.md - Technical architecture and solutions

Next steps:
  1. Review all three documents
  2. Share with your team for feedback
  3. Create tasks for the Dev Agent to start implementation
  4. Monitor progress via PM Agent coordination

To start development, you can now:
  - Use the PM Agent to manage the project
  - Use the Dev Agent to implement components
  - Create custom agents for specialized needs
  - Track progress and iterate

Happy building! 🚀
    """)
    
    # Ask about new project creation
    print("\n" + "="*70)
    print("CREATE NEW PROJECT?")
    print("="*70)
    
    response = input("""
This was a planning session to scope your project. 

Are you ready to create an actual project directory for implementation?
(This follows the multi-project architecture model)

Options:
  Y - Yes, create a new project directory
  N - No, I'll do it manually later
  H - Help (show architecture info)

Your choice (Y/N/H): """).strip().upper()
    
    if response == 'H':
        print("""
MULTI-PROJECT ARCHITECTURE GUIDE:
══════════════════════════════════════════════════════════════════

Your projects should follow the template + promotion model:

1. FRAMEWORK (base template)
   📂 agentic-infrastructure-framework/
   - Pristine, well-tested general-purpose skills
   - Reusable across all projects
   - Changes only through promotion from projects

2. PROJECTS (independent clones)
   📂 my-project-name/
   - Clone of framework with project-specific customizations
   - Independent git repository
   - .project/ with scoping documents
   - project-specific skills and agents

3. TOOL SHARING
   - General tools → Promote to framework
   - Project-specific tools → Keep in project
   - Shared across projects → Create shared-tools package
   - (See MULTI_PROJECT_ARCHITECTURE.md for details)

For more details, see:
  📄 MULTI_PROJECT_ARCHITECTURE.md in the framework root

Would you like to create a project now? (Y/N): """)
        response = input("Your choice: ").strip().upper()
    
    if response == 'Y':
        project_name = input("""
Project Directory Name:
(Use lowercase with hyphens, e.g., 'my-awesome-project')
Name: """).strip()
        
        if not project_name:
            print("❌ Project name cannot be empty.")
            return True
        
        print(f"""
✅ Ready to create project: {project_name}

Next steps to set up your project:

1. INITIALIZE DIRECTORY:
   - Framework/project will clone the agentic-infrastructure-framework
   - All framework capabilities available
   
2. INITIALIZE GIT:
   - New git repository for {project_name}
   - Independent versioning from framework
   
3. PROJECT SETUP:
   - Copy this .project/ folder to your new project
   - Update .env for project-specific config
   - Create custom skills/ for project needs
   
4. VERSION TRACKING:
   - Add FRAMEWORK_VERSION to your project
   - Track which framework version you're based on
   - Easier promotion decisions later

📖 Full guide: MULTI_PROJECT_ARCHITECTURE.md
   
To proceed with creation, you can:
1. Manually copy the framework to {project_name}/
2. cd into {project_name}
3. Update .env and project configuration
4. Run: python pm_init.py (to replan for this project)

🚀 Your project structure is ready to be created!
        """)
    else:
        print("""
No problem! You can create your project directory at any time.

Remember to follow the multi-project architecture:
  📖 See MULTI_PROJECT_ARCHITECTURE.md for details
  
Quick reminder:
  1. Take a fresh copy of the framework
  2. Create a new git repository
  3. Update configuration for your project
  4. Start building!
        """)
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Architecture design cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error during architecture design: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)
