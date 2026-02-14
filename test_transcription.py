#!/usr/bin/env python
"""
Test script for Transcription Agent Phase 1 implementation
Verifies Whisper installation and model loading
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_whisper_installation():
    """Test if whisper is installed and can be imported"""
    logger.info("Testing Whisper installation...")
    try:
        import whisper
        logger.info(f"✓ Whisper is installed: {whisper.__file__}")
        return True
    except ImportError as e:
        logger.error(f"✗ Whisper not installed: {e}")
        return False

def test_transcription_agent_import():
    """Test if TranscriptionAgent can be imported"""
    logger.info("Testing TranscriptionAgent import...")
    try:
        from src.analysis.agents import TranscriptionAgent
        logger.info("✓ TranscriptionAgent imported successfully")
        return True
    except ImportError as e:
        logger.error(f"✗ Failed to import TranscriptionAgent: {e}")
        return False

def test_agent_instantiation():
    """Test if TranscriptionAgent can be instantiated"""
    logger.info("Testing TranscriptionAgent instantiation...")
    try:
        from src.analysis.agents import TranscriptionAgent
        
        config = {
            "whisper_model": "base",
            "whisper_device": "cpu",
            "language": "en"
        }
        agent = TranscriptionAgent(config)
        logger.info(f"✓ TranscriptionAgent created with model: {agent.model_size}")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to instantiate agent: {e}")
        return False

def test_model_loading():
    """Test if Whisper model can load (first run will download)"""
    logger.info("Testing Whisper model loading...")
    logger.info("Note: First run will download the model (~140MB for 'base')")
    
    try:
        from src.analysis.agents import TranscriptionAgent
        
        config = {"whisper_model": "tiny"}  # Use tiny for faster testing
        agent = TranscriptionAgent(config)
        model = agent._get_model()
        
        if model is None:
            logger.error("✗ Model loading returned None")
            return False
        
        logger.info(f"✓ Model loaded successfully: {agent.model_size}")
        return True
    except Exception as e:
        logger.error(f"✗ Model loading failed: {e}", exc_info=True)
        return False

def test_invalid_file_handling():
    """Test graceful handling of invalid files"""
    logger.info("Testing invalid file handling...")
    try:
        from src.analysis.agents import TranscriptionAgent
        
        agent = TranscriptionAgent()
        result = agent.transcribe("/nonexistent/file.mp4")
        
        if "not found" in result.lower():
            logger.info(f"✓ Invalid file handled correctly: {result}")
            return True
        else:
            logger.error(f"✗ Unexpected result: {result}")
            return False
    except Exception as e:
        logger.error(f"✗ Error handling failed: {e}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    logger.info("=" * 60)
    logger.info("PHASE 1: LOCAL WHISPER TRANSCRIPTION - TEST SUITE")
    logger.info("=" * 60)
    
    tests = [
        ("Whisper Installation", test_whisper_installation),
        ("TranscriptionAgent Import", test_transcription_agent_import),
        ("Agent Instantiation", test_agent_instantiation),
        ("Invalid File Handling", test_invalid_file_handling),
        ("Model Loading", test_model_loading),  # Run last as it's slowest
    ]
    
    results = []
    for name, test_func in tests:
        logger.info("")
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            logger.error(f"Unexpected error in {name}: {e}", exc_info=True)
            results.append((name, False))
    
    # Summary
    logger.info("")
    logger.info("=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status}: {name}")
    
    logger.info("-" * 60)
    logger.info(f"Results: {passed}/{total} tests passed")
    logger.info("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
