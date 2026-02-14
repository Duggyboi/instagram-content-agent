"""
Categorization Agent - Intelligent content classification using multi-source context
Phase 2: Premium Implementation
"""
from src.analysis.agents.base_agent import BaseAgent
from typing import Dict, Any, List
import logging
import re
from collections import Counter

logger = logging.getLogger(__name__)


class CategorizationAgent(BaseAgent):
    """
    Classify video content using transcription, research findings, and summary.
    
    Leverages research areas identified and summary insights for improved categorization.
    Assigns multiple categories with confidence scores and relevant tags.
    """
    
    DEFAULT_CATEGORIES = [
        "Educational",
        "Entertainment", 
        "News",
        "Tutorial",
        "Review",
        "How-to",
        "Vlog",
        "Comedy",
        "Technology",
        "Business",
        "Lifestyle",
        "Gaming",
        "Sports",
        "Music",
        "Art",
        "Science",
        "Politics",
        "Health",
        "Food",
        "Travel"
    ]
    
    # Keywords associated with each category
    CATEGORY_KEYWORDS = {
        "Educational": ["learn", "explain", "teach", "course", "lesson", "education", "knowledge", "study", "understand", "concepts", "principles"],
        "Entertainment": ["fun", "entertainment", "enjoy", "watch", "show", "amusing", "entertaining", "funny", "humor"],
        "News": ["news", "report", "breaking", "happening", "current", "events", "update", "latest", "announcement"],
        "Tutorial": ["tutorial", "guide", "how to", "step", "instruction", "demo", "walkthrough", "learn how"],
        "Review": ["review", "opinion", "rating", "recommend", "verdict", "thoughts", "critique", "assessment"],
        "How-to": ["how to", "guide", "process", "method", "technique", "procedure", "steps", "build", "create"],
        "Vlog": ["vlog", "vlogging", "day in my life", "personal", "journal", "daily", "follow along"],
        "Comedy": ["funny", "laugh", "comic", "joke", "humor", "hilarious", "comedy", "comedic"],
        "Technology": ["tech", "software", "hardware", "code", "coding", "programming", "app", "digital", "algorithm", "system"],
        "Business": ["business", "company", "corporate", "money", "finance", "marketing", "sales", "enterprise", "startup", "strategy"],
        "Lifestyle": ["lifestyle", "routine", "wellness", "habit", "productivity", "self-improvement", "daily", "living"],
        "Gaming": ["game", "gaming", "video game", "console", "esports", "stream", "gameplay", "gamer", "play"],
        "Sports": ["sport", "athletic", "team", "competition", "athlete", "championship", "match", "tournament", "game"],
        "Music": ["music", "song", "track", "musical", "instrument", "concert", "rhythm", "melody", "artist"],
        "Art": ["art", "paint", "draw", "creative", "design", "aesthetic", "artist", "visual", "creative process"],
        "Science": ["science", "scientific", "research", "experiment", "study", "data", "discovery", "theory", "hypothesis"],
        "Politics": ["politics", "political", "election", "government", "policy", "parliament", "vote", "congress"],
        "Health": ["health", "medical", "doctor", "disease", "fitness", "exercise", "wellness", "nutrition", "healthcare"],
        "Food": ["food", "recipe", "cook", "cooking", "cuisine", "culinary", "eat", "restaurant", "dish"],
        "Travel": ["travel", "journey", "destination", "trip", "explore", "adventure", "tourism", "visit", "location"]
    }
    
    # Map research areas to categories
    RESEARCH_AREA_CATEGORY_MAP = {
        "Machine Learning": ["Technology", "Science", "Educational"],
        "Data Science": ["Science", "Technology", "Educational"],
        "Software Engineering": ["Technology", "How-to", "Tutorial"],
        "Web Technology": ["Technology", "Tutorial", "How-to"],
        "Product Development": ["Business", "Technology", "How-to"],
        "Research & Innovation": ["Science", "Educational", "Technology"],
        "Business & Strategy": ["Business", "Educational", "News"]
    }
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.categories = config.get("categories", self.DEFAULT_CATEGORIES) if config else self.DEFAULT_CATEGORIES
    
    def execute(self, transcription_text: str, research_results: Dict[str, Any] = None, summary_results: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Categorize and tag video content using multi-source context.
        
        Args:
            transcription_text: Full transcription from TranscriptionAgent
            research_results: Research findings from ResearchAgent (optional)
            summary_results: Summary results from SummaryAgent (optional)
            
        Returns:
            Dict with categories, tags, and confidence scores
        """
        if not self._validate_input(transcription_text):
            return {
                "categories": [],
                "tags": [],
                "primary_category": None
            }
        
        try:
            logger.info("Categorizing content with context-aware analysis")
            
            # Classify content with context
            categories = self.classify(transcription_text, research_results, summary_results)
            
            # Extract tags
            tags = self.extract_tags(transcription_text, research_results, summary_results)
            
            # Determine primary category
            primary = categories[0]["name"] if categories else None
            
            return {
                "categories": categories,
                "tags": tags,
                "primary_category": primary,
                "num_categories": len(categories),
                "num_tags": len(tags)
            }
        except Exception as e:
            logger.error(f"Categorization error: {str(e)}", exc_info=True)
            return {
                "categories": [],
                "tags": [],
                "primary_category": None,
                "error": str(e)
            }
    
    def classify(self, text: str, research_results: Dict[str, Any] = None, summary_results: Dict[str, Any] = None, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Classify text using keyword matching and research context with intelligent suppression.
        
        Args:
            text: Text to classify
            research_results: Research findings for context boost
            summary_results: Summary for additional context
            top_k: Number of top categories to return
            
        Returns:
            List of categories with confidence scores (0-100)
        """
        try:
            text_lower = text.lower()
            category_scores = {}
            
            # 1. Base scoring from keyword matches with minimum thresholds
            for category, keywords in self.CATEGORY_KEYWORDS.items():
                score = 0
                matched_keywords = 0
                
                for keyword in keywords:
                    # Use word boundary matching for more accuracy
                    if self._is_keyword_present(text_lower, keyword):
                        count = text_lower.count(keyword)
                        score += min(count, 3)  # Cap at 3 per keyword
                        matched_keywords += 1
                
                # Only include categories with meaningful keyword presence
                # Weak categories (Music, Entertainment, Vlog) need stronger evidence
                weak_categories = {"Music", "Entertainment", "Vlog", "Comedy"}
                min_keywords = 3 if category in weak_categories else 1
                
                if matched_keywords >= min_keywords:
                    category_scores[category] = score
            
            # 2. Determine research domain strength (if available)
            research_domain = None
            if research_results and "research_areas" in research_results:
                research_areas = research_results.get("research_areas", [])
                if research_areas:
                    research_domain = research_areas[0]  # Primary domain
            
            # 3. Boost technical categories if research domain is tech-focused
            if research_domain in ["Machine Learning", "Data Science", "Software Engineering", "Web Technology"]:
                # Suppress non-technical categories
                for weak_cat in ["Music", "Entertainment", "Comedy", "Vlog", "Art", "Food", "Travel"]:
                    if weak_cat in category_scores:
                        category_scores[weak_cat] = category_scores[weak_cat] * 0.3  # Reduce to 30%
                
                # Boost technical categories
                category_scores["Technology"] = category_scores.get("Technology", 0) + 40
                category_scores["Science"] = category_scores.get("Science", 0) + 30
                category_scores["Educational"] = category_scores.get("Educational", 0) + 25
            
            # 4. Boost business categories if research domain is business
            elif research_domain == "Business & Strategy":
                for weak_cat in ["Music", "Entertainment", "Comedy", "Vlog"]:
                    if weak_cat in category_scores:
                        category_scores[weak_cat] = category_scores[weak_cat] * 0.2
                
                category_scores["Business"] = category_scores.get("Business", 0) + 40
                category_scores["Educational"] = category_scores.get("Educational", 0) + 20
            
            # 5. Boost based on research topics
            if research_results and "topics_extracted" in research_results:
                topics = research_results.get("topics_extracted", [])
                topic_str = " ".join(topics).lower()
                
                # Tech/science indicators
                tech_keywords = ["ai", "llm", "model", "algorithm", "code", "software", "data", "system", "optimization"]
                science_keywords = ["research", "study", "experiment", "analysis", "theory", "hypothesis"]
                business_keywords = ["business", "market", "strategy", "product", "company"]
                
                tech_count = sum(1 for kw in tech_keywords if kw in topic_str)
                science_count = sum(1 for kw in science_keywords if kw in topic_str)
                business_count = sum(1 for kw in business_keywords if kw in topic_str)
                
                if tech_count >= 2:
                    category_scores["Technology"] = category_scores.get("Technology", 0) + 25
                if science_count >= 2:
                    category_scores["Science"] = category_scores.get("Science", 0) + 25
                if business_count >= 2:
                    category_scores["Business"] = category_scores.get("Business", 0) + 25
            
            # 6. Boost educational content if summary has key takeaways
            if summary_results and "key_takeaways" in summary_results:
                takeaways = summary_results.get("key_takeaways", [])
                if len(takeaways) >= 3:
                    category_scores["Educational"] = category_scores.get("Educational", 0) + 30
            
            # 7. Remove unreliable categories if they have very low scores relative to top category
            if category_scores:
                max_score = max(category_scores.values())
                threshold = max_score * 0.15  # Remove categories with <15% of max score
                
                weak_cats_to_check = ["Music", "Entertainment", "Comedy", "Vlog"]
                for cat in weak_cats_to_check:
                    if cat in category_scores and category_scores[cat] < threshold:
                        del category_scores[cat]
            
            # Fallback
            if not category_scores:
                category_scores[self.DEFAULT_CATEGORIES[0]] = 20
            
            # Normalize scores to confidence (0-100)
            max_score = max(category_scores.values()) if category_scores else 1
            results = []
            
            for category, score in sorted(category_scores.items(), key=lambda x: x[1], reverse=True):
                confidence = int((score / max_score) * 100)
                results.append({
                    "name": category,
                    "confidence": min(confidence, 100)
                })
            
            return results[:top_k]
        except Exception as e:
            logger.error(f"Classification error: {e}")
            return []
    
    def _is_keyword_present(self, text: str, keyword: str) -> bool:
        """
        Check if keyword is present with word boundary awareness.
        
        Args:
            text: Text to search in
            keyword: Keyword to find
            
        Returns:
            True if keyword is found
        """
        # For multi-word keywords, just check substring
        if " " in keyword:
            return keyword in text
        
        # For single words, use word boundary matching
        import re
        pattern = r'\b' + re.escape(keyword) + r'\b'
        return bool(re.search(pattern, text))
    
    def categorize(self, transcription: str, research_results: Dict[str, Any] = None, summary_results: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Categorize transcription with optional context (pipeline-compatible method).
        
        Args:
            transcription: Text to categorize
            research_results: Research findings for context
            summary_results: Summary for context
            
        Returns:
            Dictionary with categories and tags (alias for execute)
        """
        return self.execute(transcription, research_results, summary_results)
    
    def extract_tags(self, text: str, research_results: Dict[str, Any] = None, summary_results: Dict[str, Any] = None, num_tags: int = 12) -> List[str]:
        """
        Extract relevant tags and hashtags from text and research context.
        
        Args:
            text: Text to extract tags from
            research_results: Research findings to extract tags from
            summary_results: Summary to extract tags from
            num_tags: Maximum number of tags to extract
            
        Returns:
            List of tag strings
        """
        try:
            tags = []
            
            # 1. Extract existing hashtags
            hashtags = re.findall(r'#\w+', text)
            tags.extend([tag[1:].lower() for tag in hashtags])
            
            # 2. Extract capitalized phrases as tags
            phrases = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
            tags.extend([p.lower() for p in phrases if len(p) > 2])
            
            # 3. Extract keywords from all category keywords that appear in text
            text_lower = text.lower()
            for category, keywords in self.CATEGORY_KEYWORDS.items():
                for keyword in keywords:
                    if keyword in text_lower and keyword not in tags and len(keyword) > 2:
                        tags.append(keyword)
            
            # 4. Add research topics as tags
            if research_results and "topics_extracted" in research_results:
                research_topics = research_results.get("topics_extracted", [])
                for topic in research_topics[:5]:  # Top 5 research topics
                    if topic and len(topic) > 2:
                        tags.append(topic.lower().replace(" ", "-"))
            
            # 5. Add research areas as tags
            if research_results and "research_areas" in research_results:
                research_areas = research_results.get("research_areas", [])
                for area in research_areas:
                    tags.append(area.lower().replace(" ", "-"))
            
            # 6. Extract key concepts from summary
            if summary_results and "key_takeaways" in summary_results:
                takeaways = summary_results.get("key_takeaways", [])
                # Extract first word from each takeaway as concept tag
                for takeaway in takeaways[:3]:
                    words = takeaway.split()
                    if words and len(words[0]) > 3:
                        tags.append(words[0].lower().strip(',.!?'))
            
            # Remove duplicates while preserving order
            tags = list(dict.fromkeys(tags))
            
            # Filter short tags
            tags = [t for t in tags if len(t) > 2]
            
            return tags[:num_tags]
        except Exception as e:
            logger.error(f"Tag extraction error: {e}")
            return []
