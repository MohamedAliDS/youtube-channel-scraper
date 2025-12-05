"""
YouTube Channel Scraper - COMPLETE VERSION (Standalone)
Windows-compatible, optimized, production-ready
Works with direct imports in Jupyter notebooks
"""

import logging
import time
from typing import Optional, List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.common.by import By
import urllib.parse

# Import with absolute imports (works in notebooks and scripts)
try:
    from . import config
    from . import selenium_utils as su
except ImportError:
    # Fallback for direct imports in Jupyter
    import config_UPDATED as config
    import selenium_utils_COMPLETE as su

logger = logging.getLogger(__name__)


class YouTubeScraper:
    """Main scraper class for YouTube channel operations."""

    def __init__(self, max_workers: int = None, headless: bool = True):
        """
        Initialize YouTubeScraper with optimizations.

        Args:
            max_workers: Number of parallel threads (default from config)
            headless: Run browser in headless mode
        """
        self.max_workers = max_workers or getattr(config, 'MAX_WORKERS', 6)
        self.headless = headless
        logger.info(f"[OK] YouTubeScraper initialized with {self.max_workers} workers")

    # ==================== CHANNEL SEARCH ====================

    def search_single_channel(self, channel_name: str) -> Optional[str]:
        """
        Search for a single channel by name and return its URL.
        Includes error recovery and retry logic.

        Args:
            channel_name: Name or alias of the channel
        Returns:
            Channel URL if found, None otherwise
        """
        driver = None
        retries = 0
        max_retries = getattr(config, 'MAX_RETRIES', 3)

        while retries < max_retries:
            try:
                driver = su.create_chrome_driver(headless=self.headless)

                # Try direct @alias URL first
                alias_clean = channel_name.strip().replace(" ", "")
                direct_url = f"https://www.youtube.com/@{alias_clean}"

                if su.safe_get(driver, direct_url):
                    if "404" not in driver.title and "This channel" not in driver.page_source:
                        logger.info(f"[OK] Found channel: {channel_name} -> {direct_url}")
                        return direct_url

                # Fallback to YouTube search
                logger.info(f"[INFO] Direct URL not found, searching for: {channel_name}")
                search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(channel_name)}"

                if su.safe_get(driver, search_url):
                    delay = getattr(config, 'DELAY_BETWEEN_REQUESTS', 1)
                    su.safe_sleep(delay)

                    # Find first channel link
                    channel_links = su.find_elements_safe(
                        driver, By.XPATH, "//a[@href and contains(@href, '/@')]"
                    )

                    if channel_links:
                        channel_url = su.get_attribute_safe(channel_links[0], "href")
                        if channel_url:
                            channel_url = su.normalize_url(channel_url)
                            logger.info(f"[OK] Found channel via search: {channel_name} -> {channel_url}")
                            return channel_url

                logger.warning(f"[WARN] Channel not found: {channel_name}")
                return None

            except Exception as e:
                retries += 1
                logger.error(f"[ERROR] Error searching channel {channel_name} (attempt {retries}/{max_retries}): {e}")

                if retries < max_retries:
                    wait_time = 2 ** retries  # Exponential backoff
                    logger.info(f"[INFO] Retrying in {wait_time} seconds...")
                    su.safe_sleep(wait_time)

            finally:
                su.close_driver(driver)

        return None

    def search_channels(self, channel_names: List[str]) -> List[Dict]:
        """
        Search for multiple channels in parallel with optimization.

        Args:
            channel_names: List of channel names
        Returns:
            List of dicts with 'alias' and 'channel_url' keys
        """
        results = []

        logger.info(f"[INFO] Starting parallel search with {self.max_workers} workers")
        logger.info(f"[INFO] Processing {len(channel_names)} channels...")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.search_single_channel, name): name
                for name in channel_names
            }

            completed = 0
            for future in as_completed(futures):
                name = futures[future]
                try:
                    url = future.result()
                    results.append({
                        "alias": name,
                        "channel_url": url if url else "Not Found"
                    })
                    completed += 1
                    logger.info(f"[INFO] Progress: {completed}/{len(channel_names)}")

                except Exception as e:
                    logger.error(f"[ERROR] Error processing {name}: {e}")
                    results.append({
                        "alias": name,
                        "channel_url": "Error"
                    })

        logger.info(f"[OK] Search completed! Found {sum(1 for r in results if r['channel_url'] != 'Not Found')} channels")
        return results

    # ==================== SOCIAL MEDIA LINKS ====================

    def extract_single_channel_links(self, channel_url: str) -> List[Dict]:
        """
        Extract social media links from a single channel.

        Args:
            channel_url: YouTube channel URL
        Returns:
            List of dicts with 'platform' and 'url' keys
        """
        driver = None
        results = []

        try:
            driver = su.create_chrome_driver(headless=self.headless)

            # Visit featured/home page
            featured_url = channel_url + "/featured"
            if not su.safe_get(driver, featured_url):
                return []

            # Try to expand "More" button in description
            try:
                more_buttons = su.find_elements_safe(
                    driver, By.XPATH, "//tp-yt-paper-button[contains(., 'more')]"
                )
                if more_buttons:
                    su.safe_click(driver, more_buttons[0])
                    su.safe_sleep(1)
            except:
                pass

            # Extract links from description
            desc_links = su.find_elements_safe(driver, By.CSS_SELECTOR, "#description a")
            for link_el in desc_links:
                platform_text = su.get_text_safe(link_el)
                raw_url = su.get_attribute_safe(link_el, "href")
                clean_url = su.clean_youtube_redirect(raw_url)

                if clean_url:
                    platform = self._normalize_platform(platform_text, clean_url)
                    if platform:
                        results.append({
                            "platform": platform,
                            "url": clean_url
                        })

            # Visit about page for official links
            about_url = channel_url + "/about"
            if su.safe_get(driver, about_url):
                su.safe_sleep(1)

                # Find links section
                link_elements = su.find_elements_safe(
                    driver, By.CSS_SELECTOR, "#links-section yt-channel-external-link-view-model"
                )

                for el in link_elements:
                    try:
                        platform_el = el.find_element(By.CSS_SELECTOR, ".ytChannelExternalLinkViewModelTitle")
                        platform_text = su.get_text_safe(platform_el)
                        link_el = el.find_element(By.TAG_NAME, "a")
                        raw_url = su.get_attribute_safe(link_el, "href")
                        clean_url = su.clean_youtube_redirect(raw_url)

                        if clean_url:
                            platform = self._normalize_platform(platform_text, clean_url)
                            if platform:
                                results.append({
                                    "platform": platform,
                                    "url": clean_url
                                })
                    except:
                        continue

            logger.info(f"[OK] Extracted {len(results)} links from {channel_url}")

        except Exception as e:
            logger.error(f"[ERROR] Error extracting links from {channel_url}: {e}")
        finally:
            su.close_driver(driver)

        return results

    def extract_social_links(self, channel_urls: List[str]) -> List[Dict]:
        """
        Extract social media links from multiple channels in parallel.

        Args:
            channel_urls: List of YouTube channel URLs
        Returns:
            List of dicts with 'channel_url', 'platform', and 'url' keys
        """
        results = []
        logger.info(f"[INFO] Starting link extraction with {self.max_workers} workers")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.extract_single_channel_links, url): url
                for url in channel_urls
            }

            for future in as_completed(futures):
                channel_url = futures[future]
                try:
                    links = future.result()
                    for link_data in links:
                        results.append({
                            "channel_url": channel_url,
                            **link_data
                        })
                except Exception as e:
                    logger.error(f"[ERROR] Error processing {channel_url}: {e}")

        logger.info(f"[OK] Link extraction completed! Total links found: {len(results)}")
        return results

    # ==================== HELPER METHODS ====================

    @staticmethod
    def _normalize_platform(platform_text: str, url: str) -> Optional[str]:
        """
        Normalize platform name from text and URL.

        Args:
            platform_text: Platform name from link text
            url: Link URL
        Returns:
            Standardized platform name or None
        """
        platform_lower = platform_text.lower()
        url_lower = url.lower()

        # Check known platforms
        if "instagram" in url_lower or "instagram" in platform_lower:
            return "Instagram"
        elif "tiktok" in url_lower or "tiktok" in platform_lower:
            return "TikTok"
        elif "twitter" in url_lower or "x.com" in url_lower or "twitter" in platform_lower:
            return "X (Twitter)"
        elif "facebook" in url_lower or "facebook" in platform_lower:
            return "Facebook"
        elif "telegram" in url_lower or "t.me" in url_lower or "telegram" in platform_lower:
            return "Telegram"
        elif "discord" in url_lower or "discord.gg" in url_lower:
            return "Discord"
        elif "snapchat" in url_lower or "snapchat" in platform_lower:
            return "Snapchat"
        elif "youtube.com/channel" in url_lower or "youtube.com/c/" in url_lower:
            return "YouTube Channel"
        elif "@" in url_lower:
            return "Email"

        return None


logger.info("[OK] YouTube Scraper module loaded successfully")
