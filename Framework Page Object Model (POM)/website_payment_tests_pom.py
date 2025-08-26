#!/usr/bin/env python3
"""
Website Payment Tests using Page Object Model (POM) Structure
This script demonstrates the POM approach for better maintainability and reusability.
"""

import os
import sys
import logging
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from test_base import TestBase
from login_page import LoginPage
from package_order_page import PackageOrderPage
from personal_center_page import PersonalCenterPage

class WebsitePaymentTestsPOM(TestBase):
    """Test class for Website Payment Tests using Page Object Model"""
    
    # Test credentials
    PHONE_WITH_BALANCE = "15332595364"
    PHONE_WITHOUT_BALANCE = "15658873355"
    PASSWORD = "Test@123"
    
    def __init__(self):
        super().__init__()
        self.login_page = None
        self.package_order_page = None
        self.personal_center_page = None
    
    def setup_page_objects(self):
        """Initialize page objects"""
        self.login_page = LoginPage(self.driver)
        self.package_order_page = PackageOrderPage(self.driver)
        self.personal_center_page = PersonalCenterPage(self.driver)
        self.logger.info("Page objects initialized")
    
    def setup(self):
        """Setup test environment with page objects"""
        super().setup()
        self.setup_page_objects()
    
    # ===== Test Methods for Package Order Page =====
    
    def test_dynamic_supreme_balance_payment(self):
        """Test Dynamic Supreme package purchase with balance payment"""
        try:
            # Login with balance account
            self.login_page.login_with_credentials(self.PHONE_WITH_BALANCE, self.PASSWORD)
            
            # Navigate to package order page
            self.package_order_page.navigate_to_package_order()
            
            # Purchase package with balance
            return self.package_order_page.purchase_package_with_balance("Dynamic Supreme")
            
        except Exception as e:
            self.logger.error(f"Dynamic Supreme balance payment test failed: {str(e)}")
            return False
    
    def test_dynamic_supreme_alipay_payment(self):
        """Test Dynamic Supreme package purchase with Alipay payment"""
        try:
            # Navigate to package order page
            self.package_order_page.navigate_to_package_order()
            
            # Purchase package with Alipay
            return self.package_order_page.purchase_package_with_alipay("Dynamic Supreme")
            
        except Exception as e:
            self.logger.error(f"Dynamic Supreme Alipay payment test failed: {str(e)}")
            return False
    
    def test_dynamic_supreme_wechat_payment(self):
        """Test Dynamic Supreme package purchase with WeChat payment"""
        try:
            # Navigate to package order page
            self.package_order_page.navigate_to_package_order()
            
            # Purchase package with WeChat
            return self.package_order_page.purchase_package_with_wechat("Dynamic Supreme")
            
        except Exception as e:
            self.logger.error(f"Dynamic Supreme WeChat payment test failed: {str(e)}")
            return False
    
    def test_dynamic_supreme_no_balance(self):
        """Test Dynamic Supreme package purchase with no balance"""
        try:
            # Login with no balance account
            self.login_page.login_with_credentials(self.PHONE_WITHOUT_BALANCE, self.PASSWORD)
            
            # Navigate to package order page
            self.package_order_page.navigate_to_package_order()
            
            # Attempt purchase with no balance
            return self.package_order_page.purchase_package_no_balance("Dynamic Supreme")
            
        except Exception as e:
            self.logger.error(f"Dynamic Supreme no balance test failed: {str(e)}")
            return False
    
    def test_static_ip_balance_payment(self):
        """Test Static IP package purchase with balance payment"""
        try:
            # Navigate to package order page
            self.package_order_page.navigate_to_package_order()
            
            # Purchase package with balance
            return self.package_order_page.purchase_package_with_balance("Static IP")
            
        except Exception as e:
            self.logger.error(f"Static IP balance payment test failed: {str(e)}")
            return False
    
    def test_static_ip_alipay_payment(self):
        """Test Static IP package purchase with Alipay payment"""
        try:
            # Navigate to package order page
            self.package_order_page.navigate_to_package_order()
            
            # Purchase package with Alipay
            return self.package_order_page.purchase_package_with_alipay("Static IP")
            
        except Exception as e:
            self.logger.error(f"Static IP Alipay payment test failed: {str(e)}")
            return False
    
    def test_static_ip_wechat_payment(self):
        """Test Static IP package purchase with WeChat payment"""
        try:
            # Navigate to package order page
            self.package_order_page.navigate_to_package_order()
            
            # Purchase package with WeChat
            return self.package_order_page.purchase_package_with_wechat("Static IP")
            
        except Exception as e:
            self.logger.error(f"Static IP WeChat payment test failed: {str(e)}")
            return False
    
    def test_static_ip_no_balance(self):
        """Test Static IP package purchase with no balance"""
        try:
            # Navigate to package order page
            self.package_order_page.navigate_to_package_order()
            
            # Attempt purchase with no balance
            return self.package_order_page.purchase_package_no_balance("Static IP")
            
        except Exception as e:
            self.logger.error(f"Static IP no balance test failed: {str(e)}")
            return False
    
    def test_dynamic_standard_balance_payment(self):
        """Test Dynamic Standard package purchase with balance payment"""
        try:
            # Navigate to package order page
            self.package_order_page.navigate_to_package_order()
            
            # Purchase package with balance
            return self.package_order_page.purchase_package_with_balance("Dynamic Standard")
            
        except Exception as e:
            self.logger.error(f"Dynamic Standard balance payment test failed: {str(e)}")
            return False
    
    def test_dynamic_standard_alipay_payment(self):
        """Test Dynamic Standard package purchase with Alipay payment"""
        try:
            # Navigate to package order page
            self.package_order_page.navigate_to_package_order()
            
            # Purchase package with Alipay
            return self.package_order_page.purchase_package_with_alipay("Dynamic Standard")
            
        except Exception as e:
            self.logger.error(f"Dynamic Standard Alipay payment test failed: {str(e)}")
            return False
    
    def test_dynamic_standard_wechat_payment(self):
        """Test Dynamic Standard package purchase with WeChat payment"""
        try:
            # Navigate to package order page
            self.package_order_page.navigate_to_package_order()
            
            # Purchase package with WeChat
            return self.package_order_page.purchase_package_with_wechat("Dynamic Standard")
            
        except Exception as e:
            self.logger.error(f"Dynamic Standard WeChat payment test failed: {str(e)}")
            return False
    
    def test_dynamic_standard_no_balance(self):
        """Test Dynamic Standard package purchase with no balance"""
        try:
            # Navigate to package order page
            self.package_order_page.navigate_to_package_order()
            
            # Attempt purchase with no balance
            return self.package_order_page.purchase_package_no_balance("Dynamic Standard")
            
        except Exception as e:
            self.logger.error(f"Dynamic Standard no balance test failed: {str(e)}")
            return False
    
    def test_dynamic_dedicated_balance_payment(self):
        """Test Dynamic Dedicated package purchase with balance payment"""
        try:
            # Navigate to package order page
            self.package_order_page.navigate_to_package_order()
            
            # Purchase package with balance
            return self.package_order_page.purchase_package_with_balance("Dynamic Dedicated")
            
        except Exception as e:
            self.logger.error(f"Dynamic Dedicated balance payment test failed: {str(e)}")
            return False
    
    def test_dynamic_dedicated_alipay_payment(self):
        """Test Dynamic Dedicated package purchase with Alipay payment"""
        try:
            # Navigate to package order page
            self.package_order_page.navigate_to_package_order()
            
            # Purchase package with Alipay
            return self.package_order_page.purchase_package_with_alipay("Dynamic Dedicated")
            
        except Exception as e:
            self.logger.error(f"Dynamic Dedicated Alipay payment test failed: {str(e)}")
            return False
    
    def test_dynamic_dedicated_wechat_payment(self):
        """Test Dynamic Dedicated package purchase with WeChat payment"""
        try:
            # Navigate to package order page
            self.package_order_page.navigate_to_package_order()
            
            # Purchase package with WeChat
            return self.package_order_page.purchase_package_with_wechat("Dynamic Dedicated")
            
        except Exception as e:
            self.logger.error(f"Dynamic Dedicated WeChat payment test failed: {str(e)}")
            return False
    
    def test_dynamic_dedicated_no_balance(self):
        """Test Dynamic Dedicated package purchase with no balance"""
        try:
            # Navigate to package order page
            self.package_order_page.navigate_to_package_order()
            
            # Attempt purchase with no balance
            return self.package_order_page.purchase_package_no_balance("Dynamic Dedicated")
            
        except Exception as e:
            self.logger.error(f"Dynamic Dedicated no balance test failed: {str(e)}")
            return False
    
    # ===== Test Methods for Personal Center =====
    
    def test_personal_dynamic_supreme_balance(self):
        """Test Dynamic Supreme package creation in Personal Center with balance payment"""
        try:
            # Navigate to personal center
            self.personal_center_page.navigate_to_personal_center()
            
            # Create paid account with balance
            return self.personal_center_page.create_paid_account_with_balance("天启动态尊享")
            
        except Exception as e:
            self.logger.error(f"Personal Center Dynamic Supreme balance test failed: {str(e)}")
            return False
    
    def test_personal_dynamic_supreme_alipay(self):
        """Test Dynamic Supreme package creation in Personal Center with Alipay payment"""
        try:
            # Navigate to personal center
            self.personal_center_page.navigate_to_personal_center()
            
            # Create paid account with Alipay
            return self.personal_center_page.create_paid_account_with_alipay("天启动态尊享")
            
        except Exception as e:
            self.logger.error(f"Personal Center Dynamic Supreme Alipay test failed: {str(e)}")
            return False
    
    def test_personal_dynamic_supreme_wechat(self):
        """Test Dynamic Supreme package creation in Personal Center with WeChat payment"""
        try:
            # Navigate to personal center
            self.personal_center_page.navigate_to_personal_center()
            
            # Create paid account with WeChat
            return self.personal_center_page.create_paid_account_with_wechat("天启动态尊享")
            
        except Exception as e:
            self.logger.error(f"Personal Center Dynamic Supreme WeChat test failed: {str(e)}")
            return False
    
    def test_personal_dynamic_supreme_no_balance(self):
        """Test Dynamic Supreme package creation in Personal Center with no balance"""
        try:
            # Navigate to personal center
            self.personal_center_page.navigate_to_personal_center()
            
            # Create paid account with no balance
            return self.personal_center_page.create_paid_account_no_balance("天启动态尊享")
            
        except Exception as e:
            self.logger.error(f"Personal Center Dynamic Supreme no balance test failed: {str(e)}")
            return False
    
    def test_personal_static_ip_balance(self):
        """Test Static IP package creation in Personal Center with balance payment"""
        try:
            # Navigate to personal center
            self.personal_center_page.navigate_to_personal_center()
            
            # Create paid account with balance
            return self.personal_center_page.create_paid_account_with_balance("静态IP-天启")
            
        except Exception as e:
            self.logger.error(f"Personal Center Static IP balance test failed: {str(e)}")
            return False
    
    def test_personal_static_ip_alipay(self):
        """Test Static IP package creation in Personal Center with Alipay payment"""
        try:
            # Navigate to personal center
            self.personal_center_page.navigate_to_personal_center()
            
            # Create paid account with Alipay
            return self.personal_center_page.create_paid_account_with_alipay("静态IP-天启")
            
        except Exception as e:
            self.logger.error(f"Personal Center Static IP Alipay test failed: {str(e)}")
            return False
    
    def test_personal_static_ip_wechat(self):
        """Test Static IP package creation in Personal Center with WeChat payment"""
        try:
            # Navigate to personal center
            self.personal_center_page.navigate_to_personal_center()
            
            # Create paid account with WeChat
            return self.personal_center_page.create_paid_account_with_wechat("静态IP-天启")
            
        except Exception as e:
            self.logger.error(f"Personal Center Static IP WeChat test failed: {str(e)}")
            return False
    
    def test_personal_static_ip_no_balance(self):
        """Test Static IP package creation in Personal Center with no balance"""
        try:
            # Navigate to personal center
            self.personal_center_page.navigate_to_personal_center()
            
            # Create paid account with no balance
            return self.personal_center_page.create_paid_account_no_balance("静态IP-天启")
            
        except Exception as e:
            self.logger.error(f"Personal Center Static IP no balance test failed: {str(e)}")
            return False
    
    def test_personal_dynamic_standard_balance(self):
        """Test Dynamic Standard package creation in Personal Center with balance payment"""
        try:
            # Navigate to personal center
            self.personal_center_page.navigate_to_personal_center()
            
            # Create paid account with balance
            return self.personal_center_page.create_paid_account_with_balance("天启动态标准套餐")
            
        except Exception as e:
            self.logger.error(f"Personal Center Dynamic Standard balance test failed: {str(e)}")
            return False
    
    def test_personal_dynamic_standard_alipay(self):
        """Test Dynamic Standard package creation in Personal Center with Alipay payment"""
        try:
            # Navigate to personal center
            self.personal_center_page.navigate_to_personal_center()
            
            # Create paid account with Alipay
            return self.personal_center_page.create_paid_account_with_alipay("天启动态标准套餐")
            
        except Exception as e:
            self.logger.error(f"Personal Center Dynamic Standard Alipay test failed: {str(e)}")
            return False
    
    def test_personal_dynamic_standard_wechat(self):
        """Test Dynamic Standard package creation in Personal Center with WeChat payment"""
        try:
            # Navigate to personal center
            self.personal_center_page.navigate_to_personal_center()
            
            # Create paid account with WeChat
            return self.personal_center_page.create_paid_account_with_wechat("天启动态标准套餐")
            
        except Exception as e:
            self.logger.error(f"Personal Center Dynamic Standard WeChat test failed: {str(e)}")
            return False
    
    def test_personal_dynamic_standard_no_balance(self):
        """Test Dynamic Standard package creation in Personal Center with no balance"""
        try:
            # Navigate to personal center
            self.personal_center_page.navigate_to_personal_center()
            
            # Create paid account with no balance
            return self.personal_center_page.create_paid_account_no_balance("天启动态标准套餐")
            
        except Exception as e:
            self.logger.error(f"Personal Center Dynamic Standard no balance test failed: {str(e)}")
            return False
    
    def test_personal_dynamic_dedicated_balance(self):
        """Test Dynamic Dedicated package creation in Personal Center with balance payment"""
        try:
            # Navigate to personal center
            self.personal_center_page.navigate_to_personal_center()
            
            # Create paid account with balance
            return self.personal_center_page.create_paid_account_with_balance("天启动态独享套餐")
            
        except Exception as e:
            self.logger.error(f"Personal Center Dynamic Dedicated balance test failed: {str(e)}")
            return False
    
    def test_personal_dynamic_dedicated_alipay(self):
        """Test Dynamic Dedicated package creation in Personal Center with Alipay payment"""
        try:
            # Navigate to personal center
            self.personal_center_page.navigate_to_personal_center()
            
            # Create paid account with Alipay
            return self.personal_center_page.create_paid_account_with_alipay("天启动态独享套餐")
            
        except Exception as e:
            self.logger.error(f"Personal Center Dynamic Dedicated Alipay test failed: {str(e)}")
            return False
    
    def test_personal_dynamic_dedicated_wechat(self):
        """Test Dynamic Dedicated package creation in Personal Center with WeChat payment"""
        try:
            # Navigate to personal center
            self.personal_center_page.navigate_to_personal_center()
            
            # Create paid account with WeChat
            return self.personal_center_page.create_paid_account_with_wechat("天启动态独享套餐")
            
        except Exception as e:
            self.logger.error(f"Personal Center Dynamic Dedicated WeChat test failed: {str(e)}")
            return False
    
    def test_personal_dynamic_dedicated_no_balance(self):
        """Test Dynamic Dedicated package creation in Personal Center with no balance"""
        try:
            # Navigate to personal center
            self.personal_center_page.navigate_to_personal_center()
            
            # Create paid account with no balance
            return self.personal_center_page.create_paid_account_no_balance("天启动态独享套餐")
            
        except Exception as e:
            self.logger.error(f"Personal Center Dynamic Dedicated no balance test failed: {str(e)}")
            return False

