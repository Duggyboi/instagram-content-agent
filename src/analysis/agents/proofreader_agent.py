"""
Proofreader Agent - Quality validation using Ollama
Validates and refines analysis results before display
Phase 2: Premium Implementation
"""
from src.analysis.agents.base_agent import BaseAgent
from typing import Dict, Any, Optional
import logging
import requests
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class ProofreaderAgent(BaseAgent):
    """
    Validates and refines analysis results using Ollama local LLM.
    
    Acts as a quality gate, reviewing:
    - Transcription accuracy and completeness
    - Summary relevance and key point importance
    - Research findings reliability
    - Category accuracy and confidence
    
    Returns validation metadata and optional refinements.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Proofreader Agent.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.ollama_host = config.get("ollama_host", "http://localhost:11434") if config else "http://localhost:11434"
        self.model = config.get("ollama_model", "mistral") if config else "mistral"
        self.enable_refinement = config.get("enable_refinement", True) if config else True
        self._validate_ollama_connection()
    
    def _validate_ollama_connection(self) -> bool:
        """
        Check if Ollama is available and responding.
        
        Returns:
            True if Ollama is accessible, False otherwise
        """
        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=1)
            if response.status_code == 200:
                logger.info(f"Ollama connection established at {self.ollama_host}")
                return True
        except (requests.RequestException, Exception) as e:
            logger.warning(f"Ollama not available at {self.ollama_host}: {e}")
        
        return False
    
    def proofread(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and optionally refine analysis results using Ollama.
        
        Args:
            results: Complete analysis results from pipeline
        
        Returns:
            Dictionary with validation metadata and optional refinements
        """
        validation_metadata = {
            "validated": True,
            "validation_timestamp": datetime.now().isoformat(),
            "model_used": self.model,
            "validation_results": {}
        }
        
        try:
            # Check Ollama availability
            if not self._validate_ollama_connection():
                logger.warning("Ollama not available - skipping proofreading")
                validation_metadata["validated"] = False
                validation_metadata["reason"] = "Ollama service unavailable"
                return validation_metadata
            
            # Validate each section
            transcription = results.get("transcription", "")
            if transcription:
                trans_validation = self._validate_transcription(transcription, results)
                validation_metadata["validation_results"]["transcription"] = trans_validation
            
            summary = results.get("summary", {})
            if summary:
                summary_validation = self._validate_summary(summary, transcription)
                validation_metadata["validation_results"]["summary"] = summary_validation
            
            research = results.get("research", {})
            if research:
                research_validation = self._validate_research(research, transcription)
                validation_metadata["validation_results"]["research"] = research_validation
            
            categorization = results.get("categorization", {})
            if categorization:
                category_validation = self._validate_categorization(categorization, transcription, research)
                validation_metadata["validation_results"]["categorization"] = category_validation
            
            # Store validation metadata
            return validation_metadata
        
        except Exception as e:
            logger.error(f"Proofreading failed: {e}")
            validation_metadata["validated"] = False
            validation_metadata["error"] = str(e)
            return validation_metadata
    
    def _validate_transcription(self, transcription: str, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate transcription quality.
        
        Args:
            transcription: Transcribed text
            results: Full results dict for context
        
        Returns:
            Validation metrics
        """
        try:
            char_count = len(transcription)
            word_count = len(transcription.split())
            
            # Check for reasonable length
            quality_score = 100
            issues = []
            
            if char_count < 100:
                quality_score -= 30
                issues.append("Very short transcription - may be incomplete")
            elif char_count > 50000:
                quality_score -= 10
                issues.append("Very long transcription - quality may degrade with length")
            
            # Check for common transcription artifacts
            filler_words = transcription.lower().count(" um ") + transcription.lower().count(" uh ")
            if filler_words > word_count * 0.05:  # More than 5% filler words
                quality_score -= 5
                issues.append(f"High filler word content ({filler_words} instances detected)")
            
            # Quality message from Ollama - only try if connection is available
            assessment = ""
            if self._validate_ollama_connection():
                prompt = f"""Analyze this transcription for quality issues. Be brief (1-2 sentences):

Transcription: {transcription[:500]}...

Issues to check:
- Accuracy of transcription (coherence)
- Missing major words or phrases
- Obvious errors

Provide a brief quality assessment:"""
                
                assessment = self._query_ollama(prompt)
            
            return {
                "quality_score": max(0, quality_score),
                "char_count": char_count,
                "word_count": word_count,
                "issues": issues,
                "ollama_assessment": assessment
            }
        
        except Exception as e:
            logger.error(f"Transcription validation failed: {e}")
            return {"quality_score": 0, "error": str(e)}
    
    def _validate_summary(self, summary: Dict[str, Any], transcription: str) -> Dict[str, Any]:
        """
        Validate summary quality and relevance.
        
        Args:
            summary: Summary results dict
            transcription: Original transcription for context
        
        Returns:
            Validation metrics
        """
        try:
            summary_text = summary.get("summary", "")
            key_takeaways = summary.get("key_takeaways", [])
            
            quality_score = 100
            issues = []
            
            # Check summary completeness
            if len(summary_text) < 50:
                quality_score -= 30
                issues.append("Summary too short - insufficient detail")
            
            # Check key takeaways
            if len(key_takeaways) == 0:
                quality_score -= 20
                issues.append("No key takeaways identified")
            elif len(key_takeaways) > 10:
                quality_score -= 10
                issues.append("Too many takeaways - may dilute importance")
            
            # Ask Ollama if summary captures main points - only if available
            assessment = ""
            if self._validate_ollama_connection():
                prompt = f"""Does this summary capture the main points and value of the content? Rate 1-10 and explain briefly (1 sentence):

Content snippet: {transcription[:300]}...

Summary: {summary_text[:300]}...

Key takeaways: {', '.join(key_takeaways[:3])}

Rate and brief explanation:"""
                assessment = self._query_ollama(prompt)
            
            return {
                "quality_score": max(0, quality_score),
                "takeaway_count": len(key_takeaways),
                "summary_length": len(summary_text),
                "issues": issues,
                "ollama_assessment": assessment
            }
        
        except Exception as e:
            logger.error(f"Summary validation failed: {e}")
            return {"quality_score": 0, "error": str(e)}
    
    def _validate_research(self, research: Dict[str, Any], transcription: str) -> Dict[str, Any]:
        """
        Validate research findings relevance.
        
        Args:
            research: Research results dict
            transcription: Original transcription for context
        
        Returns:
            Validation metrics
        """
        try:
            findings = research.get("findings", [])
            topics = research.get("topics_extracted", [])
            research_areas = research.get("research_areas", [])
            
            quality_score = 100
            issues = []
            
            # Check findings quantity
            if len(findings) == 0:
                quality_score -= 25
                issues.append("No findings identified")
            elif len(findings) > 15:
                quality_score -= 10
                issues.append("Too many findings - may be over-detailed")
            
            # Check research areas
            if len(research_areas) == 0:
                quality_score -= 15
                issues.append("No research domains identified")
            
            # Ask Ollama about research relevance - only if available
            assessment = ""
            if self._validate_ollama_connection():
                prompt = f"""Are these research findings relevant and valuable? Rate 1-10:

Content: {transcription[:300]}...

Research areas: {', '.join(research_areas)}

Key findings: {'; '.join(findings[:3])}

Rate and one-sentence explanation:"""
                assessment = self._query_ollama(prompt)
            
            return {
                "quality_score": max(0, quality_score),
                "findings_count": len(findings),
                "topics_count": len(topics),
                "research_areas": research_areas,
                "issues": issues,
                "ollama_assessment": assessment
            }
        
        except Exception as e:
            logger.error(f"Research validation failed: {e}")
            return {"quality_score": 0, "error": str(e)}
    
    def _validate_categorization(self, categorization: Dict[str, Any], transcription: str, research: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate category assignments.
        
        Args:
            categorization: Categorization results dict
            transcription: Original transcription
            research: Research results for context
        
        Returns:
            Validation metrics
        """
        try:
            categories = categorization.get("categories", [])
            primary_category = categorization.get("primary_category", "")
            tags = categorization.get("tags", [])
            
            quality_score = 100
            issues = []
            
            # Check if categories are identified
            if len(categories) == 0:
                quality_score -= 30
                issues.append("No categories identified")
            
            # Check if primary category is set and confident
            if not primary_category:
                quality_score -= 25
                issues.append("No primary category assigned")
            else:
                # Find primary category confidence
                primary_confidence = 0
                for cat in categories:
                    if cat.get("name") == primary_category:
                        primary_confidence = cat.get("confidence", 0)
                        break
                
                if primary_confidence < 30:
                    quality_score -= 20
                    issues.append(f"Low confidence in primary category ({primary_confidence}%)")
            
            # Ask Ollama if categorization makes sense - only if available
            assessment = ""
            if self._validate_ollama_connection():
                prompt = f"""Is this content categorized correctly? Rate accuracy 1-10:

Main topic: {transcription[:250]}...

Primary category: {primary_category}

Research areas: {', '.join(research.get('research_areas', []))}

One-sentence rating:"""
                assessment = self._query_ollama(prompt)
            
            return {
                "quality_score": max(0, quality_score),
                "category_count": len(categories),
                "primary_category": primary_category,
                "tag_count": len(tags),
                "issues": issues,
                "ollama_assessment": assessment
            }
        
        except Exception as e:
            logger.error(f"Categorization validation failed: {e}")
            return {"quality_score": 0, "error": str(e)}
    
    def _query_ollama(self, prompt: str) -> str:
        """
        Query Ollama for analysis.
        
        Args:
            prompt: The prompt to send to Ollama
        
        Returns:
            Response from Ollama model
        """
        try:
            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3  # Lower temperature for more consistent validation
                },
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                logger.warning(f"Ollama returned status {response.status_code}")
                return ""
        
        except requests.exceptions.Timeout:
            logger.warning("Ollama request timed out")
            return ""
        except Exception as e:
            logger.warning(f"Failed to query Ollama: {e}")
            return ""
    
    def execute(self, input_data: str) -> str:
        """
        Base execute method (not used in this agent).
        
        Args:
            input_data: Not used
        
        Returns:
            Not applicable
        """
        return "ProofreaderAgent uses proofread() method, not execute()"
