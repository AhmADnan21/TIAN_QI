# Automation Framework Guide

## Overview

This document provides a comprehensive guide to the new automation framework structure. The framework has been redesigned to be clean, scalable, and consistent across the project.

## Framework Structure

```
Framework Page Object Model (POM)/
├── config/                          # Configuration files
│   ├── framework_config.py          # Browser settings, timeouts, reports
│   ├── browser_config.py            # WebDriverManager and browser options
│   ├── test_data_config.py          # App URLs and test data
│   └── credentials_config.py        # User accounts by type
├── locators/                        # Element locators
│   └── element_locators.py          # Structured locators by page
├── mappings/                        # Dropdown mappings
│   └── dropdown_mappings.py         # Package, country, language mappings
├── helpers/                         # Core helper classes
│   ├── element_helper.py            # Enhanced element interactions
│   ├── navigation_helper.py         # Navigation and page management
│   └── utility_helper.py            # Utility methods
├── core/                            # Main framework class
│   └── test_framework.py            # TestFramework for initialization
├── actions/                         # Common test actions
│   └── common_actions.py            # Reusable actions (login, logout, etc.)
├── execution/                       # Test execution manager
│   └── test_execution_manager.py    # Execution logic for tests and suites
├── test_reports/                    # Test reporting
│   └── test_report.py               # TestStep, TestCase, TestReport classes
├── main.py                          # Main execution script
└── FRAMEWORK_GUIDE.md               # This guide
```

## Framework Configuration

### Framework Config (`config/framework_config.py`)

Contains all framework settings:

```python
class FrameworkConfig:
    # Browser Settings
    BROWSER_TYPE = "chrome"
    HEADLESS = False
    WINDOW_SIZE = (1920, 1080)
    
    # Timeout Settings
    DEFAULT_TIMEOUT = 20
    IMPLICIT_WAIT = 10
    
    # Report Settings
    REPORT_DIR = "reports"
    SCREENSHOT_ON_FAILURE = True
```

### Browser Config (`config/browser_config.py`)

Manages WebDriver creation and configuration:

```python
class WebDriverManager:
    def create_driver(self):
        # Creates and configures WebDriver instance
        pass
```

### Test Data Config (`config/test_data_config.py`)

Contains application URLs and test data:

```python
class AppURLs:
    TEST_ENV = "https://test-ip-tianqi.cd.xiaoxigroup.net"
    
class TestData:
    ACCOUNT_WITH_BALANCE = {
        "phone": "15332595364",
        "password": "Test@123"
    }
```

### Credentials Config (`config/credentials_config.py`)

Organizes user accounts by type:

```python
class UserCredentials:
    USERS_WITH_BALANCE = {
        "user_with_balance_1": {
            "phone": "15332595364",
            "password": "Test@123"
        }
    }
```

## Element Locators

### Element Locators (`locators/element_locators.py`)

Structured locators organized by page:

```python
class LoginPageLocators:
    PHONE_INPUT = (By.ID, "__BVID__23")
    PASSWORD_INPUT = (By.ID, "__BVID__24")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), '登录')]")

class PackageOrderPageLocators:
    DYNAMIC_SUPREME_PACKAGE = (By.XPATH, "//div[contains(text(), '天启动态尊享')]")
    BUY_NOW_BUTTON = (By.XPATH, "//div[contains(text(), '立即购买')]")
```

## Dropdown Mappings

### Dropdown Mappings (`mappings/dropdown_mappings.py`)

Mappings for package, country, language, and payment selections:

```python
class PackageMappings:
    PACKAGE_NAME_TO_VALUE = {
        "天启动态尊享": "70",
        "静态IP-天启": "64"
    }

class PaymentMappings:
    PAYMENT_NAME_TO_VALUE = {
        "余额": "balance",
        "支付宝": "alipay"
    }
```

## Core Helper Classes

### Element Helper (`helpers/element_helper.py`)

