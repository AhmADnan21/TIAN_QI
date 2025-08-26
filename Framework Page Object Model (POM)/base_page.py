from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
import time
import logging

class BasePage:
    """Base page class that provides common functionality for all page objects"""
    
    def __init__(self, driver, wait_timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_timeout)
        self.logger = logging.getLogger(__name__)
    
    def find_element(self, locator, timeout=None):
        """Find element with explicit wait"""
        wait_time = timeout if timeout else 20
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.presence_of_element_located(locator))
    
    def find_clickable_element(self, locator, timeout=None):
        """Find clickable element with explicit wait"""
        wait_time = timeout if timeout else 20
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def find_visible_element(self, locator, timeout=None):
        """Find visible element with explicit wait"""
        wait_time = timeout if timeout else 20
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def click_element(self, locator, timeout=None):
        """Click element with JavaScript fallback"""
        try:
            element = self.find_clickable_element(locator, timeout)
            element.click()
        except Exception as e:
            self.logger.warning(f"Regular click failed, trying JavaScript click: {e}")
            element = self.find_element(locator, timeout)
            self.driver.execute_script("arguments[0].click();", element)
    
    def input_text(self, locator, text, timeout=None):
        """Input text into element"""
        element = self.find_clickable_element(locator, timeout)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator, timeout=None):
        """Get text from element"""
        element = self.find_element(locator, timeout)
        return element.text
    
    def is_element_present(self, locator, timeout=5):
        """Check if element is present"""
        try:
            self.find_element(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible"""
        try:
            self.find_visible_element(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def wait_for_url_change(self, expected_url_part, timeout=10):
        """Wait for URL to contain specific part"""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda d: expected_url_part in d.current_url)
    
    def wait_for_page_load(self, timeout=10):
        """Wait for page to load completely"""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    
    def switch_to_window(self, window_index=-1):
        """Switch to window by index (default: last window)"""
        self.driver.switch_to.window(self.driver.window_handles[window_index])
    
    def close_current_window(self):
        """Close current window and switch to first window"""
        self.driver.close()
        if len(self.driver.window_handles) > 0:
            self.driver.switch_to.window(self.driver.window_handles[0])
    
    def take_screenshot(self, filename):
        """Take screenshot and save to file"""
        self.driver.save_screenshot(filename)
        self.logger.info(f"Screenshot saved: {filename}")
    
    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url
    
    def navigate_to(self, url):
        """Navigate to URL"""
        self.driver.get(url)
        self.wait_for_page_load()
        self.logger.info(f"Navigated to: {url}") 