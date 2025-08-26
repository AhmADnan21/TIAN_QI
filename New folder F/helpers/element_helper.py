"""
Element Helper
Enhanced element interaction methods for WebDriver
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from config.framework_config import FrameworkConfig
import time
import logging

class ElementHelper:
    """Enhanced element interaction helper class"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, FrameworkConfig.DEFAULT_TIMEOUT)
        self.actions = ActionChains(driver)
        self.logger = logging.getLogger(__name__)
    
    def find_element(self, locator, timeout=None):
        """Find element with explicit wait"""
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator, timeout=None):
        """Find multiple elements with explicit wait"""
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.presence_of_all_elements_located(locator))
    
    def find_clickable_element(self, locator, timeout=None):
        """Find clickable element with explicit wait"""
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def find_visible_element(self, locator, timeout=None):
        """Find visible element with explicit wait"""
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def click_element(self, locator, timeout=None, use_js=False):
        """Click element with JavaScript fallback"""
        try:
            if use_js:
                element = self.find_element(locator, timeout)
                self.driver.execute_script("arguments[0].click();", element)
            else:
                element = self.find_clickable_element(locator, timeout)
                element.click()
            self.logger.debug(f"Clicked element: {locator}")
        except Exception as e:
            self.logger.warning(f"Regular click failed, trying JavaScript click: {e}")
            element = self.find_element(locator, timeout)
            self.driver.execute_script("arguments[0].click();", element)
    
    def input_text(self, locator, text, timeout=None, clear_first=True):
        """Input text into element"""
        element = self.find_clickable_element(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
        self.logger.debug(f"Entered text '{text}' into element: {locator}")
    
    def get_text(self, locator, timeout=None):
        """Get text from element"""
        element = self.find_element(locator, timeout)
        text = element.text
        self.logger.debug(f"Got text '{text}' from element: {locator}")
        return text
    
    def get_attribute(self, locator, attribute, timeout=None):
        """Get attribute value from element"""
        element = self.find_element(locator, timeout)
        value = element.get_attribute(attribute)
        self.logger.debug(f"Got attribute '{attribute}'='{value}' from element: {locator}")
        return value
    
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
    
    def is_element_clickable(self, locator, timeout=5):
        """Check if element is clickable"""
        try:
            self.find_clickable_element(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_present(self, locator, timeout=None):
        """Wait for element to be present"""
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(EC.presence_of_element_located(locator))
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible"""
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable"""
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(EC.element_to_be_clickable(locator))
    
    def wait_for_element_disappear(self, locator, timeout=None):
        """Wait for element to disappear"""
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(EC.invisibility_of_element_located(locator))
    
    def wait_for_text_present(self, locator, text, timeout=None):
        """Wait for specific text to be present in element"""
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(EC.text_to_be_present_in_element(locator, text))
    
    def hover_over_element(self, locator, timeout=None):
        """Hover over element"""
        element = self.find_element(locator, timeout)
        self.actions.move_to_element(element).perform()
        self.logger.debug(f"Hovered over element: {locator}")
    
    def double_click_element(self, locator, timeout=None):
        """Double click element"""
        element = self.find_clickable_element(locator, timeout)
        self.actions.double_click(element).perform()
        self.logger.debug(f"Double clicked element: {locator}")
    
    def right_click_element(self, locator, timeout=None):
        """Right click element"""
        element = self.find_clickable_element(locator, timeout)
        self.actions.context_click(element).perform()
        self.logger.debug(f"Right clicked element: {locator}")
    
    def drag_and_drop(self, source_locator, target_locator, timeout=None):
        """Drag and drop element"""
        source = self.find_element(source_locator, timeout)
        target = self.find_element(target_locator, timeout)
        self.actions.drag_and_drop(source, target).perform()
        self.logger.debug(f"Dragged element {source_locator} to {target_locator}")
    
    def scroll_to_element(self, locator, timeout=None):
        """Scroll to element"""
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # Small delay for scroll animation
        self.logger.debug(f"Scrolled to element: {locator}")
    
    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        self.logger.debug("Scrolled to bottom of page")
    
    def scroll_to_top(self):
        """Scroll to top of page"""
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        self.logger.debug("Scrolled to top of page")
    
    def select_dropdown_option(self, dropdown_locator, option_text, timeout=None):
        """Select option from dropdown by text"""
        from selenium.webdriver.support.ui import Select
        dropdown = self.find_element(dropdown_locator, timeout)
        select = Select(dropdown)
        select.select_by_visible_text(option_text)
        self.logger.debug(f"Selected '{option_text}' from dropdown: {dropdown_locator}")
    
    def select_dropdown_option_by_value(self, dropdown_locator, option_value, timeout=None):
        """Select option from dropdown by value"""
        from selenium.webdriver.support.ui import Select
        dropdown = self.find_element(dropdown_locator, timeout)
        select = Select(dropdown)
        select.select_by_value(option_value)
        self.logger.debug(f"Selected value '{option_value}' from dropdown: {dropdown_locator}")
    
    def get_selected_dropdown_option(self, dropdown_locator, timeout=None):
        """Get selected option from dropdown"""
        from selenium.webdriver.support.ui import Select
        dropdown = self.find_element(dropdown_locator, timeout)
        select = Select(dropdown)
        selected_option = select.first_selected_option
        return selected_option.text
    
    def get_dropdown_options(self, dropdown_locator, timeout=None):
        """Get all options from dropdown"""
        from selenium.webdriver.support.ui import Select
        dropdown = self.find_element(dropdown_locator, timeout)
        select = Select(dropdown)
        options = [option.text for option in select.options]
        return options
    
    def switch_to_frame(self, frame_locator, timeout=None):
        """Switch to iframe"""
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(EC.frame_to_be_available_and_switch_to_it(frame_locator))
        self.logger.debug(f"Switched to frame: {frame_locator}")
    
    def switch_to_default_content(self):
        """Switch back to default content"""
        self.driver.switch_to.default_content()
        self.logger.debug("Switched to default content")
    
    def switch_to_window(self, window_index=-1):
        """Switch to window by index (default: last window)"""
        self.driver.switch_to.window(self.driver.window_handles[window_index])
        self.logger.debug(f"Switched to window index: {window_index}")
    
    def close_current_window(self):
        """Close current window and switch to first window"""
        self.driver.close()
        if len(self.driver.window_handles) > 0:
            self.driver.switch_to.window(self.driver.window_handles[0])
        self.logger.debug("Closed current window and switched to first window")
    
    def accept_alert(self, timeout=None):
        """Accept alert dialog"""
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        alert = wait.until(EC.alert_is_present())
        alert.accept()
        self.logger.debug("Accepted alert")
    
    def dismiss_alert(self, timeout=None):
        """Dismiss alert dialog"""
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        alert = wait.until(EC.alert_is_present())
        alert.dismiss()
        self.logger.debug("Dismissed alert")
    
    def get_alert_text(self, timeout=None):
        """Get alert text"""
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        alert = wait.until(EC.alert_is_present())
        text = alert.text
        self.logger.debug(f"Got alert text: {text}")
        return text
    
    def send_keys_to_alert(self, text, timeout=None):
        """Send keys to alert prompt"""
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        alert = wait.until(EC.alert_is_present())
        alert.send_keys(text)
        self.logger.debug(f"Sent keys '{text}' to alert")
    
    def take_screenshot(self, filename):
        """Take screenshot and save to file"""
        self.driver.save_screenshot(filename)
        self.logger.info(f"Screenshot saved: {filename}")
    
    def get_current_url(self):
        """Get current URL"""
        url = self.driver.current_url
        self.logger.debug(f"Current URL: {url}")
        return url
    
    def get_page_title(self):
        """Get page title"""
        title = self.driver.title
        self.logger.debug(f"Page title: {title}")
        return title
    
    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
        self.logger.debug("Page refreshed")
    
    def navigate_to(self, url):
        """Navigate to URL"""
        self.driver.get(url)
        self.logger.info(f"Navigated to: {url}")
    
    def wait_for_url_change(self, expected_url_part, timeout=None):
        """Wait for URL to contain specific part"""
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(lambda d: expected_url_part in d.current_url)
        self.logger.debug(f"URL changed to contain: {expected_url_part}")
    
    def wait_for_page_load(self, timeout=None):
        """Wait for page to load completely"""
        wait_time = timeout if timeout else FrameworkConfig.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        self.logger.debug("Page loaded completely") 