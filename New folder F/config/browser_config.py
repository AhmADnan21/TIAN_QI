"""
Browser Configuration
WebDriverManager class setup and browser options
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.framework_config import FrameworkConfig
import logging

class WebDriverManager:
    """Manages WebDriver creation and configuration"""
    
    def __init__(self, browser_type=None, headless=None):
        self.browser_type = browser_type or FrameworkConfig.BROWSER_TYPE
        self.headless = headless if headless is not None else FrameworkConfig.HEADLESS
        self.driver = None
        self.logger = logging.getLogger(__name__)
    
    def create_driver(self):
        """Create and configure WebDriver instance"""
        try:
            if self.browser_type.lower() == "chrome":
                self.driver = self._create_chrome_driver()
            elif self.browser_type.lower() == "firefox":
                self.driver = self._create_firefox_driver()
            elif self.browser_type.lower() == "edge":
                self.driver = self._create_edge_driver()
            else:
                raise ValueError(f"Unsupported browser type: {self.browser_type}")
            
            self._configure_driver()
            self.logger.info(f"Successfully created {self.browser_type} WebDriver")
            return self.driver
            
        except Exception as e:
            self.logger.error(f"Failed to create WebDriver: {str(e)}")
            raise
    
    def _create_chrome_driver(self):
        """Create Chrome WebDriver"""
        options = ChromeOptions()
        
        if self.headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def _create_firefox_driver(self):
        """Create Firefox WebDriver"""
        options = FirefoxOptions()
        
        if self.headless:
            options.add_argument("--headless")
        
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        return driver
    
    def _create_edge_driver(self):
        """Create Edge WebDriver"""
        options = EdgeOptions()
        
        if self.headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
        return driver
    
    def _configure_driver(self):
        """Configure WebDriver settings"""
        if FrameworkConfig.MAXIMIZE_WINDOW:
            self.driver.maximize_window()
        else:
            self.driver.set_window_size(*FrameworkConfig.WINDOW_SIZE)
        
        self.driver.implicitly_wait(FrameworkConfig.IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(FrameworkConfig.PAGE_LOAD_TIMEOUT)
        self.driver.set_script_timeout(FrameworkConfig.SCRIPT_TIMEOUT)
    
    def quit_driver(self):
        """Quit WebDriver instance"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("WebDriver quit successfully")
            except Exception as e:
                self.logger.warning(f"Error quitting WebDriver: {str(e)}")
            finally:
                self.driver = None
    
    def get_driver(self):
        """Get current WebDriver instance"""
        return self.driver 