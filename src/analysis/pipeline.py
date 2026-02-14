"""
Analysis Pipeline
Core module for orchestrating the analysis workflow.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AnalysisPipeline:
    """Main pipeline for orchestrating video analysis."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the analysis pipeline.
        
        Args:
            config: Configuration dictionary with analysis settings
        """
        self.config = config
        self.results = {}
        self.temp_dir = Path("temp_uploads")
        self.results_dir = Path("results")
        self.results_dir.mkdir(exist_ok=True)
    
    def run(self, video_path: str) -> Dict[str, Any]:
        """
        Execute the complete analysis pipeline.
        
        Args:
            video_path: Path to the video file
        
        Returns:
            Dictionary containing all analysis results
        """
        self.results = {
            "file_name": Path(video_path).name,
            "timestamp": datetime.now().isoformat(),
            "config": self.config
        }
        
        try:
            steps = self.config.get("steps", {})
            
            if steps.get("transcription", True):
                self._run_transcription(video_path)
            
            if steps.get("summary", True):
                self._run_summary()
            
            if steps.get("research", True):
                self._run_research()
            
            if steps.get("categorization", True):
                self._run_categorization()
            
            if steps.get("proofreading", True):
                self._run_proofreading()
            
            if steps.get("impact", True):
                self._run_impact_analysis()
            
            # Save results
            self._save_results()
            
            return self.results
        
        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            raise
    
    def _run_transcription(self, video_path: str) -> None:
        """Extract transcription from video."""
        try:
            from src.analysis.agents import TranscriptionAgent
            
            agent = TranscriptionAgent(self.config)
            transcription = agent.transcribe(video_path)
            self.results["transcription"] = transcription
            logger.info("Transcription completed")
            
        except ImportError as e:
            logger.warning(f"TranscriptionAgent not found: {e}")
            self.results["transcription"] = "[Transcription would be extracted from video]"
    
    def _run_summary(self) -> None:
        """Generate summary from transcription."""
        try:
            from src.analysis.agents import SummaryAgent
            
            transcription = self.results.get("transcription", "")
            agent = SummaryAgent(self.config)
            summary = agent.summarize(transcription)
            self.results["summary"] = summary
            logger.info("Summary generation completed")
            
        except ImportError as e:
            logger.warning(f"SummaryAgent not found: {e}")
            self.results["summary"] = "[Summary would be generated from transcription]"
    
    def _run_research(self) -> None:
        """Conduct research based on video content."""
        try:
            from src.analysis.agents import ResearchAgent
            
            transcription = self.results.get("transcription", "")
            agent = ResearchAgent(self.config)
            research = agent.research(transcription)
            self.results["research"] = research
            logger.info("Research analysis completed")
            
        except ImportError as e:
            logger.warning(f"ResearchAgent not found: {e}")
            self.results["research"] = {
                "findings": ["Research findings would be discovered here"],
                "links": []
            }
    
    def _run_categorization(self) -> None:
        """Categorize video content with research and summary context."""
        try:
            from src.analysis.agents import CategorizationAgent
            
            transcription = self.results.get("transcription", "")
            research_results = self.results.get("research", {})
            summary_results = self.results.get("summary", {})
            
            agent = CategorizationAgent(self.config)
            categorization = agent.categorize(transcription, research_results, summary_results)
            self.results["categorization"] = categorization
            logger.info("Categorization completed with research and summary context")
            
        except ImportError as e:
            logger.warning(f"CategorizationAgent not found: {e}")
            self.results["categorization"] = {
                "primary": "Uncategorized",
                "confidence": 0,
                "tags": []
            }
    
    def _run_proofreading(self) -> None:
        """Validate and refine results using Ollama proofreader."""
        try:
            from src.analysis.agents import ProofreaderAgent
            
            agent = ProofreaderAgent(self.config)
            validation_metadata = agent.proofread(self.results)
            self.results["validation_metadata"] = validation_metadata
            logger.info("Proofreading validation completed")
            
        except ImportError as e:
            logger.warning(f"ProofreaderAgent not found: {e}")
            self.results["validation_metadata"] = {
                "validated": False,
                "reason": "ProofreaderAgent not available"
            }
        except Exception as e:
            logger.warning(f"Proofreading failed: {e}")
            self.results["validation_metadata"] = {
                "validated": False,
                "error": str(e)
            }
    
    def _run_impact_analysis(self) -> None:
        """Analyze project impact."""
        try:
            # Note: ImpactAgent not yet implemented - using placeholder
            transcription = self.results.get("transcription", "")
            categorization = self.results.get("categorization", {})
            # future: from src.analysis.agents import ImpactAgent
            self.results["impact"] = {
                "affected_projects": [],
                "actionable_insights": []
            }
            logger.info("Impact analysis skipped (agent not implemented)")
            
        except Exception as e:
            logger.warning(f"Impact analysis failed: {e}")
            self.results["impact"] = {
                "affected_projects": [],
                "actionable_insights": []
            }
    
    def _save_results(self) -> None:
        """Save results to disk."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.results_dir / f"analysis_{timestamp}.json"
            
            with open(filename, "w") as f:
                json.dump(self.results, f, indent=2)
            
            logger.info(f"Results saved to {filename}")
        
        except Exception as e:
            logger.error(f"Failed to save results: {e}")
