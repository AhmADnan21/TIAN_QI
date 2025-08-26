from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .base_page import BasePage
import time
import random
import string

class PersonalCenterPage(BasePage):
    """Page object for the personal center page"""
    
    # Navigation locators
    ADD_PAID_ACCOUNT_BUTTON = (By.XPATH, "//button[contains(text(), '添加付费账户')]")
    
    # Package popup locators
    PACKAGE_POPUP_HEADER = (By.ID, "__BVID__66___BV_modal_header_")
    PACKAGE_DROPDOWN = (By.ID, "__BVID__548")
    PACKAGE_DROPDOWN_NO_BALANCE = (By.ID, "__BVID__98")
    ACCOUNT_INPUT = (By.ID, "__BVID__552")
    ACCOUNT_INPUT_NO_BALANCE = (By.ID, "__BVID__102")
    
    # Payment method locators
    PAYMENT_METHOD_BALANCE = (By.XPATH, "//div[contains(text(), '余额')]")
    PAYMENT_METHOD_ALIPAY = (By.XPATH, "//div[contains(text(), '支付宝')]")
    PAYMENT_METHOD_WECHAT = (By.XPATH, "//div[contains(text(), '微信')]")
    
    # Action buttons
    PAY_BUTTON = (By.XPATH, "//div[contains(text(), '确定')]")
    
    # Success/Error message locators
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'ml-20') and contains(text(), '创建成功')]")
    INSUFFICIENT_BALANCE_ERROR = (By.XPATH, "//div[contains(@class, 'ml-20') and contains(text(), '账户余额不足')]")
    WECHAT_POPUP_CLOSE = (By.XPATH, "//i[contains(@class, 'icon--x') and contains(@class, 'close-icon')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://test-ip-tianqi.cd.xiaoxigroup.net/personal/accountManager"
    
    def navigate_to_personal_center(self):
        """Navigate to Personal Center account manager page"""
        self.navigate_to(self.url)
        time.sleep(3)
        self.logger.info(f"Navigated to Personal Center. Current URL: {self.get_current_url()}")
    
    def click_add_paid_account(self):
        """Click the 添加付费账户 button"""
        self.click_element(self.ADD_PAID_ACCOUNT_BUTTON)
        time.sleep(2)
        self.logger.info("Clicked add paid account button")
    
    def wait_for_package_popup(self):
        """Wait for the package selection popup to appear"""
        self.find_visible_element(self.PACKAGE_POPUP_HEADER)
        time.sleep(5)
        self.logger.info("Package selection popup appeared")
    
    def select_package_type(self, package_name, has_balance=True):
        """Select package type in Personal Center popup"""
        dropdown_id = self.PACKAGE_DROPDOWN if has_balance else self.PACKAGE_DROPDOWN_NO_BALANCE
        dropdown = self.find_element(dropdown_id)
        select = Select(dropdown)
        
        # Map package names to their values
        package_mapping = {
            "天启动态尊享": "70",
            "静态IP-天启": "64", 
            "天启动态标准套餐": "28",
            "天启动态独享套餐": "30"
        }
        
        if package_name in package_mapping:
            select.select_by_value(package_mapping[package_name])
            self.logger.info(f"Selected {package_name} using Select class")
            time.sleep(1)
        else:
            raise Exception(f"Package name {package_name} not found in mapping")
    
    def input_random_account(self, has_balance=True):
        """Input random 8-character alphanumeric string in account field"""
        # Generate random 8-character alphanumeric string
        account = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        
        input_id = self.ACCOUNT_INPUT if has_balance else self.ACCOUNT_INPUT_NO_BALANCE
        account_field = self.find_clickable_element(input_id)
        account_field.clear()
        account_field.send_keys(account)
        time.sleep(1)
        self.logger.info(f"Entered account: {account}")
        return account
    
    def select_payment_method(self, method):
        """Select payment method in Personal Center popup"""
        method_mapping = {
            "余额": self.PAYMENT_METHOD_BALANCE,
            "支付宝": self.PAYMENT_METHOD_ALIPAY,
            "微信": self.PAYMENT_METHOD_WECHAT
        }
        
        if method not in method_mapping:
            raise ValueError(f"Invalid payment method: {method}")
        
        locator = method_mapping[method]
        self.click_element(locator)
        time.sleep(1)
        self.logger.info(f"Payment method selected: {method}")
    
    def click_pay_button(self):
        """Click Pay button in Personal Center popup"""
        self.click_element(self.PAY_BUTTON)
        self.logger.info("Clicked 确定 button")
        time.sleep(2)
        self.logger.info("Pay button clicked")
    
    def verify_success_message(self):
        """Verify success message appears"""
        success_msg = self.find_visible_element(self.SUCCESS_MESSAGE)
        assert "创建成功" in success_msg.text
        self.logger.info("✅ Success message verified")
        return True
    
    def verify_insufficient_balance_error(self):
        """Verify insufficient balance error message appears"""
        error_msg = self.find_visible_element(self.INSUFFICIENT_BALANCE_ERROR)
        assert "账户余额不足" in error_msg.text
        self.logger.info("✅ Insufficient balance error message verified")
        return True
    
    def close_wechat_popup(self):
        """Close WeChat QR popup"""
        self.click_element(self.WECHAT_POPUP_CLOSE)
        time.sleep(1)
        self.logger.info("WeChat popup closed")
    
    def verify_alipay_sandbox(self):
        """Verify Alipay sandbox opens"""
        self.switch_to_window()
        self.wait_for_url_change("alipaydev.com")
        assert "alipaydev.com" in self.get_current_url()
        self.logger.info("✅ Alipay sandbox verified")
        self.close_current_window()
        return True
    
    def create_paid_account_with_balance(self, package_name):
        """Complete paid account creation with balance payment"""
        self.click_add_paid_account()
        self.wait_for_package_popup()
        self.select_package_type(package_name, has_balance=True)
        self.input_random_account(has_balance=True)
        self.select_payment_method("余额")
        self.click_pay_button()
        return self.verify_success_message()
    
    def create_paid_account_with_alipay(self, package_name):
        """Complete paid account creation with Alipay payment"""
        self.click_add_paid_account()
        self.wait_for_package_popup()
        self.select_package_type(package_name, has_balance=True)
        self.input_random_account(has_balance=True)
        self.select_payment_method("支付宝")
        self.click_pay_button()
        return self.verify_alipay_sandbox()
    
    def create_paid_account_with_wechat(self, package_name):
        """Complete paid account creation with WeChat payment"""
        self.click_add_paid_account()
        self.wait_for_package_popup()
        self.select_package_type(package_name, has_balance=True)
        self.input_random_account(has_balance=True)
        self.select_payment_method("微信")
        self.click_pay_button()
        self.close_wechat_popup()
        return True
    
    def create_paid_account_no_balance(self, package_name):
        """Complete paid account creation when no balance"""
        self.click_add_paid_account()
        self.wait_for_package_popup()
        self.select_package_type(package_name, has_balance=False)
        self.input_random_account(has_balance=False)
        self.select_payment_method("余额")
        self.click_pay_button()
        return self.verify_insufficient_balance_error() 