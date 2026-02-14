"""
Research Agent - Extract topics and generate intelligent research findings
Phase 2: Premium Implementation
"""
from src.analysis.agents.base_agent import BaseAgent
from typing import Dict, Any, List, Tuple
import logging
import re
from collections import Counter

logger = logging.getLogger(__name__)


class ResearchAgent(BaseAgent):
    """
    Extract key topics from transcription and generate research findings.
    
    Uses intelligent topic extraction, frequency analysis, and pattern matching.
    Returns prioritized findings with confidence scores.
    """
    
    # Stop words for filtering
    STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'is', 'are', 'was', 'were',
        'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'could', 'should', 'may', 'might', 'must', 'can', 'you', 'your',
        'i', 'me', 'my', 'we', 'our', 'he', 'she', 'it', 'this', 'that', 'these',
        'those', 'from', 'to', 'for', 'of', 'with', 'by', 'at', 'on', 'as', 'just',
        'so', 'like', 'right', 'also', 'there', 'get', 'got', 'make', 'go', 'come'
    }
    
    # Research context indicators
    RESEARCH_INDICATORS = [
        'research', 'study', 'analyze', 'investigate', 'discover', 'find', 
        'explore', 'examine', 'evaluate', 'test', 'experiment', 'prove',
        'demonstrate', 'show', 'reveal', 'understand', 'explain', 'learn'
    ]
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.max_results = config.get("max_research_results", 8) if config else 8
    
    def execute(self, transcription_text: str) -> Dict[str, Any]:
        """
        Extract topics and generate research findings from transcription.
        
        Args:
            transcription_text: Full transcription from TranscriptionAgent
            
        Returns:
            Dict with findings, topics, and research insights
        """
        if not self._validate_input(transcription_text):
            return {
                "findings": [],
                "search_terms_used": [],
                "topics_extracted": [],
                "research_areas": []
            }
        
        try:
            logger.info("Extracting research topics from transcription")
            
            # Extract intelligent topics
            topics = self.extract_topics(transcription_text)
            logger.info(f"Extracted {len(topics)} topics")
            
            # Generate research findings
            findings = self.generate_findings(transcription_text, topics)
            
            # Identify research areas
            research_areas = self.identify_research_areas(transcription_text)
            
            return {
                "findings": findings,
                "search_terms_used": [t[0] for t in topics[:5]],  # Top 5 as search terms
                "topics_extracted": [t[0] for t in topics],
                "research_areas": research_areas,
                "num_findings": len(findings),
                "num_topics": len(topics)
            }
        except Exception as e:
            logger.error(f"Research error: {str(e)}", exc_info=True)
            return {
                "findings": [],
                "search_terms_used": [],
                "topics_extracted": [],
                "research_areas": [],
                "error": str(e)
            }
    
    def extract_topics(self, text: str, num_topics: int = 8) -> List[Tuple[str, float]]:
        """
        Extract key topics with confidence scores using TF-IDF-style analysis.
        
        Args:
            text: Text to extract topics from
            num_topics: Number of topics to extract
            
        Returns:
            List of (topic, confidence) tuples sorted by confidence
        """
        try:
            text_lower = text.lower()
            topics_with_scores = []
            
            # 1. Extract multi-word noun phrases (2-4 words)
            phrases = self._extract_noun_phrases(text)
            
            # 2. Extract capitalized proper nouns
            proper_nouns = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
            
            # 3. Extract high-frequency important words
            important_words = self._extract_important_words(text)
            
            # Score extraction
            for phrase, count in phrases:
                score = min(count / max(len(text) / 1000, 1), 1.0)  # Normalize by text length
                topics_with_scores.append((phrase, score * 0.9))
            
            for word in important_words[:5]:
                topics_with_scores.append((word, 0.75))
            
            for noun in proper_nouns[:5]:
                topics_with_scores.append((noun, 0.70))
            
            # Remove duplicates and sort
            seen = set()
            unique_topics = []
            for topic, score in sorted(topics_with_scores, key=lambda x: x[1], reverse=True):
                topic_lower = topic.lower()
                if topic_lower not in seen and len(topic) > 2:
                    seen.add(topic_lower)
                    unique_topics.append((topic, score))
            
            return unique_topics[:num_topics]
        except Exception as e:
            logger.error(f"Topic extraction error: {e}")
            return []
    
    def _extract_noun_phrases(self, text: str, min_frequency: int = 2) -> List[Tuple[str, int]]:
        """
        Extract multi-word noun phrases with frequency count.
        
        Args:
            text: Text to analyze
            min_frequency: Minimum occurrences to include
            
        Returns:
            List of (phrase, count) tuples
        """
        # Extract bigrams and trigrams
        words = text.lower().split()
        bigrams = []
        trigrams = []
        
        for i in range(len(words) - 1):
            w1 = words[i].strip(',.!?()[]{}').lower()
            w2 = words[i + 1].strip(',.!?()[]{}').lower()
            
            if w1 not in self.STOP_WORDS and w2 not in self.STOP_WORDS and len(w1) > 3 and len(w2) > 3:
                bigrams.append(f"{w1} {w2}")
            
            if i < len(words) - 2:
                w3 = words[i + 2].strip(',.!?()[]{}').lower()
                if w1 not in self.STOP_WORDS and w2 not in self.STOP_WORDS and w3 not in self.STOP_WORDS:
                    trigrams.append(f"{w1} {w2} {w3}")
        
        bigram_counts = Counter(bigrams)
        trigram_counts = Counter(trigrams)
        
        # Combine, filter, and return
        phrases = []
        for phrase, count in trigram_counts.most_common(10):
            if count >= min_frequency:
                phrases.append((phrase, count))
        
        for phrase, count in bigram_counts.most_common(10):
            if count >= min_frequency and phrase not in [p[0] for p in phrases]:
                phrases.append((phrase, count))
        
        return phrases[:12]
    
    def _extract_important_words(self, text: str, num_words: int = 5) -> List[str]:
        """
        Extract high-value individual words.
        
        Args:
            text: Text to analyze
            num_words: Number of words to extract
            
        Returns:
            List of important words
        """
        words = text.lower().split()
        word_freq = Counter(
            w.strip(',.!?()[]{}') for w in words 
            if w.strip(',.!?()[]{}') not in self.STOP_WORDS and len(w) > 4
        )
        
        return [w for w, _ in word_freq.most_common(num_words)]
    
    def generate_findings(self, text: str, topics: List[Tuple[str, float]]) -> List[str]:
        """
        Generate research findings based on topics and text patterns.
        
        Args:
            text: Original transcription
            topics: List of (topic, confidence) tuples
            
        Returns:
            List of finding strings
        """
        try:
            findings = []
            used_sentences = set()  # Track which sentences we've already used
            sentences = [s.strip() for s in text.split('.') if s.strip() and len(s.strip()) > 15]
            
            # For each topic, find supporting evidence
            for topic, confidence in topics[:self.max_results]:
                topic_lower = topic.lower()
                
                # Find sentences mentioning this topic
                supporting_sentences = [
                    s for s in sentences 
                    if any(word in s.lower() for word in topic_lower.split())
                ]
                
                if supporting_sentences:
                    # Find an unused sentence (preference for longer/more detailed ones)
                    supporting_sentences_sorted = sorted(supporting_sentences, key=lambda x: len(x), reverse=True)
                    
                    key_sentence = None
                    for sent in supporting_sentences_sorted:
                        # Create a normalized version for comparison
                        sent_normalized = sent.lower()[:80]  # First 80 chars for comparison
                        if sent_normalized not in used_sentences:
                            key_sentence = sent
                            used_sentences.add(sent_normalized)
                            break
                    
                    # If all supporting sentences are used, find a different one
                    if not key_sentence and supporting_sentences_sorted:
                        key_sentence = supporting_sentences_sorted[0]  # Use best even if duplicate
                    
                    if key_sentence:
                        # Generate finding statement with better context
                        finding = self._generate_finding_statement(topic, key_sentence)
                        
                        if finding and finding not in findings:
                            findings.append(finding)
                else:
                    # If no direct match, look for semantic similarity
                    # Try to find sentences with related concepts
                    topic_words = set(topic_lower.split())
                    scored_sentences = []
                    
                    for sent in sentences:
                        sent_words = set(sent.lower().split())
                        overlap = len(topic_words & sent_words)
                        if overlap > 0:
                            scored_sentences.append((sent, overlap))
                    
                    if scored_sentences:
                        # Find an unused sentence from scored results
                        scored_sentences_sorted = sorted(scored_sentences, key=lambda x: x[1], reverse=True)
                        
                        best_sentence = None
                        for sent, score in scored_sentences_sorted:
                            sent_normalized = sent.lower()[:80]
                            if sent_normalized not in used_sentences:
                                best_sentence = sent
                                used_sentences.add(sent_normalized)
                                break
                        
                        if best_sentence:
                            finding = self._generate_finding_statement(topic, best_sentence)
                            if finding and finding not in findings:
                                findings.append(finding)
            
            # Ensure we have minimum findings - add focus areas for uncovered topics
            if len(findings) < 3 and len(topics) > len(findings):
                for topic, conf in topics[len(findings):]:
                    if not any(topic.lower() in f.lower() for f in findings):
                        finding = f"Focus: {topic} - Key topic with {int(conf*100)}% confidence"
                        if finding not in findings:
                            findings.append(finding)
            
            return findings[:self.max_results]
        except Exception as e:
            logger.error(f"Finding generation error: {e}")
            return []
    
    def _generate_finding_statement(self, topic: str, context: str) -> str:
        """
        Generate a well-formed finding statement from topic and context.
        
        Args:
            topic: The research topic
            context: Context sentence
            
        Returns:
            Finding statement
        """
        try:
            # Clean up context
            context = context.strip('.,;:!?')
            
            # Split into chunks to find relevant information around the topic
            words = context.split()
            topic_words = set(topic.lower().split())
            
            # Find meaningful phrases containing the topic
            context_lower = context.lower()
            
            # Look for specific patterns for better findings
            patterns = {
                'enable|allow|permit|support': f'{topic} enables or supports key functionality.',
                'require|require|need|must': f'{topic} is critical and requires careful implementation.',
                'improve|enhance|optimize|better': f'{topic} improvements lead to better performance and user experience.',
                'create|build|develop|design': f'{topic} is actively being developed and deployed.',
                'solve|fix|address|resolve': f'{topic} addresses important technical challenges.',
                'learn|understand|know|realize': f'{topic} provides important insights for development.',
                'risk|problem|issue|challenge': f'{topic} presents significant technical challenges that need attention.',
                'performance|speed|efficient|fast': f'{topic} directly impacts system performance and efficiency.',
                'security|protect|safe|secure': f'{topic} is crucial for security and system safety.',
            }
            
            # Try to find pattern matches
            for pattern, default_finding in patterns.items():
                if any(word in context_lower for word in pattern.split('|')):
                    # Extract meaningful part - get words around the topic
                    if len(words) > 10:
                        # Take a meaningful substring
                        limited_context = ' '.join(words[:min(20, len(words))])
                        return f"{topic}: {limited_context.capitalize()}"
                    else:
                        return default_finding
            
            # Smart fallback: Extract actual content from context
            if len(context) > 50:
                # Find the most relevant part of the context
                sentences_in_context = context.split(',')
                if len(sentences_in_context) > 1:
                    # Use the part that's not just the topic name
                    for sent in sentences_in_context:
                        if len(sent.strip()) > 20 and topic.lower() not in sent.lower():
                            return f"{topic}: {sent.strip().capitalize()}"
                
                # If all else fails, use the first part intelligently
                meaningful_part = context[:150].capitalize() if len(context) > 150 else context.capitalize()
                return f"{topic}: {meaningful_part}"
            else:
                return f"{topic}: {context.capitalize()}"
        
        except Exception as e:
            logger.error(f"Finding statement generation error: {e}")
            return f"Key research area: {topic}"
    
    def identify_research_areas(self, text: str) -> List[str]:
        """
        Identify broader research areas/domains discussed.
        
        Args:
            text: Transcription text
            
        Returns:
            List of research area categories
        """
        try:
            text_lower = text.lower()
            research_areas = []
            
            # Domain mappings
            domain_keywords = {
                "Machine Learning": ["ai", "artificial intelligence", "llm", "model", "training", "neural", "algorithm"],
                "Data Science": ["data", "analysis", "statistics", "dataset", "query", "vector"],
                "Software Engineering": ["code", "software", "build", "deploy", "architecture", "implementation"],
                "Web Technology": ["web", "api", "frontend", "backend", "database", "service"],
                "Product Development": ["product", "feature", "user", "design", "system", "development"],
                "Research & Innovation": ["research", "study", "experiment", "discover", "explore", "novel"],
                "Business & Strategy": ["business", "market", "strategy", "company", "enterprise", "solution"]
            }
            
            for area, keywords in domain_keywords.items():
                keyword_count = sum(1 for k in keywords if k in text_lower)
                if keyword_count >= 2:
                    research_areas.append(area)
            
            return research_areas[:4] if research_areas else ["Content Analysis"]
        except Exception as e:
            logger.error(f"Research area identification error: {e}")
            return ["Content Analysis"]
    
    def research(self, transcription: str) -> Dict[str, Any]:
        """
        Research topics in transcription (pipeline-compatible method).
        
        Args:
            transcription: Text to research
            
        Returns:
            Dictionary with findings and topics (alias for execute)
        """
        return self.execute(transcription)
