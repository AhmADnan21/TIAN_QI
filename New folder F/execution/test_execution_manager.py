"""
Test Execution Manager
Execution logic for single tests and full suites
"""

import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path
from core.test_framework import TestFramework
from actions.common_actions import CommonActions
from config.test_data_config import PackageData, PaymentData
from config.credentials_config import UserCredentials

class TestExecutionManager:
    """Manages test execution for single tests and full suites"""
    
    def __init__(self, browser_type=None, headless=None, environment="test"):
        self.browser_type = browser_type
        self.headless = headless
        self.environment = environment
        self.framework = None
        self.actions = None
        self.logger = logging.getLogger(__name__)
    
    def initialize_framework(self):
        """Initialize the test framework"""
        try:
            self.framework = TestFramework(self.browser_type, self.headless, self.environment)
            if self.framework.initialize():
                self.actions = CommonActions(self.framework)
                self.logger.info("Test Execution Manager initialized successfully")
                return True
            else:
                self.logger.error("Failed to initialize framework")
                return False
        except Exception as e:
            self.logger.error(f"Failed to initialize Test Execution Manager: {str(e)}")
            return False
    
    def teardown_framework(self):
        """Teardown the test framework"""
        if self.framework:
            self.framework.teardown()
            self.logger.info("Test Execution Manager torn down successfully")
    
    def run_single_test(self, test_function, test_name, test_description):
        """Run a single test"""
        try:
            self.logger.info(f"Starting single test: {test_name}")
            
            # Create test case
            test_case = self.framework.create_test_case(test_name, test_description)
            test_case.start()
            
            # Run the test
            result = test_function(self.framework, self.actions, test_case)
            
            # Complete test case
            test_case.complete(success=result)
            
            # Add to report
            self.framework.add_test_case(test_case)
            
            self.logger.info(f"Single test completed: {test_name} - {'PASSED' if result else 'FAILED'}")
            return result
            
        except Exception as e:
            self.logger.error(f"Single test failed: {test_name} - {str(e)}")
            if test_case:
                test_case.complete(success=False, error_message=str(e))
                self.framework.add_test_case(test_case)
            return False
    
    def run_test_suite(self, test_suite):
        """Run a complete test suite"""
        try:
            self.logger.info(f"Starting test suite with {len(test_suite)} tests")
            
            results = {}
            passed_count = 0
            failed_count = 0
            
            for test_name, test_config in test_suite.items():
                try:
                    self.logger.info(f"Running test: {test_name}")
                    
                    # Create test case
                    test_case = self.framework.create_test_case(
                        test_config.get("name", test_name),
                        test_config.get("description", f"Test: {test_name}")
                    )
                    test_case.start()
                    
                    # Run the test function
                    test_function = test_config["function"]
                    result = test_function(self.framework, self.actions, test_case)
                    
                    # Complete test case
                    test_case.complete(success=result)
                    
                    # Add to report
                    self.framework.add_test_case(test_case)
                    
                    # Track results
                    results[test_name] = {
                        "status": "PASSED" if result else "FAILED",
                        "test_case": test_case
                    }
                    
                    if result:
                        passed_count += 1
                        self.logger.info(f"✅ Test passed: {test_name}")
                    else:
                        failed_count += 1
                        self.logger.error(f"❌ Test failed: {test_name}")
                    
                except Exception as e:
                    failed_count += 1
                    self.logger.error(f"❌ Test failed with exception: {test_name} - {str(e)}")
                    
                    if test_case:
                        test_case.complete(success=False, error_message=str(e))
                        self.framework.add_test_case(test_case)
                    
                    results[test_name] = {
                        "status": "FAILED",
                        "error": str(e),
                        "test_case": test_case
                    }
            
            # Generate summary
            total_tests = len(test_suite)
            success_rate = (passed_count / total_tests) * 100 if total_tests > 0 else 0
            
            self.logger.info(f"Test suite completed:")
            self.logger.info(f"  Total tests: {total_tests}")
            self.logger.info(f"  Passed: {passed_count}")
            self.logger.info(f"  Failed: {failed_count}")
            self.logger.info(f"  Success rate: {success_rate:.1f}%")
            
            return {
                "results": results,
                "summary": {
                    "total": total_tests,
                    "passed": passed_count,
                    "failed": failed_count,
                    "success_rate": success_rate
                }
            }
            
        except Exception as e:
            self.logger.error(f"Test suite execution failed: {str(e)}")
            return {
                "results": {},
                "summary": {
                    "total": 0,
                    "passed": 0,
                    "failed": 0,
                    "success_rate": 0
                },
                "error": str(e)
            }
    
    def run_package_payment_tests(self, package_name, payment_methods=None):
        """Run payment tests for a specific package"""
        if payment_methods is None:
            payment_methods = [PaymentData.BALANCE_PAYMENT, PaymentData.ALIPAY_PAYMENT, PaymentData.WECHAT_PAYMENT]
        
        test_suite = {}
        
        for payment_method in payment_methods:
            test_name = f"{package_name}_{payment_method}_payment"
            test_suite[test_name] = {
                "name": f"{package_name} - {payment_method} Payment",
                "description": f"Test {payment_method} payment for {package_name} package",
                "function": self._create_package_payment_test(package_name, payment_method)
            }
        
        return self.run_test_suite(test_suite)
    
    def run_all_package_payment_tests(self):
        """Run payment tests for all packages"""
        packages = [
            PackageData.DYNAMIC_SUPREME,
            PackageData.STATIC_IP,
            PackageData.DYNAMIC_STANDARD,
            PackageData.DYNAMIC_DEDICATED
        ]
        
        payment_methods = [PaymentData.BALANCE_PAYMENT, PaymentData.ALIPAY_PAYMENT, PaymentData.WECHAT_PAYMENT]
        
        all_results = {}
        
        for package in packages:
            self.logger.info(f"Running payment tests for package: {package}")
            results = self.run_package_payment_tests(package, payment_methods)
            all_results[package] = results
        
        return all_results
    
    def run_personal_center_tests(self, package_name, payment_methods=None):
        """Run personal center tests for a specific package"""
        if payment_methods is None:
            payment_methods = [PaymentData.BALANCE_PAYMENT, PaymentData.ALIPAY_PAYMENT, PaymentData.WECHAT_PAYMENT]
        
        test_suite = {}
        
        for payment_method in payment_methods:
            test_name = f"personal_{package_name}_{payment_method}_payment"
            test_suite[test_name] = {
                "name": f"Personal Center - {package_name} - {payment_method} Payment",
                "description": f"Test {payment_method} payment for {package_name} in Personal Center",
                "function": self._create_personal_center_test(package_name, payment_method)
            }
        
        return self.run_test_suite(test_suite)
    
    def run_all_personal_center_tests(self):
        """Run personal center tests for all packages"""
        packages = [
            PackageData.DYNAMIC_SUPREME,
            PackageData.STATIC_IP,
            PackageData.DYNAMIC_STANDARD,
            PackageData.DYNAMIC_DEDICATED
        ]
        
        payment_methods = [PaymentData.BALANCE_PAYMENT, PaymentData.ALIPAY_PAYMENT, PaymentData.WECHAT_PAYMENT]
        
        all_results = {}
        
        for package in packages:
            self.logger.info(f"Running personal center tests for package: {package}")
            results = self.run_personal_center_tests(package, payment_methods)
            all_results[package] = results
        
        return all_results
    
    def run_no_balance_tests(self):
        """Run tests for scenarios with no balance"""
        packages = [
            PackageData.DYNAMIC_SUPREME,
            PackageData.STATIC_IP,
            PackageData.DYNAMIC_STANDARD,
            PackageData.DYNAMIC_DEDICATED
        ]
        
        test_suite = {}
        
        # Package order no balance tests
        for package in packages:
            test_name = f"no_balance_{package}_package_order"
            test_suite[test_name] = {
                "name": f"No Balance - {package} - Package Order",
                "description": f"Test no balance scenario for {package} on package order page",
                "function": self._create_no_balance_package_order_test(package)
            }
        
        # Personal center no balance tests
        for package in packages:
            test_name = f"no_balance_{package}_personal_center"
            test_suite[test_name] = {
                "name": f"No Balance - {package} - Personal Center",
                "description": f"Test no balance scenario for {package} in personal center",
                "function": self._create_no_balance_personal_center_test(package)
            }
        
        return self.run_test_suite(test_suite)
    
    def run_complete_test_suite(self):
        """Run the complete test suite including all scenarios"""
        self.logger.info("Starting complete test suite execution")
        
        complete_results = {}
        
        # 1. Package Order Payment Tests (with balance)
        self.logger.info("=== Running Package Order Payment Tests ===")
        complete_results["package_order_tests"] = self.run_all_package_payment_tests()
        
        # 2. Personal Center Tests (with balance)
        self.logger.info("=== Running Personal Center Tests ===")
        complete_results["personal_center_tests"] = self.run_all_personal_center_tests()
        
        # 3. No Balance Tests
        self.logger.info("=== Running No Balance Tests ===")
        complete_results["no_balance_tests"] = self.run_no_balance_tests()
        
        # Generate overall summary
        overall_summary = self._generate_overall_summary(complete_results)
        complete_results["overall_summary"] = overall_summary
        
        self.logger.info("Complete test suite execution finished")
        return complete_results
    
    def _create_package_payment_test(self, package_name, payment_method):
        """Create a package payment test function"""
        def test_function(framework, actions, test_case):
            try:
                # Login with balance
                actions.login_with_balance(test_case)
                
                # Select package
                actions.select_package(package_name, test_case)
                
                # Click buy now
                actions.click_buy_now(test_case)
                
                # Select payment method
                actions.select_payment_method(payment_method, test_case)
                
                # Click pay now
                actions.click_pay_now(test_case)
                
                # Handle different payment methods
                if payment_method == PaymentData.BALANCE_PAYMENT:
                    # Verify success popup
                    with framework.track_step(test_case, "Verify Success", "Check purchase success message"):
                        success_msg = actions.element_helper.find_visible_element(
                            PackageOrderPageLocators.SUCCESS_POPUP
                        )
                        assert ErrorMessages.PAYMENT_SUCCESS in success_msg.text
                        
                        # Close success popup
                        with framework.track_step(test_case, "Close Success Popup", "Close the success popup"):
                            actions.element_helper.click_element(
                                PackageOrderPageLocators.SUCCESS_POPUP_CLOSE, use_js=True
                            )
                            actions.utility_helper.wait(1)
                
                elif payment_method == PaymentData.ALIPAY_PAYMENT:
                    # Verify Alipay sandbox
                    actions.verify_alipay_sandbox(test_case)
                    # Switch back to main window
                    actions.navigation_helper.switch_to_main_window()
                
                elif payment_method == PaymentData.WECHAT_PAYMENT:
                    # Verify WeChat QR
                    actions.verify_wechat_qr(test_case)
                    # Close WeChat popup
                    actions.close_wechat_popup(test_case)
                
                return True
                
            except Exception as e:
                framework.logger.error(f"Package payment test failed: {str(e)}")
                return False
        
        return test_function
    
    def _create_personal_center_test(self, package_name, payment_method):
        """Create a personal center test function"""
        def test_function(framework, actions, test_case):
            try:
                # Navigate to personal center
                actions.navigate_to_personal_center(test_case)
                
                # Click add paid account
                actions.click_add_paid_account(test_case)
                
                # Wait for popup
                actions.wait_for_package_popup(test_case)
                
                # Select package type
                actions.select_package_type_personal(package_name, test_case, has_balance=True)
                
                # Input random account
                actions.input_random_account(test_case, has_balance=True)
                
                # Select payment method
                actions.select_payment_method_personal(payment_method, test_case)
                
                # Click pay
                actions.click_pay_personal(test_case)
                
                # Handle different payment methods
                if payment_method == PaymentData.BALANCE_PAYMENT:
                    # Verify success message
                    actions.verify_success_message(test_case)
                
                elif payment_method == PaymentData.ALIPAY_PAYMENT:
                    # Verify Alipay sandbox
                    actions.verify_alipay_sandbox(test_case)
                    # Switch back to main window
                    actions.navigation_helper.switch_to_main_window()
                
                elif payment_method == PaymentData.WECHAT_PAYMENT:
                    # Close WeChat popup
                    actions.close_wechat_popup(test_case)
                
                return True
                
            except Exception as e:
                framework.logger.error(f"Personal center test failed: {str(e)}")
                return False
        
        return test_function
    
    def _create_no_balance_package_order_test(self, package_name):
        """Create a no balance package order test function"""
        def test_function(framework, actions, test_case):
            try:
                # Login without balance
                actions.login_without_balance(test_case)
                
                # Select package
                actions.select_package(package_name, test_case)
                
                # Click buy now
                actions.click_buy_now(test_case)
                
                # Select balance payment (should fail)
                actions.select_payment_method(PaymentData.BALANCE_PAYMENT, test_case)
                
                # Click recharge now
                actions.click_recharge_now(test_case)
                
                # Verify recharge redirect
                actions.verify_recharge_redirect(test_case)
                
                return True
                
            except Exception as e:
                framework.logger.error(f"No balance package order test failed: {str(e)}")
                return False
        
        return test_function
    
    def _create_no_balance_personal_center_test(self, package_name):
        """Create a no balance personal center test function"""
        def test_function(framework, actions, test_case):
            try:
                # Navigate to personal center
                actions.navigate_to_personal_center(test_case)
                
                # Click add paid account
                actions.click_add_paid_account(test_case)
                
                # Wait for popup
                actions.wait_for_package_popup(test_case)
                
                # Select package type (no balance)
                actions.select_package_type_personal(package_name, test_case, has_balance=False)
                
                # Input random account
                actions.input_random_account(test_case, has_balance=False)
                
                # Select balance payment (should fail)
                actions.select_payment_method_personal(PaymentData.BALANCE_PAYMENT, test_case)
                
                # Click pay
                actions.click_pay_personal(test_case)
                
                # Verify insufficient balance error
                actions.verify_insufficient_balance_error(test_case)
                
                return True
                
            except Exception as e:
                framework.logger.error(f"No balance personal center test failed: {str(e)}")
                return False
        
        return test_function
    
    def _generate_overall_summary(self, complete_results):
        """Generate overall summary from all test results"""
        total_tests = 0
        total_passed = 0
        total_failed = 0
        
        for category, results in complete_results.items():
            if "summary" in results:
                summary = results["summary"]
                total_tests += summary.get("total", 0)
                total_passed += summary.get("passed", 0)
                total_failed += summary.get("failed", 0)
        
        success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
        
        return {
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "success_rate": success_rate,
            "execution_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def generate_final_report(self):
        """Generate final HTML report"""
        if self.framework and self.framework.test_report:
            return self.framework.generate_html_report()
        return None
    
    def __enter__(self):
        """Context manager entry"""
        self.initialize_framework()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.teardown_framework() 