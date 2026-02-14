"""
My First Agent Task - Complete Working Example

This script demonstrates how to use the agentic framework.
It shows:
  1. Creating agents (PM and Dev)
  2. Creating tasks
  3. Creating a crew
  4. Executing coordinated work

Run with:
  python my_first_task.py

This is the same example from FIRST_TIME_USER_GUIDE.md Part 4
"""

from crewai import Crew, Task
from agents.pm_agent import create_pm_agent
from agents.dev_agent import create_dev_agent
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main execution function"""
    
    # Step 1: Create agents
    print("\n" + "="*70)
    print("STEP 1: Creating agents...")
    print("="*70)
    
    pm_agent = create_pm_agent(allow_delegation=True)
    dev_agent = create_dev_agent(allow_delegation=False)
    
    print("✓ PM Agent created")
    print("✓ Dev Agent created")
    
    # Step 2: Create tasks
    print("\n" + "="*70)
    print("STEP 2: Creating tasks...")
    print("="*70)
    
    planning_task = Task(
        description=(
            "Review the current agentic-infrastructure-framework project structure. "
            "Identify what we currently have (agents, skills, documentation). "
            "Assess what's working well, and identify any obvious gaps or improvements needed. "
            "Create a brief analysis with findings and top 3 recommendations."
        ),
        agent=pm_agent,
        expected_output=(
            "A project status analysis document with: "
            "(1) What we have, (2) What's working, (3) Top 3 suggested improvements"
        )
    )
    
    implementation_task = Task(
        description=(
            "Based on the PM's analysis, write a simple Python script that demonstrates "
            "using the framework's features. The script should: "
            "(1) Use logging skill to trace execution, "
            "(2) Handle errors gracefully, "
            "(3) Show best practices. "
            "Output the script code and explain what it does."
        ),
        agent=dev_agent,
        expected_output=(
            "Working Python code that demonstrates framework usage, "
            "with explanation of what it does and why"
        )
    )
    
    print("✓ Planning task created")
    print("✓ Implementation task created")
    
    # Step 3: Create crew (coordinate agents)
    print("\n" + "="*70)
    print("STEP 3: Setting up crew...")
    print("="*70)
    
    crew = Crew(
        agents=[pm_agent, dev_agent],
        tasks=[planning_task, implementation_task],
        manager_agent=pm_agent,  # PM coordinates the work
        verbose=True,            # Show all agent thinking
    )
    
    print("✓ Crew created with PM as manager")
    print("✓ Ready to execute!")
    
    # Step 4: Execute!
    print("\n" + "="*70)
    print("STEP 4: EXECUTING CREW - Watch the agents work!")
    print("="*70 + "\n")
    
    try:
        result = crew.kickoff()
        
        print("\n" + "="*70)
        print("✓ EXECUTION COMPLETE!")
        print("="*70)
        print(f"\nFinal Result:\n{result}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        print(f"\n✗ Error occurred: {e}")
        print("\nTroubleshooting tips:")
        print("  1. Check logs/agent_log.txt for detailed information")
        print("  2. Verify .env has OPENAI_API_KEY set")
        print("  3. Check that all dependencies are installed: pip install -r requirements.txt")
        print("  4. Ensure you're using the activated virtual environment")
        return False


def post_execution_check():
    """Check results after execution"""
    print("\n" + "="*70)
    print("STEP 5: Verifying execution...")
    print("="*70)
    
    try:
        from skills.logging_skill import read_log
        
        print("\nRecent activity from logs/agent_log.txt:")
        print("-" * 70)
        recent_logs = read_log(15)  # Get last 15 lines
        print(recent_logs)
        print("-" * 70)
        print("✓ Logs verified")
        
    except Exception as e:
        logger.warning(f"Could not read logs: {e}")


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║        MY FIRST AGENT TASK - Agentic Framework Example            ║
║                                                                    ║
║  This script demonstrates how agents, skills, and tasks work      ║
║  together in the agentic-infrastructure-framework.                ║
║                                                                    ║
║  The PM Agent will plan the work, then the Dev Agent will         ║
║  implement the solution. Everything is coordinated by CrewAI.     ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    # Run the main execution
    success = main()
    
    # Check results
    if success:
        post_execution_check()
        
        print("\n" + "="*70)
        print("SUCCESS! 🎉")
        print("="*70)
        print("\nNext steps:")
        print("  1. Review logs/agent_log.txt to see what happened")
        print("  2. Read FIRST_TIME_USER_GUIDE.md to learn more")
        print("  3. Create your own custom agent using templates/AGENT_TEMPLATE.md")
        print("  4. Create your own custom skill using templates/SKILL_TEMPLATE.md")
        print("\nKey files to explore:")
        print("  • agents/pm_agent.py - PM Agent implementation")
        print("  • agents/dev_agent.py - Dev Agent implementation")
        print("  • skills/ directory - All available skills")
        print("  • FIRST_TIME_USER_GUIDE.md - Comprehensive tutorial")
        
    else:
        print("\n" + "="*70)
        print("FAILED - Check errors above")
        print("="*70)
        print("\nDebug steps:")
        print("  1. Check logs/agent_log.txt")
        print("  2. Verify .env configuration: cat .env")
        print("  3. Test imports: python -c 'import crewai; print(crewai.__version__)'")
        print("  4. Check API keys are valid")
