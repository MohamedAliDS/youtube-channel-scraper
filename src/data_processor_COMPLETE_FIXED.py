"""
Data Processor Module - Windows Compatible, Standalone (COMPLETE)
Handles Excel I/O, data transformation, and Windows encoding
Works directly in Jupyter notebooks - ALL METHODS INCLUDED
"""

import logging
import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path
import sys
import io

# ==================== WINDOWS ENCODING FIX ====================
# Fix UTF-8 encoding on Windows console
if sys.platform == 'win32':
    # Reconfigure stdout/stderr for UTF-8
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except:
        pass  # Fallback if already wrapped

# ==================== LOGGING SETUP ====================
def setup_logging(level='INFO'):
    """
    Setup logging with Windows-compatible formatting.
    Uses [OK], [ERROR], [WARN] instead of emoji
    """

    class WindowsSafeFormatter(logging.Formatter):
        """Formatter that works on Windows console"""

        def format(self, record):
            msg = super().format(record)
            # Replace emoji with ASCII equivalents
            msg = msg.replace('✅', '[OK]')
            msg = msg.replace('❌', '[ERROR]')
            msg = msg.replace('⚠️', '[WARN]')
            msg = msg.replace('🔍', '[SEARCH]')
            msg = msg.replace('📊', '[STATS]')
            msg = msg.replace('🔗', '[LINK]')
            msg = msg.replace('🚀', '[START]')
            return msg

    logger = logging.getLogger()
    logger.setLevel(level)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Format without emoji
    formatter = WindowsSafeFormatter(
        '[%(levelname)s] %(asctime)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


# ==================== DATA PROCESSOR CLASS ====================
class DataProcessor:
    """
    Handle data transformation and Excel I/O
    Windows-compatible with proper encoding
    COMPLETE with all methods including categorize_views
    """

    @staticmethod
    def read_excel(file_path: str, column_name: str = 'alias'):
        """
        Read Excel file and extract column data

        Args:
            file_path: Path to Excel file
            column_name: Column to extract

        Returns:
            List of values from column
        """
        try:
            df = pd.read_excel(file_path)
            items = df[column_name].tolist()
            logger = logging.getLogger(__name__)
            logger.info(f"[OK] Read {len(items)} items from {file_path}")
            return items
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"[ERROR] Failed to read {file_path}: {e}")
            raise

    @staticmethod
    def save_results(results: list, output_file: str, output_dir: str = 'data/processed'):
        """
        Save results to Excel file

        Args:
            results: List of result dictionaries
            output_file: Output filename
            output_dir: Output directory
        """
        try:
            df = pd.DataFrame(results)
            output_path = Path(output_dir) / output_file
            output_path.parent.mkdir(parents=True, exist_ok=True)

            df.to_excel(output_path, index=False, engine='openpyxl')

            logger = logging.getLogger(__name__)
            logger.info(f"[OK] Saved {len(results)} results to {output_path}")

            return str(output_path)

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"[ERROR] Failed to save results: {e}")
            raise

    @staticmethod
    def pivot_social_links(results: list):
        """
        Pivot social media links data

        Args:
            results: Raw links data

        Returns:
            Pivoted DataFrame with platforms as columns
        """
        try:
            df = pd.DataFrame(results)

            # Pivot so each channel is one row
            pivot_df = df.pivot_table(
                index='channel_url',
                columns='platform',
                values='url',
                aggfunc='first'
            ).reset_index()

            logger = logging.getLogger(__name__)
            logger.info(f"[OK] Pivoted {len(pivot_df)} unique channels")

            return pivot_df

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"[ERROR] Failed to pivot data: {e}")
            raise

    @staticmethod
    def categorize_views(avg_views: Optional[int]) -> str:
        """
        Categorize average views into engagement bins.

        Args:
            avg_views: Average view count

        Returns:
            Category string (e.g., "100k-250k")
        """
        if avg_views is None:
            return "N/A"

        # Define categories with thresholds
        categories = [
            ("< 5k", 5000),
            ("5k-10k", 10000),
            ("10k-25k", 25000),
            ("25k-50k", 50000),
            ("50k-100k", 100000),
            ("100k-250k", 250000),
            ("250k-1M", 1000000),
            ("1M+", float('inf')),
        ]

        # Find matching category
        for category, threshold in categories:
            if avg_views < threshold:
                return category

        return "1M+"

    @staticmethod
    def merge_dataframes(df1: pd.DataFrame, df2: pd.DataFrame, on: str = None) -> pd.DataFrame:
        """
        Merge two DataFrames

        Args:
            df1: First DataFrame
            df2: Second DataFrame
            on: Column(s) to merge on

        Returns:
            Merged DataFrame
        """
        try:
            merged = pd.merge(df1, df2, on=on, how="left")
            logger = logging.getLogger(__name__)
            logger.info(f"[OK] Merged DataFrames: {len(merged)} rows")
            return merged
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"[ERROR] Error merging DataFrames: {e}")
            raise


# ==================== MODULE INITIALIZATION ====================
logger = logging.getLogger(__name__)

if sys.platform == 'win32':
    logger.info('[INFO] Windows platform detected - UTF-8 encoding enabled')
else:
    logger.info(f'[INFO] {sys.platform.upper()} platform detected')

logger.info('[INFO] Data processor module loaded successfully')

# Default paths (matches config)
DATA_RAW_DIR = 'data/raw'
DATA_PROCESSED_DIR = 'data/processed'
