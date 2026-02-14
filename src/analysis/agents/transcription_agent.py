"""
Transcription Agent - Extract audio from video and convert to text
Phase 1: Premium Implementation Using OpenAI Whisper
"""
from src.analysis.agents.base_agent import BaseAgent
from typing import Dict, Any, Optional
import os
import sys
import shutil
import subprocess
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def _ensure_ffmpeg_in_path():
    """
    Ensure ffmpeg is discoverable on PATH.
    
    Whisper calls ffmpeg via subprocess.run(["ffmpeg", ...]) which requires
    ffmpeg to be on the system PATH. In conda environments on Windows, ffmpeg
    is often installed at <conda_env>/Library/bin/ which may not be on PATH,
    or may be a broken build.
    
    This function tries multiple strategies:
    1. Check if ffmpeg is already on PATH and actually works
    2. Use imageio-ffmpeg's bundled binary (most reliable on Windows)
    3. Search conda environment paths
    """
    # Already on PATH and working?
    ffmpeg_loc = shutil.which("ffmpeg")
    if ffmpeg_loc is not None:
        # Verify it actually runs
        try:
            result = subprocess.run(
                [ffmpeg_loc, "-version"],
                capture_output=True, timeout=5
            )
            if result.returncode == 0:
                logger.debug("ffmpeg already on PATH and working: %s", ffmpeg_loc)
                return True
            else:
                logger.warning("ffmpeg on PATH but broken (exit %d): %s", result.returncode, ffmpeg_loc)
        except Exception:
            logger.warning("ffmpeg on PATH but failed to execute: %s", ffmpeg_loc)
    
    # Strategy 1: imageio-ffmpeg (bundled, most reliable)
    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        if os.path.isfile(ffmpeg_exe):
            ffmpeg_dir = os.path.dirname(ffmpeg_exe)
            # Whisper expects the binary to be named "ffmpeg", so create a symlink/copy if needed
            expected_name = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"
            expected_path = os.path.join(ffmpeg_dir, expected_name)
            
            if not os.path.isfile(expected_path):
                # Create a copy with the expected name
                import shutil as sh
                sh.copy2(ffmpeg_exe, expected_path)
                logger.info("Copied imageio-ffmpeg binary to: %s", expected_path)
            
            os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
            logger.info("Using imageio-ffmpeg binary from: %s", ffmpeg_dir)
            return True
    except ImportError:
        logger.debug("imageio-ffmpeg not installed, trying other methods")
    except Exception as e:
        logger.warning("imageio-ffmpeg fallback failed: %s", e)
    
    # Strategy 2: Conda environment paths
    candidate_dirs = []
    
    conda_prefix = os.environ.get("CONDA_PREFIX")
    if conda_prefix:
        candidate_dirs.append(os.path.join(conda_prefix, "Library", "bin"))
        candidate_dirs.append(os.path.join(conda_prefix, "bin"))
    
    python_dir = Path(sys.executable).resolve().parent
    candidate_dirs.append(str(python_dir / "Library" / "bin"))
    candidate_dirs.append(str(python_dir / ".." / "Library" / "bin"))
    candidate_dirs.append(str(python_dir))
    
    home = os.path.expanduser("~")
    for env_root in [
        os.path.join(home, "anaconda3"),
        os.path.join(home, "miniconda3"),
        os.path.join(home, "Anaconda3"),
        os.path.join(home, "Miniconda3"),
    ]:
        if os.path.isdir(env_root):
            envs_dir = os.path.join(env_root, "envs")
            if os.path.isdir(envs_dir):
                for env_name in os.listdir(envs_dir):
                    candidate_dirs.append(
                        os.path.join(envs_dir, env_name, "Library", "bin")
                    )
            candidate_dirs.append(os.path.join(env_root, "Library", "bin"))
    
    for d in candidate_dirs:
        ffmpeg_path = os.path.join(d, "ffmpeg.exe") if os.name == "nt" else os.path.join(d, "ffmpeg")
        if os.path.isfile(ffmpeg_path):
            # Verify it works
            try:
                result = subprocess.run(
                    [ffmpeg_path, "-version"],
                    capture_output=True, timeout=5
                )
                if result.returncode == 0:
                    logger.info("Found working ffmpeg at: %s", ffmpeg_path)
                    os.environ["PATH"] = d + os.pathsep + os.environ.get("PATH", "")
                    return True
                else:
                    logger.debug("ffmpeg at %s is broken (exit %d), skipping", ffmpeg_path, result.returncode)
            except Exception:
                logger.debug("ffmpeg at %s failed to execute, skipping", ffmpeg_path)
    
    logger.warning("Could not find a working ffmpeg in any known location")
    return False


