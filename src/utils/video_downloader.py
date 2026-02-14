"""
Video Downloader Module
Handles downloading videos from various sources (YouTube, direct URLs, Instagram, etc.)
"""

import os
import re
from pathlib import Path
from typing import Optional, Tuple, Callable
import logging
from urllib.parse import urlparse
import requests

logger = logging.getLogger(__name__)


class VideoDownloader:
    """Download videos from various sources."""
    
    # Supported URL patterns
    YOUTUBE_PATTERNS = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch',
        r'(?:https?://)?(?:www\.)?youtu\.be/',
        r'(?:https?://)?(?:www\.)?youtube\.com/shorts/'
    ]
    
    INSTAGRAM_PATTERNS = [
        r'(?:https?://)?(?:www\.)?instagram\.com/(?:p|reel|tv)/',
        r'(?:https?://)?(?:www\.)?instagr(?:\.am|am\.com)/'
    ]
    
    TIKTOK_PATTERNS = [
        r'(?:https?://)?(?:www\.)?tiktok\.com/@[\w\.]+/video/',
        r'(?:https?://)?(?:www\.)?vm\.tiktok\.com/',
        r'(?:https?://)?(?:www\.)?vt\.tiktok\.com/'
    ]
    
    def __init__(self, output_dir: str = "temp_uploads"):
        """Initialize the downloader."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def detect_url_type(url: str) -> str:
        """
        Detect the type of URL.
        
        Returns: 'youtube', 'instagram', 'tiktok', or 'direct'
        """
        url_lower = url.lower().strip()
        
        for pattern in VideoDownloader.YOUTUBE_PATTERNS:
            if re.search(pattern, url_lower):
                return "youtube"
        
        for pattern in VideoDownloader.INSTAGRAM_PATTERNS:
            if re.search(pattern, url_lower):
                return "instagram"
        
        for pattern in VideoDownloader.TIKTOK_PATTERNS:
            if re.search(pattern, url_lower):
                return "tiktok"
        
        # Check if it's a direct video URL
        if url_lower.startswith(('http://', 'https://')):
            return "direct"
        
        return "unknown"
    
    def download(
        self,
        url: str,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Download a video from the URL.
        
        Args:
            url: Video URL
            progress_callback: Function to call with progress messages
        
        Returns:
            Tuple of (success, message, file_path)
        """
        def log_progress(msg: str):
            logger.info(msg)
            if progress_callback:
                progress_callback(msg)
        
        # Validate URL
        url = url.strip()
        if not url:
            return False, "URL cannot be empty", None
        
        # Detect URL type
        url_type = self.detect_url_type(url)
        log_progress(f"Detected URL type: {url_type}")
        
        if url_type == "unknown":
            return False, "Unknown URL format. Supported: YouTube, Instagram, TikTok, direct video URLs", None
        
        try:
            if url_type == "youtube":
                return self._download_youtube(url, log_progress)
            elif url_type == "tiktok":
                return self._download_tiktok(url, log_progress)
            elif url_type == "instagram":
                return self._download_instagram(url, log_progress)
            else:  # direct
                return self._download_direct(url, log_progress)
        
        except Exception as e:
            error_msg = f"Download failed: {str(e)}"
            logger.error(error_msg)
            return False, error_msg, None
    
    def _download_youtube(self, url: str, log_progress: Callable) -> Tuple[bool, str, Optional[str]]:
        """Download from YouTube using yt-dlp."""
        try:
            import yt_dlp
        except ImportError:
            return False, "yt-dlp not installed. Install with: pip install yt-dlp", None
        
        log_progress("Downloading from YouTube...")
        
        try:
            output_template = str(self.output_dir / "%(title)s_%(id)s.%(ext)s")
            
            ydl_opts = {
                'format': 'best[ext=mp4]/best[ext=webm]/best',
                'outtmpl': output_template,
                'quiet': False,
                'no_warnings': False,
                'progress_hooks': [self._yt_dlp_progress_hook(log_progress)],
                'socket_timeout': 30,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                file_path = Path(filename)
                
                if file_path.exists():
                    log_progress(f"✓ Download complete: {file_path.name}")
                    return True, f"Downloaded: {file_path.name}", str(file_path)
                else:
                    return False, "Download completed but file not found", None
        
        except Exception as e:
            return False, f"YouTube download failed: {str(e)}", None
    
    def _download_tiktok(self, url: str, log_progress: Callable) -> Tuple[bool, str, Optional[str]]:
        """Download from TikTok using yt-dlp."""
        try:
            import yt_dlp
        except ImportError:
            return False, "yt-dlp not installed. Install with: pip install yt-dlp", None
        
        log_progress("Downloading from TikTok...")
        
        try:
            output_template = str(self.output_dir / "tiktok_%(id)s.%(ext)s")
            
            ydl_opts = {
                'format': 'best[ext=mp4]/best[ext=webm]/best',
                'outtmpl': output_template,
                'quiet': False,
                'no_warnings': False,
                'socket_timeout': 30,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                file_path = Path(filename)
                
                if file_path.exists():
                    log_progress(f"✓ Download complete: {file_path.name}")
                    return True, f"Downloaded: {file_path.name}", str(file_path)
                else:
                    return False, "Download completed but file not found", None
        
        except Exception as e:
            return False, f"TikTok download failed: {str(e)}", None
    
    def _download_instagram(self, url: str, log_progress: Callable) -> Tuple[bool, str, Optional[str]]:
        """Download from Instagram using yt-dlp."""
        try:
            import yt_dlp
        except ImportError:
            return False, "yt-dlp not installed. Install with: pip install yt-dlp", None
        
        log_progress("Downloading from Instagram...")
        
        try:
            output_template = str(self.output_dir / "instagram_%(id)s.%(ext)s")
            
            ydl_opts = {
                'format': 'best[ext=mp4]/best[ext=webm]/best',
                'outtmpl': output_template,
                'quiet': False,
                'no_warnings': False,
                'socket_timeout': 30,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                file_path = Path(filename)
                
                if file_path.exists():
                    log_progress(f"✓ Download complete: {file_path.name}")
                    return True, f"Downloaded: {file_path.name}", str(file_path)
                else:
                    return False, "Download completed but file not found", None
        
        except Exception as e:
            return False, f"Instagram download failed: {str(e)}", None
    
    def _download_direct(self, url: str, log_progress: Callable) -> Tuple[bool, str, Optional[str]]:
        """Download from direct HTTP/HTTPS URL."""
        log_progress("Downloading from direct URL...")
        
        try:
            # Extract filename from URL
            parsed_url = urlparse(url)
            filename = Path(parsed_url.path).name
            
            if not filename or '.' not in filename:
                filename = "downloaded_video.mp4"
            
            # Sanitize filename
            filename = "".join(c for c in filename if c.isalnum() or c in '._-')
            file_path = self.output_dir / filename
            
            # Download the file
            log_progress(f"Downloading: {filename}")
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = int((downloaded / total_size) * 100)
                            log_progress(f"Progress: {percent}%")
            
            if file_path.exists() and file_path.stat().st_size > 0:
                log_progress(f"✓ Download complete: {filename}")
                return True, f"Downloaded: {filename}", str(file_path)
            else:
                return False, "Downloaded file is empty or doesn't exist", None
        
        except requests.exceptions.RequestException as e:
            return False, f"Download failed: {str(e)}", None
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    @staticmethod
    def _yt_dlp_progress_hook(log_progress: Callable):
        """Create a progress hook for yt-dlp."""
        def hook(d):
            if d['status'] == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes', 0)
                if total > 0:
                    percent = int((downloaded / total) * 100)
                    log_progress(f"Downloading: {percent}%")
            elif d['status'] == 'finished':
                log_progress("Download finished, processing...")
        
        return hook
    
    def cleanup_old_videos(self, max_age_hours: int = 24) -> int:
        """
        Delete downloaded videos older than specified hours.
        
        Returns: Number of files deleted
        """
        import time
        
        if not self.output_dir.exists():
            return 0
        
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        deleted_count = 0
        
        for video_file in self.output_dir.glob("*"):
            if video_file.is_file():
                file_age = current_time - video_file.stat().st_mtime
                if file_age > max_age_seconds:
                    try:
                        video_file.unlink()
                        logger.info(f"Deleted old video: {video_file.name}")
                        deleted_count += 1
                    except Exception as e:
                        logger.error(f"Failed to delete {video_file.name}: {e}")
        
        return deleted_count
    
    def get_video_info(self, url: str) -> Optional[dict]:
        """Get video metadata without downloading."""
        try:
            import yt_dlp
        except ImportError:
            return None
        
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'description': info.get('description', ''),
                    'ext': info.get('ext', 'Unknown'),
                }
        except Exception as e:
            logger.error(f"Failed to get video info: {e}")
            return None
