"""
Example agent for demonstrating the framework
"""

from src.agents import create_agent
from src.config import load_config
from src.utils import setup_logging, get_timestamp


def main():
    """Example main function"""
    # Setup
    config = load_config()
    logger = setup_logging(config.logging.log_level)

    logger.info(f"Starting Agentic Framework Example - {get_timestamp()}")
    logger.info(f"Environment: {config.project.environment}")

    # Create a sample agent
    researcher = create_agent(
        name="Research Agent",
        role="Research Specialist",
        goal="Conduct thorough research on given topics",
        backstory="""You are an expert researcher with years of experience 
        in gathering and synthesizing information from multiple sources.""",
        verbose=True,
    )

    logger.info(f"Created agent: {researcher.role}")
    logger.info("Agent ready for task execution")

    return researcher


if __name__ == "__main__":
    agent = main()
