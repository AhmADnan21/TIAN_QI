"""
Framework Configuration
Contains browser settings, timeouts, and report configurations
"""

import os
from pathlib import Path

# ===== Framework Configuration =====
class FrameworkConfig:
    """Framework configuration settings"""
    
    # Browser Settings
    BROWSER_TYPE = "chrome"  # chrome, firefox, edge
    HEADLESS = False
    WINDOW_SIZE = (1920, 1080)
    MAXIMIZE_WINDOW = True
    
    # Timeout Settings
    DEFAULT_TIMEOUT = 20
    IMPLICIT_WAIT = 10
    PAGE_LOAD_TIMEOUT = 30
    SCRIPT_TIMEOUT = 30
    
    # Report Settings
    REPORT_DIR = "reports"
    SCREENSHOT_ON_FAILURE = True
    SCREENSHOT_DIR = "screenshots"
    LOG_LEVEL = "INFO"
    
    # Test Execution Settings
    RETRY_FAILED_TESTS = 1
    PARALLEL_EXECUTION = False
    MAX_WORKERS = 1
    
    # Wait Settings
    POLLING_FREQUENCY = 0.5
    IGNORED_EXCEPTIONS = []
    
    @classmethod
    def get_report_dir(cls):
        """Get the report directory path"""
        base_dir = Path(__file__).parent.parent.parent
        report_path = base_dir / cls.REPORT_DIR
        report_path.mkdir(exist_ok=True)
        return str(report_path)
    
    @classmethod
    def get_screenshot_dir(cls):
        """Get the screenshot directory path"""
        base_dir = Path(__file__).parent.parent.parent
        screenshot_path = base_dir / cls.SCREENSHOT_DIR
        screenshot_path.mkdir(exist_ok=True)
        return str(screenshot_path) 