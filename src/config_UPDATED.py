
"""
YouTube Scraper Configuration
All settings optimized for Windows & performance
"""

# ==================== SELENIUM SETTINGS ====================
HEADLESS_MODE = True
PAGE_LOAD_TIMEOUT = 15  # seconds
IMPLICIT_WAIT = 10     # seconds
EXPLICIT_WAIT = 20     # seconds

# ==================== SCRAPING SETTINGS ====================
MAX_WORKERS = 6        # OPTIMIZED: 6 workers (Windows stable + fast)
                       # Options: 4 (conservative), 6 (balanced), 8+ (fast)
DELAY_BETWEEN_REQUESTS = 1  # seconds (helps with rate limiting)
MAX_RETRIES = 3        # retry attempts before giving up

# ==================== OUTPUT SETTINGS ====================
OUTPUT_DIR = 'data/processed'
LOG_LEVEL = 'INFO'

# ==================== ADVANCED SETTINGS ====================
USE_PROXY = False
PROXY_LIST = []
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# ==================== WINDOWS-SPECIFIC FIXES ====================
# Set UTF-8 encoding for Windows console
WINDOWS_UTF8_ENCODING = True
DISABLE_EMOJI_LOGGING = True  # Use [OK], [ERROR] instead of ✅, ❌

# ==================== PERFORMANCE TUNING ====================
# Adjust these based on your system resources
CHROME_MEMORY_PERCENT = 80    # Max % of system RAM Chrome can use
CPU_CORES_TO_USE = 6          # Max CPU cores to use (matches MAX_WORKERS)
BATCH_SIZE = 10               # Process channels in batches
BATCH_DELAY = 5               # Delay between batches (seconds)

print("[INFO] Configuration loaded successfully")
print(f"[INFO] Max workers: {MAX_WORKERS}")
print(f"[INFO] Headless mode: {HEADLESS_MODE}")
print(f"[INFO] UTF-8 encoding: {WINDOWS_UTF8_ENCODING}")
