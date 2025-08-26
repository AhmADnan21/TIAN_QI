from selenium.webdriver.common.by import By
from .base_page import BasePage
import time

class PackageOrderPage(BasePage):
    """Page object for the package order page"""
    
    # Package locators
    DYNAMIC_SUPREME_PACKAGE = (By.XPATH, "//div[contains(text(), '天启动态尊享')]")
    STATIC_IP_PACKAGE = (By.XPATH, "//div[contains(text(), '静态IP-天启')]")
    DYNAMIC_STANDARD_PACKAGE = (By.XPATH, "//div[contains(text(), '天启动态标准套餐')]")
    DYNAMIC_DEDICATED_PACKAGE = (By.XPATH, "//div[contains(text(), '天启动态独享套餐')]")
    
    # Purchase flow locators
    BUY_NOW_BUTTON = (By.XPATH, "//div[contains(text(), '立即购买')]")
    PAYMENT_METHOD_BALANCE = (By.XPATH, "//div[contains(text(), '余额')]")
    PAYMENT_METHOD_ALIPAY = (By.XPATH, "//div[contains(text(), '支付宝')]")
    PAYMENT_METHOD_WECHAT = (By.XPATH, "//div[contains(text(), '微信')]")
    PAY_NOW_BUTTON = (By.XPATH, "//div[contains(text(), '立即支付')]")
    RECHARGE_NOW_BUTTON = (By.XPATH, "//div[@class='buyBt hover text-center' and contains(text(), '立即充值')]")
    RECHARGE_NOW_BUTTON_FALLBACK = (By.XPATH, "//div[contains(text(), '立即充值')]")
    
    # Success/Error message locators
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(text(), '套餐购买成功')]")
    SUCCESS_POPUP_CLOSE = (By.XPATH, "//div[contains(@class, 'fee-header') and contains(text(), '×')]")
    WECHAT_QR_CODE = (By.XPATH, "//div[contains(text(), '微信扫码支付')]")
    WECHAT_POPUP_CLOSE = (By.XPATH, "//i[contains(@class, 'icon--x') and contains(@class, 'close-icon')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://test-ip-tianqi.cd.xiaoxigroup.net/packageOrder"
    
    def navigate_to_package_order(self):
        """Navigate to package order page"""
        if "/packageOrder" in self.get_current_url():
            self.logger.info("Already on package order page")
            return
        
        self.navigate_to(self.url)
        time.sleep(3)
        self.logger.info(f"After navigation, current URL: {self.get_current_url()}")
        
        # Check if redirected to login page
        if "/login" in self.get_current_url():
            self.logger.info("Redirected to login page, need to login again")
            return False
        return True
    
    def select_package(self, package_type):
        """Select package by type"""
        package_mapping = {
            "Dynamic Supreme": self.DYNAMIC_SUPREME_PACKAGE,
            "Static IP": self.STATIC_IP_PACKAGE,
            "Dynamic Standard": self.DYNAMIC_STANDARD_PACKAGE,
            "Dynamic Dedicated": self.DYNAMIC_DEDICATED_PACKAGE
        }
        
        if package_type not in package_mapping:
            raise ValueError(f"Invalid package type: {package_type}")
        
        locator = package_mapping[package_type]
        self.click_element(locator)
        time.sleep(2)
        self.logger.info(f"Selected package: {package_type}")
    
    def click_buy_now(self):
        """Click the Buy Now button"""
        self.click_element(self.BUY_NOW_BUTTON)
        time.sleep(1)
        self.logger.info("Clicked Buy Now button")
    
    def select_payment_method(self, method):
        """Select payment method"""
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
        self.logger.info(f"Selected payment method: {method}")
    
    def click_pay_now(self):
        """Click the Pay Now button"""
        self.click_element(self.PAY_NOW_BUTTON)
        time.sleep(2)
        self.logger.info("Clicked Pay Now button")
    
    def click_recharge_now(self):
        """Click the Recharge Now button (for no balance scenario)"""
        try:
            self.click_element(self.RECHARGE_NOW_BUTTON)
            self.logger.info("Found recharge button with specific class (no balance scenario)")
        except:
            self.click_element(self.RECHARGE_NOW_BUTTON_FALLBACK)
            self.logger.info("Found recharge button with general selector")
        
        time.sleep(2)
        self.logger.info("Clicked Recharge Now button")
    
    def wait_for_success_message(self):
        """Wait for success message to appear"""
        success_msg = self.find_visible_element(self.SUCCESS_MESSAGE)
        assert "套餐购买成功" in success_msg.text
        self.logger.info("✅ Success message verified")
        return True
    
    def close_success_popup(self):
        """Close the success popup"""
        self.click_element(self.SUCCESS_POPUP_CLOSE)
        time.sleep(1)
        self.logger.info("Success popup closed")
    
    def wait_for_wechat_qr(self):
        """Wait for WeChat QR code to appear"""
        qr_code = self.find_visible_element(self.WECHAT_QR_CODE)
        assert qr_code.is_displayed()
        self.logger.info("✅ WeChat QR code verified")
        return True
    
    def close_wechat_popup(self):
        """Close the WeChat QR popup"""
        self.click_element(self.WECHAT_POPUP_CLOSE)
        time.sleep(1)
        self.logger.info("WeChat QR popup closed")
    
    def verify_alipay_sandbox(self):
        """Verify Alipay sandbox opens"""
        self.switch_to_window()
        self.wait_for_url_change("alipaydev.com")
        assert "alipaydev.com" in self.get_current_url()
        self.logger.info("✅ Alipay sandbox verified")
        self.close_current_window()
        return True
    
    def verify_recharge_redirect(self):
        """Verify redirect to recharge page when no balance"""
        self.wait_for_url_change("tab=recharge")
        assert "tab=recharge" in self.get_current_url()
        self.logger.info("✅ Recharge redirect verified - no balance detected")
        return True
    
    def purchase_package_with_balance(self, package_type):
        """Complete purchase flow with balance payment"""
        self.select_package(package_type)
        self.click_buy_now()
        self.select_payment_method("余额")
        self.click_pay_now()
        self.wait_for_success_message()
        self.close_success_popup()
        return True
    
    def purchase_package_with_alipay(self, package_type):
        """Complete purchase flow with Alipay payment"""
        self.select_package(package_type)
        self.click_buy_now()
        self.select_payment_method("支付宝")
        self.click_pay_now()
        return self.verify_alipay_sandbox()
    
    def purchase_package_with_wechat(self, package_type):
        """Complete purchase flow with WeChat payment"""
        self.select_package(package_type)
        self.click_buy_now()
        self.select_payment_method("微信")
        self.click_pay_now()
        self.wait_for_wechat_qr()
        self.close_wechat_popup()
        return True
    
    def purchase_package_no_balance(self, package_type):
        """Complete purchase flow when no balance"""
        self.select_package(package_type)
        self.click_buy_now()
        self.select_payment_method("余额")
        self.click_recharge_now()
        return self.verify_recharge_redirect() 