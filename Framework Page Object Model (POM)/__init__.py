"""
Website Payment Tests - Page Object Model (POM) Framework

This package provides a complete Page Object Model implementation for website payment testing,
offering better maintainability, reusability, and separation of concerns compared to traditional approaches.

Modules:
    - base_page: Base page class with common functionality
    - login_page: Login page object
    - package_order_page: Package order page object
    - personal_center_page: Personal center page object
    - test_base: Base test class with setup/teardown
    - website_payment_tests_pom: Main test script using POM
"""

__version__ = "1.0.0"
__author__ = "Test Automation Team"
__description__ = "Page Object Model implementation for Website Payment Tests"

# Import main classes for easy access
from .base_page import BasePage
from .login_page import LoginPage
from .package_order_page import PackageOrderPage
from .personal_center_page import PersonalCenterPage
from .test_base import TestBase
from .website_payment_tests_pom import WebsitePaymentTestsPOM

__all__ = [
    'BasePage',
    'LoginPage', 
    'PackageOrderPage',
    'PersonalCenterPage',
    'TestBase',
    'WebsitePaymentTestsPOM'
] 