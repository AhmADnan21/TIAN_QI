"""
Navigation Helper
Navigation and page management methods
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.framework_config import FrameworkConfig
from config.test_data_config import AppURLs
import time
import logging

class NavigationHelper:
    """Navigation and page management helper class"""
    
    def __init__(self, driver, element_helper):
        self.driver = driver
        self.element_helper = element_helper
        self.logger = logging.getLogger(__name__)
    
    def navigate_to_login_page(self, environment="test"):
        """Navigate to login page"""
        login_url = AppURLs.get_login_url(environment)
        self.element_helper.navigate_to(login_url)
        self.logger.info(f"Navigated to login page: {login_url}")
    
    def navigate_to_package_order_page(self, environment="test"):
        """Navigate to package order page"""
        package_order_url = AppURLs.get_package_order_url(environment)
        self.element_helper.navigate_to(package_order_url)
        self.logger.info(f"Navigated to package order page: {package_order_url}")
    
    def navigate_to_personal_center_page(self, environment="test"):
        """Navigate to personal center page"""
        personal_center_url = AppURLs.get_personal_center_url(environment)
        self.element_helper.navigate_to(personal_center_url)
        self.logger.info(f"Navigated to personal center page: {personal_center_url}")
    
    def navigate_to_recharge_page(self, environment="test"):
        """Navigate to recharge page"""
        base_url = AppURLs.get_base_url(environment)
        recharge_url = base_url + AppURLs.RECHARGE_PAGE
        self.element_helper.navigate_to(recharge_url)
        self.logger.info(f"Navigated to recharge page: {recharge_url}")
    
    def navigate_to_home_page(self, environment="test"):
        """Navigate to home page"""
        home_url = AppURLs.get_base_url(environment)
        self.element_helper.navigate_to(home_url)
        self.logger.info(f"Navigated to home page: {home_url}")
    
    def navigate_to_url(self, url):
        """Navigate to specific URL"""
        self.element_helper.navigate_to(url)
        self.logger.info(f"Navigated to URL: {url}")
    
    def navigate_back(self):
        """Navigate back in browser history"""
        self.driver.back()
        self.logger.info("Navigated back in browser history")
    
    def navigate_forward(self):
        """Navigate forward in browser history"""
        self.driver.forward()
        self.logger.info("Navigated forward in browser history")
    
    def refresh_current_page(self):
        """Refresh current page"""
        self.element_helper.refresh_page()
        self.logger.info("Refreshed current page")
    
    def wait_for_page_load(self, timeout=None):
        """Wait for page to load completely"""
        self.element_helper.wait_for_page_load(timeout)
        self.logger.debug("Page loaded completely")
    
    def wait_for_url_change(self, expected_url_part, timeout=None):
        """Wait for URL to contain specific part"""
        self.element_helper.wait_for_url_change(expected_url_part, timeout)
        self.logger.debug(f"URL changed to contain: {expected_url_part}")
    
    def wait_for_url_to_be(self, expected_url, timeout=None):
        """Wait for URL to be exactly as expected"""
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(lambda d: d.current_url == expected_url)
        self.logger.debug(f"URL changed to: {expected_url}")
    
    def get_current_url(self):
        """Get current URL"""
        return self.element_helper.get_current_url()
    
    def get_page_title(self):
        """Get page title"""
        return self.element_helper.get_page_title()
    
    def is_on_login_page(self):
        """Check if currently on login page"""
        current_url = self.get_current_url()
        return "/login" in current_url
    
    def is_on_package_order_page(self):
        """Check if currently on package order page"""
        current_url = self.get_current_url()
        return "/packageOrder" in current_url
    
    def is_on_personal_center_page(self):
        """Check if currently on personal center page"""
        current_url = self.get_current_url()
        return "/personal" in current_url
    
    def is_on_recharge_page(self):
        """Check if currently on recharge page"""
        current_url = self.get_current_url()
        return "/recharge" in current_url
    
    def is_on_home_page(self):
        """Check if currently on home page"""
        current_url = self.get_current_url()
        base_url = AppURLs.get_base_url()
        return current_url == base_url or current_url == base_url + "/"
    
    def switch_to_new_window(self):
        """Switch to newly opened window"""
        if len(self.driver.window_handles) > 1:
            self.element_helper.switch_to_window(-1)
            self.logger.info("Switched to new window")
            return True
        else:
            self.logger.warning("No new window found")
            return False
    
    def switch_to_main_window(self):
        """Switch to main window (first window)"""
        if len(self.driver.window_handles) > 0:
            self.element_helper.switch_to_window(0)
            self.logger.info("Switched to main window")
            return True
        else:
            self.logger.warning("No windows found")
            return False
    
    def close_all_windows_except_main(self):
        """Close all windows except the main window"""
        main_window = self.driver.window_handles[0]
        for window in self.driver.window_handles[1:]:
            self.driver.switch_to.window(window)
            self.driver.close()
        self.driver.switch_to.window(main_window)
        self.logger.info("Closed all windows except main window")
    
    def get_window_count(self):
        """Get number of open windows"""
        return len(self.driver.window_handles)
    
    def wait_for_new_window(self, timeout=None):
        """Wait for a new window to open"""
        initial_window_count = self.get_window_count()
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        
        def window_count_increased(driver):
            return len(driver.window_handles) > initial_window_count
        
        wait.until(window_count_increased)
        self.logger.info("New window opened")
    
    def wait_for_window_to_close(self, timeout=None):
        """Wait for a window to close"""
        initial_window_count = self.get_window_count()
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        
        def window_count_decreased(driver):
            return len(driver.window_handles) < initial_window_count
        
        wait.until(window_count_decreased)
        self.logger.info("Window closed")
    
    def switch_to_frame(self, frame_locator, timeout=None):
        """Switch to iframe"""
        self.element_helper.switch_to_frame(frame_locator, timeout)
    
    def switch_to_default_content(self):
        """Switch back to default content"""
        self.element_helper.switch_to_default_content()
    
    def accept_alert(self, timeout=None):
        """Accept alert dialog"""
        self.element_helper.accept_alert(timeout)
    
    def dismiss_alert(self, timeout=None):
        """Dismiss alert dialog"""
        self.element_helper.dismiss_alert(timeout)
    
    def get_alert_text(self, timeout=None):
        """Get alert text"""
        return self.element_helper.get_alert_text(timeout)
    
    def send_keys_to_alert(self, text, timeout=None):
        """Send keys to alert prompt"""
        self.element_helper.send_keys_to_alert(text, timeout)
    
    def wait_for_alert_present(self, timeout=None):
        """Wait for alert to be present"""
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(EC.alert_is_present())
        self.logger.debug("Alert is present")
    
    def scroll_to_element(self, locator, timeout=None):
        """Scroll to element"""
        self.element_helper.scroll_to_element(locator, timeout)
    
    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        self.element_helper.scroll_to_bottom()
    
    def scroll_to_top(self):
        """Scroll to top of page"""
        self.element_helper.scroll_to_top()
    
    def take_screenshot(self, filename):
        """Take screenshot and save to file"""
        self.element_helper.take_screenshot(filename)
    
    def wait_for_element_to_be_clickable(self, locator, timeout=None):
        """Wait for element to be clickable"""
        self.element_helper.wait_for_element_clickable(locator, timeout)
    
    def wait_for_element_to_be_visible(self, locator, timeout=None):
        """Wait for element to be visible"""
        self.element_helper.wait_for_element_visible(locator, timeout)
    
    def wait_for_element_to_disappear(self, locator, timeout=None):
        """Wait for element to disappear"""
        self.element_helper.wait_for_element_disappear(locator, timeout)
    
    def wait_for_text_present(self, locator, text, timeout=None):
        """Wait for specific text to be present in element"""
        self.element_helper.wait_for_text_present(locator, text, timeout)
    
    def is_element_present(self, locator, timeout=5):
        """Check if element is present"""
        return self.element_helper.is_element_present(locator, timeout)
    
    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible"""
        return self.element_helper.is_element_visible(locator, timeout)
    
    def is_element_clickable(self, locator, timeout=5):
        """Check if element is clickable"""
        return self.element_helper.is_element_clickable(locator, timeout) 