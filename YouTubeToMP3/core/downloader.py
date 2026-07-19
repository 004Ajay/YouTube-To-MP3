import os
import yt_dlp
from core.logger import setup_logger

logger = setup_logger("core.downloader")

class YouTubeDownloaderEngine:
    """Handles the business logic of interacting with YouTube streams independently of any UI layer."""

    @staticmethod
    def validate_inputs(url: str, output_dir: str) -> None:
        """Validates baseline execution parameters before launching heavy pipelines."""
        if not url.strip():
            raise ValueError("URL field cannot be empty.")
        if not output_dir:
            raise ValueError("An output directory path target must be assigned.")
        if not os.path.isdir(output_dir):
            raise ValueError(f"Target path structure is not a valid directory: {output_dir}")

    @classmethod
    def extract_mp3(cls, video_url: str, output_dir: str, custom_filename: str = None) -> None:
        """Downloads audio data from a URL source container and exports it cleanly as an MP3 file."""
        cls.validate_inputs(video_url, output_dir)
        
        url_clean = video_url.strip()
        filename_clean = custom_filename.strip() if custom_filename else None

        logger.info(f"Preparing download layout configurations for URL: {url_clean}")

        if filename_clean:
            out_template = os.path.join(output_dir, f"{filename_clean}.%(ext)s")
        else:
            out_template = os.path.join(output_dir, "%(title)s.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': out_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True
        }

        logger.info("Spawning backend stream extraction pipeline process.")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_clean])
        logger.info("Stream processing engine task completed successfully.")