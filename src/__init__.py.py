# YouTube Channel Scraper Package
__version__ = "1.0.0"
__author__ = "Data Scientist"
__description__ = "Professional YouTube Channel Scraper with Selenium"

import logging

# Configure package-level logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

# Import main classes for easier access
try:
    from youtube_scraper import YouTubeScraper
    from data_processor import DataProcessor
    import config
    
    __all__ = [
        "YouTubeScraper",
        "DataProcessor",
        "config",
    ]
except ImportError:
    pass
