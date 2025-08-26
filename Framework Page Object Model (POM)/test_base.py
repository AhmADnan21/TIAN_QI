import os
import sys
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_reports.test_report import TestReport, TestCase, TestStep, track_step, create_test_case

class TestBase:
    """Base class for all test classes"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.test_report = None
        self.report_dir = None
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('test_execution.log')
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self):
        """Setup WebDriver instance"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20) # type: ignore
        self.logger.info("WebDriver setup completed")
    
    def create_report_directory(self):
        """Create a unique report directory with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.report_dir = os.path.join(base_dir, "reports", f"POM_website_Payment_Tests_{timestamp}")
        os.makedirs(self.report_dir, exist_ok=True)
        self.logger.info(f"Report directory created: {self.report_dir}")
        return self.report_dir
    
    def setup_test_report(self):
        """Setup test report instance"""
        if not self.report_dir:
            self.create_report_directory()
        self.test_report = TestReport(self.report_dir)
        self.test_report.start()
        self.logger.info("Test report setup completed")
    
    def teardown_driver(self):
        """Cleanup WebDriver instance"""
        if self.driver:
            self.driver.quit()
            self.logger.info("WebDriver cleanup completed")
    
    def teardown_test_report(self):
        """Complete test report"""
        if self.test_report:
            self.test_report.complete()
            report_file = self.test_report.generate_html_report()
            self.logger.info(f"Test report completed: {report_file}")
    
    def setup(self):
        """Setup test environment"""
        self.setup_driver()
        self.setup_test_report()
    
    def teardown(self):
        """Teardown test environment"""
        self.teardown_test_report()
        self.teardown_driver()
    
    def run_test_with_reporting(self, test_name, test_description, test_function, *args, **kwargs):
        """Run a test with proper reporting"""
        test_case = create_test_case(test_name, test_description)
        test_case.start()
        
        try:
            result = test_function(*args, **kwargs)
            if result:
                test_case.complete()
                self.logger.info(f"✅ Test passed: {test_name}")
            else:
                test_case.fail("Test returned False")
                self.logger.error(f"❌ Test failed: {test_name}")
            return result
        except Exception as e:
            test_case.fail(f"Test failed with exception: {str(e)}")
            self.logger.error(f"❌ Test failed with exception: {test_name} - {str(e)}")
            return False
        finally:
            if self.test_report:
                self.test_report.add_test_case(test_case)
    
    def take_screenshot(self, filename):
        """Take screenshot and save to report directory"""
        if self.driver and self.report_dir:
            screenshot_path = os.path.join(self.report_dir, filename)
            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        return None
    
    def log_test_step(self, step_name, step_description):
        """Log a test step for reporting"""
        self.logger.info(f"Step: {step_name} - {step_description}")
    
    def assert_element_present(self, locator, timeout=10):
        """Assert that element is present"""
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except Exception as e:
            self.logger.error(f"Element not present: {locator} - {str(e)}")
            return False
    
    def assert_element_visible(self, locator, timeout=10):
        """Assert that element is visible"""
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception as e:
            self.logger.error(f"Element not visible: {locator} - {str(e)}")
            return False
    
    def assert_text_present(self, locator, expected_text, timeout=10):
        """Assert that element contains expected text"""
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator))
            actual_text = element.text
            assert expected_text in actual_text, f"Expected '{expected_text}' in '{actual_text}'"
            return True
        except Exception as e:
            self.logger.error(f"Text assertion failed: {locator} - {str(e)}")
            return False
    
    def assert_url_contains(self, expected_url_part, timeout=10):
        """Assert that current URL contains expected part"""
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            wait = WebDriverWait(self.driver, timeout)
            wait.until(lambda d: expected_url_part in d.current_url)
            return True
        except Exception as e:
            self.logger.error(f"URL assertion failed: expected '{expected_url_part}' - {str(e)}")
            return False 