Enhanced element interaction methods:

```python
class ElementHelper:
    def find_element(self, locator, timeout=None):
        # Find element with explicit wait
        pass
    
    def click_element(self, locator, timeout=None, use_js=False):
        # Click element with JavaScript fallback
        pass
    
    def input_text(self, locator, text, timeout=None):
        # Input text into element
        pass
```

### Navigation Helper (`helpers/navigation_helper.py`)

Navigation and page management:

```python
class NavigationHelper:
    def navigate_to_login_page(self, environment="test"):
        # Navigate to login page
        pass
    
    def switch_to_new_window(self):
        # Switch to newly opened window
        pass
```

### Utility Helper (`helpers/utility_helper.py`)

Utility methods for common operations:

```python
class UtilityHelper:
    @staticmethod
    def generate_random_string(length=8):
        # Generate random alphanumeric string
        pass
    
    @staticmethod
    def wait(seconds):
        # Wait for specified number of seconds
        pass
```

## Main Framework Class

### Test Framework (`core/test_framework.py`)

Main framework class for initialization and teardown:

```python
class TestFramework:
    def __init__(self, browser_type=None, headless=None, environment="test"):
        # Initialize framework
        pass
    
    def initialize(self):
        # Initialize WebDriver and helpers
        pass
    
    def teardown(self):
        # Cleanup resources
        pass
```

## Common Test Actions

### Common Actions (`actions/common_actions.py`)

Reusable test actions:

```python
class CommonActions:
    def login_with_balance(self, test_case=None):
        # Login with account that has balance
        pass
    
    def select_package(self, package_name, test_case=None):
        # Select package by name
        pass
    
    def select_payment_method(self, payment_method, test_case=None):
        # Select payment method
        pass
```

## Test Execution Manager

### Test Execution Manager (`execution/test_execution_manager.py`)

Manages test execution for single tests and full suites:

```python
class TestExecutionManager:
    def run_single_test(self, test_function, test_name, test_description):
        # Run a single test
        pass
    
    def run_test_suite(self, test_suite):
        # Run a complete test suite
        pass
    
    def run_complete_test_suite(self):
        # Run all test scenarios
        pass
```

## Test Report Classes

### Test Report (`test_reports/test_report.py`)

Test reporting and tracking:

```python
class TestStep:
    # Represents a single test step
    pass

class TestCase:
    # Represents a complete test case
    pass

class TestReport:
    # Manages test reporting
    pass
```

## Team Implementation Steps

### 1. Setup

1. **Install Dependencies**:
   ```bash
   pip install selenium webdriver-manager pytest
   ```

2. **Clone/Setup Framework**:
   - Ensure all framework files are in place
   - Verify configuration files are properly set

### 2. Configure

1. **Update Configuration**:
   - Modify `config/framework_config.py` for your environment
   - Update `config/test_data_config.py` with your app URLs
   - Configure `config/credentials_config.py` with test accounts

2. **Update Locators**:
   - Review and update `locators/element_locators.py` if needed
   - Ensure all element locators are current

### 3. Write Test Functions

Create test functions following this pattern:

```python
def test_example(framework, actions, test_case):
    try:
        # Login
        actions.login_with_balance(test_case)
        
        # Navigate
        actions.navigate_to_package_order_page()
        
        # Select package
        actions.select_package(PackageData.DYNAMIC_SUPREME, test_case)
        
        # Perform actions
        actions.click_buy_now(test_case)
        
        # Verify results
        with framework.track_step(test_case, "Verify", "Check success"):
            # Verification logic
            pass
        
        return True
        
    except Exception as e:
        framework.logger.error(f"Test failed: {str(e)}")
        return False
```

### 4. Add to Test Suite

Add your test to a test suite:

```python
test_suite = {
    "test_name": {
        "name": "Test Display Name",
        "description": "Test description",
        "function": test_example
    }
}
```

