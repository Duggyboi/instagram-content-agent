"""Test the ProofreaderAgent implementation"""
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from src.analysis.agents import ProofreaderAgent
from datetime import datetime

def test_proofreader_initialization():
    """Test that ProofreaderAgent initializes correctly"""
    config = {
        "ollama_host": "http://localhost:11434",
        "ollama_model": "mistral",
        "enable_refinement": True
    }
    
    agent = ProofreaderAgent(config)
    assert agent.ollama_host == "http://localhost:11434"
    assert agent.model == "mistral"
    print("[PASS] ProofreaderAgent initialization test passed")

def test_proofreader_with_mock_results():
    """Test proofreader with mock results"""
    config = {
        "ollama_host": "http://localhost:11434",
        "ollama_model": "mistral"
    }
    
    agent = ProofreaderAgent(config)
    
    # Create mock results
    mock_results = {
        "transcription": "This is a test transcription about machine learning and artificial intelligence. " * 10,
        "summary": {
            "summary": "A comprehensive overview of ML and AI concepts.",
            "key_takeaways": ["ML requires data", "AI is evolving", "Models need training"]
        },
        "research": {
            "findings": ["Finding 1 about ML", "Finding 2 about AI"],
            "topics_extracted": [("machine learning", 0.9), ("artificial intelligence", 0.85)],
            "research_areas": ["Machine Learning", "Artificial Intelligence"]
        },
        "categorization": {
            "categories": [
                {"name": "Technology", "confidence": 95},
                {"name": "Science", "confidence": 85}
            ],
            "primary_category": "Technology",
            "tags": ["ML", "AI", "Data Science"]
        }
    }
    
    # Call proofreader - note: this will gracefully handle Ollama unavailability
    validation_metadata = agent.proofread(mock_results)
    
    # Verify structure - validation should complete even if Ollama is unavailable
    assert "validated" in validation_metadata
    assert "validation_timestamp" in validation_metadata
    assert "model_used" in validation_metadata
    assert "validation_results" in validation_metadata
    
    print("[PASS] ProofreaderAgent mock results test passed")
    print(f"   Validation structure: {list(validation_metadata.keys())}")
    print(f"   Ollama available: {validation_metadata.get('validated', False)}")
    if not validation_metadata.get('validated'):
        print(f"   Reason: {validation_metadata.get('reason', 'Unknown')}")

if __name__ == "__main__":
    print("Running ProofreaderAgent tests...\n")
    
    test_proofreader_initialization()
    test_proofreader_with_mock_results()
    
    print("\n[PASS] All ProofreaderAgent tests passed!")
