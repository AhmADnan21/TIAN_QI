"""
Test Framework
Main framework class for initialization and teardown
"""

import os
import sys
import logging
from pathlib import Path
from config.framework_config import FrameworkConfig
from config.browser_config import WebDriverManager
from helpers.element_helper import ElementHelper
from helpers.navigation_helper import NavigationHelper
from helpers.utility_helper import UtilityHelper
from test_reports.test_report import TestReport, TestCase, TestStep, track_step, create_test_case

class TestFramework:
    """Main framework class for test automation"""
    
    def __init__(self, browser_type=None, headless=None, environment="test"):
        self.browser_type = browser_type or FrameworkConfig.BROWSER_TYPE
        self.headless = headless if headless is not None else FrameworkConfig.HEADLESS
        self.environment = environment
        self.driver = None
        self.webdriver_manager = None
        self.element_helper = None
        self.navigation_helper = None
        self.utility_helper = None
        self.test_report = None
        self.logger = None
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(getattr(logging, FrameworkConfig.LOG_LEVEL))
        
        # Create console handler if not exists
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(getattr(logging, FrameworkConfig.LOG_LEVEL))
            
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            
            # Add handler to logger
            self.logger.addHandler(console_handler)
    
    def initialize(self):
        """Initialize the test framework"""
        try:
            self.logger.info("Initializing Test Framework...")
            
            # Create WebDriver
            self.webdriver_manager = WebDriverManager(self.browser_type, self.headless)
            self.driver = self.webdriver_manager.create_driver()
            
            # Initialize helpers
            self.element_helper = ElementHelper(self.driver)
            self.navigation_helper = NavigationHelper(self.driver, self.element_helper)
            self.utility_helper = UtilityHelper()
            
            # Create test report
            report_dir = self._create_report_directory()
            self.test_report = TestReport(report_dir)
            self.test_report.start()
            
            self.logger.info("Test Framework initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Test Framework: {str(e)}")
            return False
    
    def _create_report_directory(self):
        """Create report directory with timestamp"""
        timestamp = self.utility_helper.get_current_timestamp_string()
        report_dir = os.path.join(
            FrameworkConfig.get_report_dir(),
            f"Test_Execution_{timestamp}"
        )
        self.utility_helper.create_directory(report_dir)
        return report_dir
    
    def teardown(self):
        """Teardown the test framework"""
        try:
            self.logger.info("Tearing down Test Framework...")
            
            # Complete test report
            if self.test_report:
                self.test_report.complete()
                self.logger.info("Test report completed")
            
            # Quit WebDriver
            if self.webdriver_manager:
                self.webdriver_manager.quit_driver()
                self.logger.info("WebDriver quit successfully")
            
            self.logger.info("Test Framework torn down successfully")
            
        except Exception as e:
            self.logger.error(f"Error during teardown: {str(e)}")
    
    def get_driver(self):
        """Get WebDriver instance"""
        return self.driver
    
    def get_element_helper(self):
        """Get ElementHelper instance"""
        return self.element_helper
    
    def get_navigation_helper(self):
        """Get NavigationHelper instance"""
        return self.navigation_helper
    
    def get_utility_helper(self):
        """Get UtilityHelper instance"""
        return self.utility_helper
    
    def get_test_report(self):
        """Get TestReport instance"""
        return self.test_report
    
    def create_test_case(self, name, description):
        """Create a new test case"""
        return create_test_case(name, description)
    
    def add_test_case(self, test_case):
        """Add test case to report"""
        if self.test_report:
            self.test_report.add_test_case(test_case)
    
    def track_step(self, test_case, step_name, step_description):
        """Track a test step"""
        return track_step(test_case, step_name, step_description)
    
    def take_screenshot(self, filename=None):
        """Take screenshot"""
        if not filename:
            timestamp = self.utility_helper.get_current_timestamp_string()
            filename = f"screenshot_{timestamp}.png"
        
        screenshot_path = os.path.join(
            FrameworkConfig.get_screenshot_dir(),
            filename
        )
        
        if self.element_helper:
            self.element_helper.take_screenshot(screenshot_path)
        
        return screenshot_path
    
    def navigate_to_login_page(self):
        """Navigate to login page"""
        if self.navigation_helper:
            self.navigation_helper.navigate_to_login_page(self.environment)
    
    def navigate_to_package_order_page(self):
        """Navigate to package order page"""
        if self.navigation_helper:
            self.navigation_helper.navigate_to_package_order_page(self.environment)
    
    def navigate_to_personal_center_page(self):
        """Navigate to personal center page"""
        if self.navigation_helper:
            self.navigation_helper.navigate_to_personal_center_page(self.environment)
    
    def navigate_to_home_page(self):
        """Navigate to home page"""
        if self.navigation_helper:
            self.navigation_helper.navigate_to_home_page(self.environment)
    
    def wait_for_page_load(self, timeout=None):
        """Wait for page to load"""
        if self.navigation_helper:
            self.navigation_helper.wait_for_page_load(timeout)
    
    def get_current_url(self):
        """Get current URL"""
        if self.navigation_helper:
            return self.navigation_helper.get_current_url()
        return None
    
    def get_page_title(self):
        """Get page title"""
        if self.navigation_helper:
            return self.navigation_helper.get_page_title()
        return None
    
    def is_on_login_page(self):
        """Check if on login page"""
        if self.navigation_helper:
            return self.navigation_helper.is_on_login_page()
        return False
    
    def is_on_package_order_page(self):
        """Check if on package order page"""
        if self.navigation_helper:
            return self.navigation_helper.is_on_package_order_page()
        return False
    
    def is_on_personal_center_page(self):
        """Check if on personal center page"""
        if self.navigation_helper:
            return self.navigation_helper.is_on_personal_center_page()
        return False
    
    def is_on_home_page(self):
        """Check if on home page"""
        if self.navigation_helper:
            return self.navigation_helper.is_on_home_page()
        return False
    
    def switch_to_new_window(self):
        """Switch to new window"""
        if self.navigation_helper:
            return self.navigation_helper.switch_to_new_window()
        return False
    
    def switch_to_main_window(self):
        """Switch to main window"""
        if self.navigation_helper:
            return self.navigation_helper.switch_to_main_window()
        return False
    
    def close_all_windows_except_main(self):
        """Close all windows except main"""
        if self.navigation_helper:
            self.navigation_helper.close_all_windows_except_main()
    
    def accept_alert(self, timeout=None):
        """Accept alert"""
        if self.navigation_helper:
            self.navigation_helper.accept_alert(timeout)
    
    def dismiss_alert(self, timeout=None):
        """Dismiss alert"""
        if self.navigation_helper:
            self.navigation_helper.dismiss_alert(timeout)
    
    def get_alert_text(self, timeout=None):
        """Get alert text"""
        if self.navigation_helper:
            return self.navigation_helper.get_alert_text(timeout)
        return None
    
    def generate_html_report(self):
        """Generate HTML report"""
        if self.test_report:
            return self.test_report.generate_html_report()
        return None
    
    def get_test_summary(self):
        """Get test summary"""
        if self.test_report:
            return self.test_report.get_summary()
        return None
    
    def __enter__(self):
        """Context manager entry"""
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.teardown()
    
    def run_test(self, test_function, *args, **kwargs):
        """Run a test function with framework setup"""
        try:
            # Initialize framework if not already done
            if not self.driver:
                if not self.initialize():
                    raise Exception("Failed to initialize framework")
            
            # Run the test function
            result = test_function(self, *args, **kwargs)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Test execution failed: {str(e)}")
            # Take screenshot on failure
            self.take_screenshot(f"failure_{self.utility_helper.get_current_timestamp_string()}.png")
            raise
    
    def run_test_suite(self, test_functions):
        """Run multiple test functions"""
        results = {}
        
        for test_name, test_function in test_functions.items():
            try:
                self.logger.info(f"Running test: {test_name}")
                result = self.run_test(test_function)
                results[test_name] = {"status": "PASSED", "result": result}
                self.logger.info(f"Test {test_name} completed successfully")
                
            except Exception as e:
                results[test_name] = {"status": "FAILED", "error": str(e)}
                self.logger.error(f"Test {test_name} failed: {str(e)}")
        
        return results 