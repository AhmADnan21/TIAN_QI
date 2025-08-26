from selenium.webdriver.common.by import By
from .base_page import BasePage
import time

class LoginPage(BasePage):
    """Page object for the login page"""
    
    # Locators
    PHONE_INPUT = (By.ID, "__BVID__23")
    PASSWORD_INPUT = (By.ID, "__BVID__24")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), '登录')]")
    ERROR_MESSAGE = (By.XPATH, "//div[contains(text(), '错误') or contains(text(), 'error') or contains(text(), '失败')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://test-ip-tianqi.cd.xiaoxigroup.net/login"
    
    def navigate_to_login(self):
        """Navigate to login page"""
        self.navigate_to(self.url)
        time.sleep(3)
        self.logger.info(f"Current URL: {self.get_current_url()}")
    
    def is_already_logged_in(self):
        """Check if user is already logged in"""
        current_url = self.get_current_url()
        return "/packageOrder" in current_url or current_url == "https://test-ip-tianqi.cd.xiaoxigroup.net/"
    
    def enter_phone_number(self, phone_number):
        """Enter phone number in the phone input field"""
        self.input_text(self.PHONE_INPUT, phone_number)
        self.logger.info(f"Entered phone number: {phone_number}")
    
    def enter_password(self, password):
        """Enter password in the password input field"""
        self.input_text(self.PASSWORD_INPUT, password)
        self.logger.info("Entered password")
    
    def click_login_button(self):
        """Click the login button"""
        self.click_element(self.LOGIN_BUTTON)
        self.logger.info("Clicked login button")
        time.sleep(5)
    
    def wait_for_login_success(self):
        """Wait for successful login redirect"""
        try:
            self.wait_for_url_change("/packageOrder", 10)
            current_url = self.get_current_url()
            if current_url == "https://test-ip-tianqi.cd.xiaoxigroup.net/":
                self.logger.info("✅ Successfully logged in - redirected to main page")
            else:
                self.logger.info("✅ Successfully logged in - redirected to package order page")
            return True
        except Exception as e:
            self.logger.error(f"Login redirect failed: {e}")
            return False
    
    def check_for_error_message(self):
        """Check for error messages after login attempt"""
        try:
            error_msg = self.find_element(self.ERROR_MESSAGE, 5)
            error_text = error_msg.text
            self.logger.error(f"Login failed: {error_text}")
            return error_text
        except:
            self.logger.error("No error message found, but login seems to have failed")
            return None
    
    def login_with_credentials(self, phone_number, password):
        """Complete login process with given credentials"""
        try:
            self.navigate_to_login()
            
            # Check if already logged in
            if self.is_already_logged_in():
                self.logger.info("Already logged in or redirected to main page")
                return True
            
            # Enter credentials
            self.enter_phone_number(phone_number)
            self.enter_password(password)
            self.click_login_button()
            
            # Check for success
            if self.wait_for_login_success():
                return True
            else:
                error_msg = self.check_for_error_message()
                if error_msg:
                    raise Exception(f"Login failed: {error_msg}")
                else:
                    raise Exception("Login failed - no redirect to expected page")
                    
        except Exception as e:
            self.logger.error(f"Login failed with error: {str(e)}")
            self.logger.error(f"Current page source: {self.driver.page_source[:1000]}...")
            raise