class TranscriptionAgent(BaseAgent):
    """
    Extract audio from video and convert to text using OpenAI Whisper.
    
    Phase 1 of premium analysis implementation.
    Supports video formats: mp4, mov, avi, mkv, webm
    Model sizes: tiny, base, small, medium, large
    """
    
    # Supported video formats
    SUPPORTED_FORMATS = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.wmv'}
    
    # Model cache for efficient reuse
    _model_cache = {}
    
    # Track whether ffmpeg path has been set up
    _ffmpeg_ready = False
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.model_size = self.config.get("whisper_model", "base")
        self.device = self.config.get("whisper_device", "cpu")
        self.language = self.config.get("language", "en")
    
    def execute(self, video_path: str) -> str:
        """
        Transcribe video audio to text.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Full transcription text
        """
        if not self._validate_input(video_path):
            return "[Transcription unavailable - invalid input]"
        
        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            return f"[Transcription unavailable - file not found: {video_path}]"
        
        if not self._is_supported_format(video_path):
            logger.error(f"Unsupported video format: {video_path}")
            return f"[Transcription unavailable - unsupported format. Supported: {', '.join(self.SUPPORTED_FORMATS)}]"
        
        # Ensure ffmpeg is discoverable (Whisper needs it via subprocess)
        if not TranscriptionAgent._ffmpeg_ready:
            if _ensure_ffmpeg_in_path():
                TranscriptionAgent._ffmpeg_ready = True
            else:
                return "[Transcription unavailable - ffmpeg not found. Install ffmpeg and ensure it is on PATH]"
        
        try:
            logger.info(f"Starting transcription for: {video_path}")
            
            # Load or retrieve cached model
            model = self._get_model()
            
            if model is None:
                return "[Transcription unavailable - failed to load Whisper model]"
            
            # Transcribe audio
            logger.info(f"Transcribing with model size: {self.model_size}")
            result = model.transcribe(
                video_path,
                language=self.language,
                verbose=False
            )
            
            transcription = result.get("text", "").strip()
            
            if not transcription:
                logger.warning("Transcription produced empty output")
                return "[Transcription failed - no audio detected or no speech in video]"
            
            logger.info(f"Transcription completed successfully ({len(transcription)} chars)")
            return transcription
            
        except ImportError as e:
            logger.error("OpenAI Whisper not installed")
            return "[Transcription unavailable - openai-whisper not installed. Install with: pip install openai-whisper]"
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}", exc_info=True)
            return f"[Transcription error: {str(e)}]"
    
    def transcribe(self, video_path: str) -> str:
        """
        Alias for execute() for clarity.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Transcription text
        """
        return self.execute(video_path)
    
    def _get_model(self):
        """
        Get or load Whisper model with caching.
        
        Returns:
            Loaded Whisper model or None if failed
        """
        try:
            # Check cache first
            cache_key = f"{self.model_size}_{self.device}"
            if cache_key in self._model_cache:
                logger.debug(f"Using cached model: {cache_key}")
                return self._model_cache[cache_key]
            
            # Load model
            logger.info(f"Loading Whisper model: {self.model_size}")
            from whisper import load_model
            
            model = load_model(self.model_size, device=self.device)
            
            # Cache it
            self._model_cache[cache_key] = model
            logger.info(f"Model loaded and cached: {cache_key}")
            
            return model
        
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {str(e)}")
            return None
    
    def _is_supported_format(self, video_path: str) -> bool:
        """Check if video file has a supported format."""
        file_ext = Path(video_path).suffix.lower()
        return file_ext in self.SUPPORTED_FORMATS