### 5. Run Tests

Use the TestExecutionManager to run tests:

```python
with TestExecutionManager() as manager:
    results = manager.run_test_suite(test_suite)
    report_file = manager.generate_final_report()
```

## Usage Examples

### Single Test Execution

```python
from execution.test_execution_manager import TestExecutionManager

def my_test_function(framework, actions, test_case):
    # Your test logic here
    pass

with TestExecutionManager() as manager:
    result = manager.run_single_test(
        my_test_function,
        "My Test Name",
        "My test description"
    )
```

### Package Payment Tests

```python
from execution.test_execution_manager import TestExecutionManager
from config.test_data_config import PackageData, PaymentData

with TestExecutionManager() as manager:
    results = manager.run_package_payment_tests(
        PackageData.DYNAMIC_SUPREME,
        [PaymentData.BALANCE_PAYMENT, PaymentData.ALIPAY_PAYMENT]
    )
```

### Complete Test Suite

```python
from execution.test_execution_manager import TestExecutionManager

with TestExecutionManager() as manager:
    complete_results = manager.run_complete_test_suite()
    report_file = manager.generate_final_report()
```

## Maintenance Guidelines

### Handling Locator Changes

1. **Update Locators**: Modify `locators/element_locators.py`
2. **Test Locators**: Run a simple test to verify
3. **Update Documentation**: Update this guide if needed

### Environment Updates

1. **Update URLs**: Modify `config/test_data_config.py`
2. **Update Credentials**: Modify `config/credentials_config.py`
3. **Test Configuration**: Run tests to verify changes

### Adding New Tests

1. **Create Test Function**: Follow the pattern shown above
2. **Add to Suite**: Include in appropriate test suite
3. **Update Documentation**: Document new test scenarios

### Adding New Pages

1. **Add Locators**: Create new locator class in `element_locators.py`
2. **Add Actions**: Create new action methods in `common_actions.py`
3. **Add Navigation**: Add navigation methods in `navigation_helper.py`
4. **Update Documentation**: Document new page functionality

## Best Practices

### 1. Use Test Cases and Steps

Always use test cases and steps for proper reporting:

```python
def test_function(framework, actions, test_case):
    with framework.track_step(test_case, "Step Name", "Step Description"):
        # Step logic here
        pass
```

### 2. Handle Exceptions Properly

Always handle exceptions and return appropriate results:

```python
try:
    # Test logic
    return True
except Exception as e:
    framework.logger.error(f"Test failed: {str(e)}")
    return False
```

### 3. Use Configuration

Use configuration files instead of hardcoding values:

```python
# Good
from config.test_data_config import PackageData
actions.select_package(PackageData.DYNAMIC_SUPREME, test_case)

# Bad
actions.select_package("天启动态尊享", test_case)
```

### 4. Use Helper Methods

Use the provided helper methods instead of direct WebDriver calls:

```python
# Good
actions.element_helper.click_element(locator)

# Bad
driver.find_element(*locator).click()
```

### 5. Generate Reports

Always generate reports for test execution:

```python
report_file = manager.generate_final_report()
print(f"Report generated: {report_file}")
```

## Troubleshooting

### Common Issues

1. **Element Not Found**: Check locators in `element_locators.py`
2. **Login Failures**: Verify credentials in `credentials_config.py`
3. **Browser Issues**: Check browser configuration in `browser_config.py`
4. **Timeout Issues**: Adjust timeouts in `framework_config.py`

### Debug Mode

Enable debug logging:

```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

### Screenshots

Take screenshots on failures:

```python
screenshot_path = framework.take_screenshot("failure.png")
```

## Conclusion

This framework provides a clean, scalable, and maintainable approach to test automation. By following the structure and guidelines outlined in this document, teams can easily contribute to and maintain the automation suite.

For questions or issues, refer to the code comments and this documentation. The framework is designed to be self-documenting and easy to understand. 