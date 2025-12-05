
"""
Selenium Utilities - Windows Compatible
Helper functions for Selenium operations with error recovery
"""

import logging
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

logger = logging.getLogger(__name__)


def create_chrome_driver(headless=True, timeout=15):
    """
    Create Chrome WebDriver with Windows compatibility

    Args:
        headless: Run in headless mode
        timeout: Page load timeout

    Returns:
        Chrome WebDriver instance
    """
    try:
        options = webdriver.ChromeOptions()

        if headless:
            options.add_argument('--headless')

        # Windows-friendly options
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-web-resources')
        options.add_argument('start-maximized')

        # Performance
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-sync')

        # Setup Chrome driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Set timeouts
        driver.set_page_load_timeout(timeout)
        driver.implicitly_wait(10)

        logger.info('[OK] Chrome driver created successfully')
        return driver

    except Exception as e:
        logger.error(f'[ERROR] Failed to create Chrome driver: {e}')
        # Auto-retry with delay
        logger.info('[INFO] Retrying after 2 second delay...')
        time.sleep(2)
        try:
            return create_chrome_driver(headless, timeout)
        except Exception as retry_error:
            logger.error(f'[ERROR] Retry failed: {retry_error}')
            raise


def safe_get(driver, url, timeout=10):
    """
    Safely navigate to URL with error handling

    Args:
        driver: WebDriver instance
        url: URL to navigate to
        timeout: Navigation timeout

    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info(f'[INFO] Navigating to {url}')
        driver.get(url)
        return True
    except TimeoutException:
        logger.warning(f'[WARN] Timeout loading {url}')
        return False
    except Exception as e:
        logger.error(f'[ERROR] Failed to navigate to {url}: {e}')
        return False


def safe_click(driver, element, timeout=10):
    """Safely click element with error handling"""
    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(element))
        element.click()
        return True
    except Exception as e:
        logger.error(f'[ERROR] Failed to click element: {e}')
        return False


def safe_sleep(duration=1):
    """Sleep with logging"""
    time.sleep(duration)


def close_driver(driver):
    """Safely close driver"""
    try:
        if driver:
            driver.quit()
            logger.info('[OK] Driver closed')
    except Exception as e:
        logger.error(f'[ERROR] Error closing driver: {e}')


def find_elements_safe(driver, by, value):
    """Safely find elements"""
    try:
        return driver.find_elements(by, value)
    except NoSuchElementException:
        return []
    except Exception as e:
        logger.error(f'[ERROR] Error finding elements: {e}')
        return []


def get_text_safe(element):
    """Safely get element text"""
    try:
        return element.text
    except Exception:
        return ''


def get_attribute_safe(element, attribute):
    """Safely get element attribute"""
    try:
        return element.get_attribute(attribute)
    except Exception:
        return None


def normalize_url(url):
    """Normalize YouTube URL"""
    if url.startswith('/'):
        return f'https://www.youtube.com{url}'
    return url


def clean_youtube_redirect(url):
    """Clean YouTube redirect URLs"""
    if url and 'redirect' in url:
        try:
            # Extract actual URL from redirect
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            if 'q' in params:
                return params['q'][0]
        except:
            pass
    return url


logger.info('[INFO] Selenium utilities loaded successfully')
