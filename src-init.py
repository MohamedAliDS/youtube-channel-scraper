"""YouTube Channel Scraper - Main Package

A production-ready Python tool for scraping YouTube channel data,
extracting social media links, and calculating engagement metrics.

Features:
- Parallel channel search with 6 workers
- Social media link extraction (Instagram, TikTok, Discord, etc.)
- Engagement metrics and categorization
- Windows-compatible encoding
- Comprehensive error handling
- Full Jupyter notebook integration

Usage:
    from src.youtube_scraper_COMPLETE_FIXED import YouTubeScraper
    from src.data_processor_COMPLETE_FIXED import DataProcessor
    from src.config_UPDATED import *

Author: YouTube Channel Scraper Team
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "YouTube Channel Scraper Team"
__license__ = "MIT"
__description__ = "Automated YouTube channel scraper with social media link extraction"

# Import main classes for easy access
try:
    from .youtube_scraper_COMPLETE_FIXED import YouTubeScraper
    from .data_processor_COMPLETE_FIXED import DataProcessor
    from .config_UPDATED import (
        MAX_WORKERS,
        MAX_RETRIES,
        HEADLESS_MODE,
        DELAY_BETWEEN_REQUESTS,
        TIMEOUT,
        USER_AGENTS,
    )
except ImportError as e:
    print(f"[WARN] Could not import all modules: {e}")
    print("[INFO] Make sure all files are in src/ folder")

__all__ = [
    'YouTubeScraper',
    'DataProcessor',
    'MAX_WORKERS',
    'MAX_RETRIES',
    'HEADLESS_MODE',
    'DELAY_BETWEEN_REQUESTS',
    'TIMEOUT',
    'USER_AGENTS',
]
