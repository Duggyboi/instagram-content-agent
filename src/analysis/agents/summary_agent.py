"""
Summary Agent - Generate high-quality summaries using LLM
Phase 2: Premium Implementation
"""
from src.analysis.agents.base_agent import BaseAgent
from typing import Dict, Any, List
import logging
import json
import re
from collections import Counter

logger = logging.getLogger(__name__)


class SummaryAgent(BaseAgent):
    """
    Generate concise summaries of video content using intelligent text processing.
    
    Extracts summary and key takeaways from transcription with priority-aware highlighting.
    """
    
    # Stop words to ignore in frequency analysis
    STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'is', 'are', 'was', 'were',
        'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'could', 'should', 'may', 'might', 'must', 'can', 'you', 'your',
        'i', 'me', 'my', 'we', 'our', 'he', 'she', 'it', 'this', 'that', 'these',
        'those', 'from', 'to', 'for', 'of', 'with', 'by', 'at', 'on', 'as', 'just',
        'so', 'like', 'right', "it's", "that's", "it'll", "you'll"
    }
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self._llm = None
        self._initialized = False
    
    def execute(self, transcription_text: str) -> Dict[str, Any]:
        """
        Generate summary from transcription.
        
        Args:
            transcription_text: Full transcription from TranscriptionAgent
            
        Returns:
            Dict with summary and key takeaways
        """
        if not self._validate_input(transcription_text):
            return {
                "summary": "[Summary unavailable - invalid input]",
                "key_takeaways": []
            }
        
        if not transcription_text or len(transcription_text) < 50:
            return {
                "summary": "[Summary unavailable - transcription too short]",
                "key_takeaways": []
            }
        
        try:
            logger.info(f"Generating summary from {len(transcription_text)} chars")
            
            # Clean and normalize transcription
            cleaned_text = self._clean_transcription(transcription_text)
            
            # Generate intelligent summary
            summary = self._generate_intelligent_summary(cleaned_text)
            
            # Extract priority-aware key takeaways
            key_takeaways = self.extract_key_takeaways(cleaned_text, num_points=5)
            
            return {
                "summary": summary if summary else "[Summary generation failed]",
                "key_takeaways": key_takeaways,
                "char_count": len(transcription_text)
            }
        except Exception as e:
            logger.error(f"Summary generation error: {str(e)}", exc_info=True)
            return {
                "summary": f"[Summary error: {str(e)}]",
                "key_takeaways": [],
                "error": str(e)
            }
    
    def summarize(self, transcription: str) -> Dict[str, Any]:
        """
        Summarize transcription (pipeline-compatible method).
        
        Args:
            transcription: Text to summarize
            
        Returns:
            Dictionary with summary and key takeaways (alias for execute)
        """
        return self.execute(transcription)
    
    def _clean_transcription(self, text: str) -> str:
        """
        Clean and normalize transcription text.
        
        Args:
            text: Raw transcription
            
        Returns:
            Cleaned text
        """
        # Fix common speech-to-text issues
        text = re.sub(r'\b(um|uh|hmm|like|you know|basically|literally)\b', '', text, flags=re.IGNORECASE)
        
        # Fix spacing
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\s+([.,!?])', r'\1', text)
        
        # Remove repeated punctuation
        text = re.sub(r'\.+', '.', text)
        text = re.sub(r'!+', '!', text)
        
        return text.strip()
    
    def _generate_intelligent_summary(self, text: str, max_sentences: int = 3) -> str:
        """
        Generate summary using importance scoring.
        
        Args:
            text: Cleaned text
            max_sentences: Target summary length
            
        Returns:
            Summary text
        """
        try:
            sentences = [s.strip() for s in text.split('.') if s.strip() and len(s.strip()) > 20]
            
            if len(sentences) <= max_sentences:
                return '. '.join(sentences) + '.'
            
            # Calculate word frequencies (excluding stop words)
            words = text.lower().split()
            word_freq = Counter(
                w.strip(',.!?()[]{}') for w in words 
                if w.strip(',.!?()[]{}') not in self.STOP_WORDS and len(w) > 3
            )
            
            # Score sentences by cumulative word importance
            sentence_scores = {}
            for i, sent in enumerate(sentences):
                score = 0
                words_in_sent = sent.lower().split()
                
                # Base score: word frequency
                for word in words_in_sent:
                    clean_word = word.strip(',.!?()[]{}')
                    score += word_freq.get(clean_word, 0)
                
                # Bonus: sentences mentioning top topics get higher score
                top_words = [w for w, _ in word_freq.most_common(5)]
                for top_word in top_words:
                    if top_word in sent.lower():
                        score += word_freq[top_word] * 2  # Double weight for top topics
                
                # Bonus: longer content sentences are more informative
                score += len(words_in_sent) * 0.5
                
                sentence_scores[i] = score
            
            # Select top sentences maintaining original order
            top_indices = sorted(sorted(range(len(sentences)), key=lambda i: sentence_scores.get(i, 0), reverse=True)[:max_sentences])
            summary = '. '.join(sentences[i] for i in top_indices) + '.'
            
            return summary
        except Exception as e:
            logger.error(f"Intelligent summarization error: {e}")
            return text.split('.')[0] + '.' if text else "[Summary failed]"
    
    def extract_key_takeaways(self, text: str, num_points: int = 5) -> List[str]:
        """
        Extract key takeaways based on topic priority and frequency.
        
        Args:
            text: Cleaned text
            num_points: Number of key points to extract
            
        Returns:
            List of key takeaway strings ordered by priority
        """
        try:
            sentences = [s.strip() for s in text.split('.') if s.strip() and len(s.strip()) > 15]
            
            if not sentences:
                return []
            
            # Extract key noun phrases and their frequency
            key_phrases = self._extract_key_phrases(text)
            
            # Score sentences based on key phrase relevance
            sentence_scores = {}
            for i, sent in enumerate(sentences):
                sent_lower = sent.lower()
                score = 0
                
                # Score based on key phrase mentions
                for phrase, freq in key_phrases[:8]:  # Top 8 phrases
                    if phrase.lower() in sent_lower:
                        score += freq
                
                # Bonus: look for action/imperative words
                action_words = ['learn', 'build', 'create', 'design', 'develop', 'understand',
                               'implement', 'apply', 'use', 'need', 'must', 'should', 'important',
                               'key', 'need to', 'have to', 'ensure', 'prevent', 'avoid']
                for action in action_words:
                    if action.lower() in sent_lower:
                        score += 3
                
                sentence_scores[i] = score
            
            # Get top scoring sentences
            top_indices = sorted(range(len(sentences)), key=lambda i: sentence_scores.get(i, 0), reverse=True)[:num_points]
            
            # Sort by original order for better flow
            top_indices = sorted(top_indices)
            
            takeaways = [sentences[i] for i in top_indices if sentence_scores.get(i, 0) > 0]
            
            # If still not enough, add high-confident sentences
            if len(takeaways) < num_points:
                for i in top_indices:
                    if sentences[i] not in takeaways:
                        takeaways.append(sentences[i])
                    if len(takeaways) >= num_points:
                        break
            
            return takeaways[:num_points]
        except Exception as e:
            logger.error(f"Key takeaway extraction error: {e}")
            return []
    
    def _extract_key_phrases(self, text: str, num_phrases: int = 10) -> List[tuple]:
        """
        Extract key phrases that capture main topics.
        
        Args:
            text: Text to analyze
            num_phrases: Number of phrases to extract
            
        Returns:
            List of (phrase, frequency) tuples
        """
        try:
            # Extract multi-word phrases and important single words
            words = text.lower().split()
            
            # Get important single words
            word_freq = Counter(
                w.strip(',.!?()[]{}') for w in words 
                if w.strip(',.!?()[]{}') not in self.STOP_WORDS and len(w) > 4
            )
            
            # Get bigrams (2-word phrases)
            bigrams = []
            for i in range(len(words) - 1):
                w1 = words[i].strip(',.!?()[]{}').lower()
                w2 = words[i + 1].strip(',.!?()[]{}').lower()
                if w1 not in self.STOP_WORDS and w2 not in self.STOP_WORDS and len(w1) > 3 and len(w2) > 3:
                    bigrams.append(f"{w1} {w2}")
            
            bigram_freq = Counter(bigrams)
            
            # Combine and rank
            all_phrases = []
            
            # Add bigrams with good frequency
            for phrase, freq in bigram_freq.most_common(5):
                if freq >= 2:
                    all_phrases.append((phrase, freq * 2))  # Weight multi-word phrases higher
            
            # Add top single words
            for word, freq in word_freq.most_common(10):
                all_phrases.append((word, freq))
            
            # Sort by frequency
            all_phrases = sorted(all_phrases, key=lambda x: x[1], reverse=True)
            
            return all_phrases[:num_phrases]
        except Exception as e:
            logger.error(f"Key phrase extraction error: {e}")
            return []
