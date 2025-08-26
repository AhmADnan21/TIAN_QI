"""
Common Test Actions
Reusable actions like login, logout, select package, etc.
"""

import time
from config.test_data_config import TestData, PackageData, PaymentData, ErrorMessages
from config.credentials_config import UserCredentials, EnvironmentCredentials
from locators.element_locators import LoginPageLocators, PackageOrderPageLocators, PersonalCenterPageLocators
from mappings.dropdown_mappings import PackageMappings, PaymentMappings
from selenium.webdriver.common.by import By

class CommonActions:
    """Common test actions for reusable operations"""
    
    def __init__(self, framework):
        self.framework = framework
        self.element_helper = framework.get_element_helper()
        self.navigation_helper = framework.get_navigation_helper()
        self.utility_helper = framework.get_utility_helper()
    
    # ===== Login Actions =====
    def login_with_balance(self, test_case=None, user_key="user_with_balance_1"):
        """Login with account that has balance"""
        if test_case:
            with self.framework.track_step(test_case, "Login", "Login with account that has balance"):
                return self._perform_login(user_key)
        else:
            return self._perform_login(user_key)
    
    def login_without_balance(self, test_case=None, user_key="user_no_balance_1"):
        """Login with account that has no balance"""
        if test_case:
            with self.framework.track_step(test_case, "Login", "Login with account that has no balance"):
                return self._perform_login(user_key)
        else:
            return self._perform_login(user_key)
    
    def _perform_login(self, user_key):
        """Perform login with specified user"""
        try:
            # Get user credentials
            user_creds = UserCredentials.get_user_with_balance(user_key) or UserCredentials.get_user_without_balance(user_key)
            if not user_creds:
                raise Exception(f"User credentials not found for key: {user_key}")
            
            # Navigate to login page
            self.navigation_helper.navigate_to_login_page()
            self.utility_helper.wait(3)
            
            # Check if already logged in
            if self.navigation_helper.is_on_package_order_page() or self.navigation_helper.is_on_home_page():
                self.framework.logger.info("Already logged in")
                return True
            
            # Enter phone number
            self.element_helper.input_text(LoginPageLocators.PHONE_INPUT, user_creds["phone"])
            self.framework.logger.info(f"Entered phone number: {user_creds['phone']}")
            
            # Enter password
            self.element_helper.input_text(LoginPageLocators.PASSWORD_INPUT, user_creds["password"])
            self.framework.logger.info("Entered password")
            
            # Click login button
            self.element_helper.click_element(LoginPageLocators.LOGIN_BUTTON, use_js=True)
            self.framework.logger.info("Clicked login button")
            
            # Wait for redirect
            self.utility_helper.wait(5)
            
            # Verify login success
            if self.navigation_helper.is_on_package_order_page() or self.navigation_helper.is_on_home_page():
                self.framework.logger.info("✅ Login successful")
                return True
            else:
                # Check for error messages
                if self.element_helper.is_element_present(LoginPageLocators.ERROR_MESSAGE, timeout=5):
                    error_text = self.element_helper.get_text(LoginPageLocators.ERROR_MESSAGE)
                    raise Exception(f"Login failed: {error_text}")
                else:
                    raise Exception("Login failed - no redirect to expected page")
                    
        except Exception as e:
            self.framework.logger.error(f"Login failed: {str(e)}")
            raise
    
    def logout(self, test_case=None):
        """Logout from the application"""
        if test_case:
            with self.framework.track_step(test_case, "Logout", "Logout from application"):
                return self._perform_logout()
        else:
            return self._perform_logout()
    
    def _perform_logout(self):
        """Perform logout"""
        try:
            # Navigate to home page first
            self.navigation_helper.navigate_to_home_page()
            
            # Look for logout button/link (implementation depends on UI)
            # This is a placeholder - actual implementation depends on the logout UI
            logout_button = (By.XPATH, "//a[contains(text(), '退出登录')]")
            
            if self.element_helper.is_element_present(logout_button, timeout=5):
                self.element_helper.click_element(logout_button)
                self.utility_helper.wait(3)
                
                # Verify logout success
                if self.navigation_helper.is_on_login_page():
                    self.framework.logger.info("✅ Logout successful")
                    return True
                else:
                    raise Exception("Logout failed - not redirected to login page")
            else:
                self.framework.logger.warning("Logout button not found")
                return False
                
        except Exception as e:
            self.framework.logger.error(f"Logout failed: {str(e)}")
            raise
    
    # ===== Package Selection Actions =====
    def select_package(self, package_name, test_case=None):
        """Select package by name"""
        if test_case:
            with self.framework.track_step(test_case, "Select Package", f"Select {package_name} package"):
                return self._perform_package_selection(package_name)
        else:
            return self._perform_package_selection(package_name)
    
    def _perform_package_selection(self, package_name):
        """Perform package selection"""
        try:
            # Navigate to package order page
            self.navigation_helper.navigate_to_package_order_page()
            self.utility_helper.wait(3)
            
            # Map package name to locator
            package_locators = {
                PackageData.DYNAMIC_SUPREME: PackageOrderPageLocators.DYNAMIC_SUPREME_PACKAGE,
                PackageData.STATIC_IP: PackageOrderPageLocators.STATIC_IP_PACKAGE,
                PackageData.DYNAMIC_STANDARD: PackageOrderPageLocators.DYNAMIC_STANDARD_PACKAGE,
                PackageData.DYNAMIC_DEDICATED: PackageOrderPageLocators.DYNAMIC_DEDICATED_PACKAGE
            }
            
            if package_name not in package_locators:
                raise Exception(f"Package '{package_name}' not found in available packages")
            
            # Click on package
            self.element_helper.click_element(package_locators[package_name], use_js=True)
            self.utility_helper.wait(2)
            
            self.framework.logger.info(f"✅ Selected package: {package_name}")
            return True
            
        except Exception as e:
            self.framework.logger.error(f"Package selection failed: {str(e)}")
            raise
    
    def click_buy_now(self, test_case=None):
        """Click Buy Now button"""
        if test_case:
            with self.framework.track_step(test_case, "Click Buy Now", "Click 立即购买 button"):
                return self._perform_buy_now()
        else:
            return self._perform_buy_now()
    
    def _perform_buy_now(self):
        """Perform buy now action"""
        try:
            self.element_helper.click_element(PackageOrderPageLocators.BUY_NOW_BUTTON, use_js=True)
            self.utility_helper.wait(1)
            self.framework.logger.info("✅ Clicked Buy Now button")
            return True
        except Exception as e:
            self.framework.logger.error(f"Buy Now failed: {str(e)}")
            raise
    
    # ===== Payment Actions =====
    def select_payment_method(self, payment_method, test_case=None):
        """Select payment method"""
        if test_case:
            with self.framework.track_step(test_case, "Select Payment", f"Select {payment_method} payment"):
                return self._perform_payment_selection(payment_method)
        else:
            return self._perform_payment_selection(payment_method)
    
    def _perform_payment_selection(self, payment_method):
        """Perform payment method selection"""
        try:
            # Map payment method to locator
            payment_locators = {
                PaymentData.BALANCE_PAYMENT: PackageOrderPageLocators.BALANCE_PAYMENT,
                PaymentData.ALIPAY_PAYMENT: PackageOrderPageLocators.ALIPAY_PAYMENT,
                PaymentData.WECHAT_PAYMENT: PackageOrderPageLocators.WECHAT_PAYMENT
            }
            
            if payment_method not in payment_locators:
                raise Exception(f"Payment method '{payment_method}' not found")
            
            # Click on payment method
            self.element_helper.click_element(payment_locators[payment_method], use_js=True)
            self.utility_helper.wait(1)
            
            self.framework.logger.info(f"✅ Selected payment method: {payment_method}")
            return True
            
        except Exception as e:
            self.framework.logger.error(f"Payment selection failed: {str(e)}")
            raise
    
    def click_pay_now(self, test_case=None):
        """Click Pay Now button"""
        if test_case:
            with self.framework.track_step(test_case, "Click Pay Now", "Click 立即支付 button"):
                return self._perform_pay_now()
        else:
            return self._perform_pay_now()
    
    def _perform_pay_now(self):
        """Perform pay now action"""
        try:
            self.element_helper.click_element(PackageOrderPageLocators.PAY_NOW_BUTTON, use_js=True)
            self.utility_helper.wait(2)
            self.framework.logger.info("✅ Clicked Pay Now button")
            return True
        except Exception as e:
            self.framework.logger.error(f"Pay Now failed: {str(e)}")
            raise
    
    def click_recharge_now(self, test_case=None):
        """Click Recharge Now button (no balance scenario)"""
        if test_case:
            with self.framework.track_step(test_case, "Click Recharge Now", "Click 立即充值 button"):
                return self._perform_recharge_now()
        else:
            return self._perform_recharge_now()
    
    def _perform_recharge_now(self):
        """Perform recharge now action"""
        try:
            # Try specific button first (no balance scenario)
            try:
                self.element_helper.click_element(PackageOrderPageLocators.RECHARGE_BUTTON_NO_BALANCE, use_js=True)
                self.framework.logger.info("Found recharge button with specific class")
            except:
                # Fall back to general button search
                self.element_helper.click_element(PackageOrderPageLocators.RECHARGE_NOW_BUTTON, use_js=True)
                self.framework.logger.info("Found recharge button with general selector")
            
            self.utility_helper.wait(2)
            self.framework.logger.info("✅ Clicked Recharge Now button")
            return True
        except Exception as e:
            self.framework.logger.error(f"Recharge Now failed: {str(e)}")
            raise
    
    # ===== Personal Center Actions =====
    def navigate_to_personal_center(self, test_case=None):
        """Navigate to Personal Center"""
        if test_case:
            with self.framework.track_step(test_case, "Navigate to Personal Center", "Navigate to account manager page"):
                return self._perform_navigate_to_personal_center()
        else:
            return self._perform_navigate_to_personal_center()
    
    def _perform_navigate_to_personal_center(self):
        """Perform navigation to personal center"""
        try:
            self.navigation_helper.navigate_to_personal_center_page()
            self.utility_helper.wait(3)
            self.framework.logger.info("✅ Navigated to Personal Center")
            return True
        except Exception as e:
            self.framework.logger.error(f"Navigation to Personal Center failed: {str(e)}")
            raise
    
    def click_add_paid_account(self, test_case=None):
        """Click Add Paid Account button"""
        if test_case:
            with self.framework.track_step(test_case, "Click Add Paid Account", "Click 添加付费账户 button"):
                return self._perform_add_paid_account()
        else:
            return self._perform_add_paid_account()
    
    def _perform_add_paid_account(self):
        """Perform add paid account action"""
        try:
            self.element_helper.click_element(PersonalCenterPageLocators.ADD_PAID_ACCOUNT_BUTTON, use_js=True)
            self.utility_helper.wait(2)
            self.framework.logger.info("✅ Clicked Add Paid Account button")
            return True
        except Exception as e:
            self.framework.logger.error(f"Add Paid Account failed: {str(e)}")
            raise
    
    def wait_for_package_popup(self, test_case=None):
        """Wait for package selection popup"""
        if test_case:
            with self.framework.track_step(test_case, "Wait for Popup", "Wait for package selection popup"):
                return self._perform_wait_for_popup()
        else:
            return self._perform_wait_for_popup()
    
    def _perform_wait_for_popup(self):
        """Perform wait for popup"""
        try:
            self.element_helper.wait_for_element_visible(PersonalCenterPageLocators.PACKAGE_SELECTION_POPUP)
            self.utility_helper.wait(5)
            self.framework.logger.info("✅ Package selection popup appeared")
            return True
        except Exception as e:
            self.framework.logger.error(f"Wait for popup failed: {str(e)}")
            raise
    
    def select_package_type_personal(self, package_name, test_case=None, has_balance=True):
        """Select package type in Personal Center popup"""
        if test_case:
            with self.framework.track_step(test_case, "Select Package Type", f"Select {package_name} in dropdown"):
                return self._perform_package_type_selection_personal(package_name, has_balance)
        else:
            return self._perform_package_type_selection_personal(package_name, has_balance)
    
    def _perform_package_type_selection_personal(self, package_name, has_balance=True):
        """Perform package type selection in personal center"""
        try:
            # Choose dropdown based on balance status
            dropdown_locator = (PersonalCenterPageLocators.PACKAGE_DROPDOWN_WITH_BALANCE 
                              if has_balance else PersonalCenterPageLocators.PACKAGE_DROPDOWN_NO_BALANCE)
            
            # Get package value from mapping
            package_value = PackageMappings.get_package_value(package_name)
            if not package_value:
                raise Exception(f"Package name {package_name} not found in mapping")
            
            # Select package by value
            self.element_helper.select_dropdown_option_by_value(dropdown_locator, package_value)
            self.utility_helper.wait(1)
            
            self.framework.logger.info(f"✅ Selected {package_name} using Select class")
            return True
            
        except Exception as e:
            self.framework.logger.error(f"Package type selection failed: {str(e)}")
            raise
    
    def input_random_account(self, test_case=None, has_balance=True):
        """Input random account name"""
        if test_case:
            with self.framework.track_step(test_case, "Input Account", "Input random 8-character account"):
                return self._perform_input_random_account(has_balance)
        else:
            return self._perform_input_random_account(has_balance)
    
    def _perform_input_random_account(self, has_balance=True):
        """Perform random account input"""
        try:
            # Generate random account name
            account = self.utility_helper.generate_random_string(8, include_uppercase=False)
            
            # Choose input field based on balance status
            input_locator = (PersonalCenterPageLocators.ACCOUNT_INPUT_WITH_BALANCE 
                           if has_balance else PersonalCenterPageLocators.ACCOUNT_INPUT_NO_BALANCE)
            
            # Input account name
            self.element_helper.input_text(input_locator, account)
            self.utility_helper.wait(1)
            
            self.framework.logger.info(f"✅ Entered account: {account}")
            return account
            
        except Exception as e:
            self.framework.logger.error(f"Random account input failed: {str(e)}")
            raise
    
    def select_payment_method_personal(self, payment_method, test_case=None):
        """Select payment method in Personal Center"""
        if test_case:
            with self.framework.track_step(test_case, "Select Payment Method", f"Select {payment_method} payment"):
                return self._perform_payment_selection_personal(payment_method)
        else:
            return self._perform_payment_selection_personal(payment_method)
    
    def _perform_payment_selection_personal(self, payment_method):
        """Perform payment method selection in personal center"""
        try:
            # Map payment method to locator (same as package order)
            payment_locators = {
                PaymentData.BALANCE_PAYMENT: PersonalCenterPageLocators.BALANCE_PAYMENT,
                PaymentData.ALIPAY_PAYMENT: PersonalCenterPageLocators.ALIPAY_PAYMENT,
                PaymentData.WECHAT_PAYMENT: PersonalCenterPageLocators.WECHAT_PAYMENT
            }
            
            if payment_method not in payment_locators:
                raise Exception(f"Payment method '{payment_method}' not found")
            
            # Click on payment method
            self.element_helper.click_element(payment_locators[payment_method], use_js=True)
            self.utility_helper.wait(1)
            
            self.framework.logger.info(f"✅ Selected payment method: {payment_method}")
            return True
            
        except Exception as e:
            self.framework.logger.error(f"Payment selection failed: {str(e)}")
            raise
    
    def click_pay_personal(self, test_case=None):
        """Click Pay button in Personal Center"""
        if test_case:
            with self.framework.track_step(test_case, "Click Pay", "Click Pay button"):
                return self._perform_pay_personal()
        else:
            return self._perform_pay_personal()
    
    def _perform_pay_personal(self):
        """Perform pay action in personal center"""
        try:
            self.element_helper.click_element(PersonalCenterPageLocators.PAY_BUTTON, use_js=True)
            self.utility_helper.wait(2)
            self.framework.logger.info("✅ Clicked Pay button")
            return True
        except Exception as e:
            self.framework.logger.error(f"Pay action failed: {str(e)}")
            raise
    
    # ===== Verification Actions =====
    def verify_success_message(self, test_case=None):
        """Verify success message appears"""
        if test_case:
            with self.framework.track_step(test_case, "Verify Success", "Check for success message"):
                return self._perform_success_verification()
        else:
            return self._perform_success_verification()
    
    def _perform_success_verification(self):
        """Perform success message verification"""
        try:
            success_msg = self.element_helper.find_visible_element(PersonalCenterPageLocators.SUCCESS_MESSAGE)
            assert ErrorMessages.ACCOUNT_CREATED in success_msg.text
            self.framework.logger.info("✅ Success message verified")
            return True
        except Exception as e:
            self.framework.logger.error(f"Success verification failed: {str(e)}")
            raise
    
    def verify_insufficient_balance_error(self, test_case=None):
        """Verify insufficient balance error message"""
        if test_case:
            with self.framework.track_step(test_case, "Verify Insufficient Balance Error", "Check for insufficient balance error message"):
                return self._perform_insufficient_balance_verification()
        else:
            return self._perform_insufficient_balance_verification()
    
    def _perform_insufficient_balance_verification(self):
        """Perform insufficient balance error verification"""
        try:
            error_msg = self.element_helper.find_visible_element(PersonalCenterPageLocators.INSUFFICIENT_BALANCE_ERROR)
            assert ErrorMessages.INSUFFICIENT_BALANCE in error_msg.text
            self.framework.logger.info("✅ Insufficient balance error message verified")
            return True
        except Exception as e:
            self.framework.logger.error(f"Insufficient balance verification failed: {str(e)}")
            raise
    
    def verify_recharge_redirect(self, test_case=None):
        """Verify redirect to recharge page"""
        if test_case:
            with self.framework.track_step(test_case, "Verify Recharge Redirect", "Check redirect to recharge page"):
                return self._perform_recharge_redirect_verification()
        else:
            return self._perform_recharge_redirect_verification()
    
    def _perform_recharge_redirect_verification(self):
        """Perform recharge redirect verification"""
        try:
            self.navigation_helper.wait_for_url_change("tab=recharge")
            assert "tab=recharge" in self.navigation_helper.get_current_url()
            self.framework.logger.info("✅ Recharge redirect verified - no balance detected")
            return True
        except Exception as e:
            self.framework.logger.error(f"Recharge redirect verification failed: {str(e)}")
            raise
    
    def verify_alipay_sandbox(self, test_case=None):
        """Verify Alipay sandbox opens"""
        if test_case:
            with self.framework.track_step(test_case, "Verify Alipay", "Check Alipay sandbox opens"):
                return self._perform_alipay_verification()
        else:
            return self._perform_alipay_verification()
    
    def _perform_alipay_verification(self):
        """Perform Alipay sandbox verification"""
        try:
            self.navigation_helper.switch_to_new_window()
            self.navigation_helper.wait_for_url_change(PaymentData.ALIPAY_SANDBOX_URL)
            assert PaymentData.ALIPAY_SANDBOX_URL in self.navigation_helper.get_current_url()
            self.framework.logger.info("✅ Alipay sandbox verified")
            return True
        except Exception as e:
            self.framework.logger.error(f"Alipay verification failed: {str(e)}")
            raise
    
    def close_wechat_popup(self, test_case=None):
        """Close WeChat QR popup"""
        if test_case:
            with self.framework.track_step(test_case, "Close WeChat Popup", "Close the WeChat QR popup"):
                return self._perform_close_wechat_popup()
        else:
            return self._perform_close_wechat_popup()
    
    def _perform_close_wechat_popup(self):
        """Perform WeChat popup close"""
        try:
            self.element_helper.click_element(PackageOrderPageLocators.WECHAT_POPUP_CLOSE, use_js=True)
            self.utility_helper.wait(1)
            self.framework.logger.info("✅ WeChat popup closed")
            return True
        except Exception as e:
            self.framework.logger.error(f"WeChat popup close failed: {str(e)}")
            raise
    
    def verify_wechat_qr(self, test_case=None):
        """Verify WeChat QR code appears"""
        if test_case:
            with self.framework.track_step(test_case, "Verify WeChat", "Check QR code appears"):
                return self._perform_wechat_qr_verification()
        else:
            return self._perform_wechat_qr_verification()
    
    def _perform_wechat_qr_verification(self):
        """Perform WeChat QR verification"""
        try:
            qr_code = self.element_helper.find_visible_element(PackageOrderPageLocators.WECHAT_QR_CODE)
            assert qr_code.is_displayed()
            self.framework.logger.info("✅ WeChat QR code verified")
            return True
        except Exception as e:
            self.framework.logger.error(f"WeChat QR verification failed: {str(e)}")
            raise 