def main():
    """Main execution function"""
    test_runner = WebsitePaymentTestsPOM()
    test_runner.setup()
    
    test_results = {}
    
    try:
        # Define test methods with their descriptions
        test_methods = [
            # Package Order Page Tests
            ("1.1 Dynamic Supreme - Wallet Balance", "Test wallet balance payment for Dynamic Supreme package", test_runner.test_dynamic_supreme_balance_payment),
            ("1.2 Dynamic Supreme - Alipay", "Test Alipay payment flow for Dynamic Supreme package", test_runner.test_dynamic_supreme_alipay_payment),
            ("1.3 Dynamic Supreme - WeChat", "Test WeChat payment flow for Dynamic Supreme package", test_runner.test_dynamic_supreme_wechat_payment),
            ("1.4 Dynamic Supreme - Wallet No Balance", "Test wallet payment with no balance for Dynamic Supreme package", test_runner.test_dynamic_supreme_no_balance),
            
            ("2.1 Static IP - Wallet Balance", "Test wallet balance payment for Static IP package", test_runner.test_static_ip_balance_payment),
            ("2.2 Static IP - Alipay", "Test Alipay payment flow for Static IP package", test_runner.test_static_ip_alipay_payment),
            ("2.3 Static IP - WeChat", "Test WeChat payment flow for Static IP package", test_runner.test_static_ip_wechat_payment),
            ("2.4 Static IP - Wallet No Balance", "Test wallet payment with no balance for Static IP package", test_runner.test_static_ip_no_balance),
            
            ("3.1 Dynamic Standard - Wallet Balance", "Test wallet balance payment for Dynamic Standard package", test_runner.test_dynamic_standard_balance_payment),
            ("3.2 Dynamic Standard - Alipay", "Test Alipay payment flow for Dynamic Standard package", test_runner.test_dynamic_standard_alipay_payment),
            ("3.3 Dynamic Standard - WeChat", "Test WeChat payment flow for Dynamic Standard package", test_runner.test_dynamic_standard_wechat_payment),
            ("3.4 Dynamic Standard - Wallet No Balance", "Test wallet payment with no balance for Dynamic Standard package", test_runner.test_dynamic_standard_no_balance),
            
            ("4.1 Dynamic Dedicated - Wallet Balance", "Test wallet balance payment for Dynamic Dedicated package", test_runner.test_dynamic_dedicated_balance_payment),
            ("4.2 Dynamic Dedicated - Alipay", "Test Alipay payment flow for Dynamic Dedicated package", test_runner.test_dynamic_dedicated_alipay_payment),
            ("4.3 Dynamic Dedicated - WeChat", "Test WeChat payment flow for Dynamic Dedicated package", test_runner.test_dynamic_dedicated_wechat_payment),
            ("4.4 Dynamic Dedicated - Wallet No Balance", "Test wallet payment with no balance for Dynamic Dedicated package", test_runner.test_dynamic_dedicated_no_balance),
            
            # Personal Center Tests
            ("5.1.1 Dynamic Supreme - Wallet Balance", "Test wallet balance payment for Dynamic Supreme in Personal Center", test_runner.test_personal_dynamic_supreme_balance),
            ("5.1.2 Dynamic Supreme - Alipay", "Test Alipay payment flow for Dynamic Supreme in Personal Center", test_runner.test_personal_dynamic_supreme_alipay),
            ("5.1.3 Dynamic Supreme - WeChat", "Test WeChat payment flow for Dynamic Supreme in Personal Center", test_runner.test_personal_dynamic_supreme_wechat),
            ("5.1.4 Dynamic Supreme - Wallet No Balance", "Test wallet payment with no balance for Dynamic Supreme in Personal Center", test_runner.test_personal_dynamic_supreme_no_balance),
            
            ("5.2.1 Static IP - Wallet Balance", "Test wallet balance payment for Static IP in Personal Center", test_runner.test_personal_static_ip_balance),
            ("5.2.2 Static IP - Alipay", "Test Alipay payment flow for Static IP in Personal Center", test_runner.test_personal_static_ip_alipay),
            ("5.2.3 Static IP - WeChat", "Test WeChat payment flow for Static IP in Personal Center", test_runner.test_personal_static_ip_wechat),
            ("5.2.4 Static IP - Wallet No Balance", "Test wallet payment with no balance for Static IP in Personal Center", test_runner.test_personal_static_ip_no_balance),
            
            ("5.3.1 Dynamic Standard - Wallet Balance", "Test wallet balance payment for Dynamic Standard in Personal Center", test_runner.test_personal_dynamic_standard_balance),
            ("5.3.2 Dynamic Standard - Alipay", "Test Alipay payment flow for Dynamic Standard in Personal Center", test_runner.test_personal_dynamic_standard_alipay),
            ("5.3.3 Dynamic Standard - WeChat", "Test WeChat payment flow for Dynamic Standard in Personal Center", test_runner.test_personal_dynamic_standard_wechat),
            ("5.3.4 Dynamic Standard - Wallet No Balance", "Test wallet payment with no balance for Dynamic Standard in Personal Center", test_runner.test_personal_dynamic_standard_no_balance),
            
            ("5.4.1 Dynamic Dedicated - Wallet Balance", "Test wallet balance payment for Dynamic Dedicated in Personal Center", test_runner.test_personal_dynamic_dedicated_balance),
            ("5.4.2 Dynamic Dedicated - Alipay", "Test Alipay payment flow for Dynamic Dedicated in Personal Center", test_runner.test_personal_dynamic_dedicated_alipay),
            ("5.4.3 Dynamic Dedicated - WeChat", "Test WeChat payment flow for Dynamic Dedicated in Personal Center", test_runner.test_personal_dynamic_dedicated_wechat),
            ("5.4.4 Dynamic Dedicated - Wallet No Balance", "Test wallet payment with no balance for Dynamic Dedicated in Personal Center", test_runner.test_personal_dynamic_dedicated_no_balance),
        ]
        
        # Execute all tests
        for test_name, test_description, test_method in test_methods:
            print(f"\n{'='*60}")
            print(f"Running: {test_name}")
            print(f"{'='*60}")
            
            result = test_runner.run_test_with_reporting(test_name, test_description, test_method)
            test_results[test_name] = result
            
            # Add some delay between tests
            import time
            time.sleep(2)
    
    finally:
        test_runner.teardown()
        
        # Print final results
        print("\n" + "="*60)
        print("FINAL TEST RESULTS - POM VERSION")
        print("="*60)
        
        # Group results by category
        categories = {
            "1. DYNAMIC SUPREME": ["1.1", "1.2", "1.3", "1.4"],
            "2. STATIC IP": ["2.1", "2.2", "2.3", "2.4"],
            "3. DYNAMIC STANDARD": ["3.1", "3.2", "3.3", "3.4"],
            "4. DYNAMIC DEDICATED": ["4.1", "4.2", "4.3", "4.4"],
            "5. PERSONAL CENTER": {
                "5.1 Dynamic Supreme": ["5.1.1", "5.1.2", "5.1.3", "5.1.4"],
                "5.2 Static IP": ["5.2.1", "5.2.2", "5.2.3", "5.2.4"],
                "5.3 Dynamic Standard": ["5.3.1", "5.3.2", "5.3.3", "5.3.4"],
                "5.4 Dynamic Dedicated": ["5.4.1", "5.4.2", "5.4.3", "5.4.4"]
            }
        }
        
        for category, tests in categories.items():
            print(f"\n{category}:")
            if isinstance(tests, list):
                for test_prefix in tests:
                    for test_name, result in test_results.items():
                        if test_name.startswith(test_prefix):
                            status = "✅ PASSED" if result else "❌ FAILED"
                            print(f"   {test_name}: {status}")
            else:
                for subcategory, sub_tests in tests.items():
                    print(f"   {subcategory}:")
                    for test_prefix in sub_tests:
                        for test_name, result in test_results.items():
                            if test_name.startswith(test_prefix):
                                status = "✅ PASSED" if result else "❌ FAILED"
                                print(f"      {test_name}: {status}")
        
        # Calculate summary
        passed_count = sum(1 for result in test_results.values() if result)
        total_count = len(test_results)
        
        print(f"\nSUMMARY: {passed_count}/{total_count} tests passed")
        print(f"Success Rate: {(passed_count/total_count)*100:.1f}%")

if __name__ == "__main__":
    main() 