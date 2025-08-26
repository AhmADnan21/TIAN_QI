import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ===== Configuration =====
LOGIN_URL = "https://test-ip-tianqi.cd.xiaoxigroup.net/login"
PACKAGE_ORDER_URL = "https://test-ip-tianqi.cd.xiaoxigroup.net/packageOrder"
PHONE_WITH_BALANCE = "15332595364"
PHONE_WITHOUT_BALANCE = "15658873355"
PASSWORD = "Test@123"

# ===== Utility Functions =====
def login_with_balance(driver, wait):
    """Login with account that has balance"""
    print(f"Navigating to login page: {LOGIN_URL}")
    driver.get(LOGIN_URL)
    time.sleep(3)
    
    print(f"Current URL: {driver.current_url}")
    
    # Check if already logged in
    if "/packageOrder" in driver.current_url or driver.current_url == "https://test-ip-tianqi.cd.xiaoxigroup.net/":
        print("Already logged in or redirected to main page")
        return
    
    # Find and fill phone input
    phone_input = wait.until(EC.element_to_be_clickable((By.ID, "__BVID__23")))
    phone_input.clear()
    phone_input.send_keys(PHONE_WITH_BALANCE)
    print(f"Entered phone number: {PHONE_WITH_BALANCE}")
    
    # Find and fill password input
    password_input = wait.until(EC.element_to_be_clickable((By.ID, "__BVID__24")))
    password_input.clear()
    password_input.send_keys(PASSWORD)
    print("Entered password")
    
    # Click login button
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '登录')]")))
    driver.execute_script("arguments[0].click();", login_button)
    print("Clicked login button")
    
    time.sleep(5)
    print(f"After login click, current URL: {driver.current_url}")
    
    # Wait for redirect
    try:
        wait.until(lambda d: "/packageOrder" in d.current_url or d.current_url == "https://test-ip-tianqi.cd.xiaoxigroup.net/")
        print("✅ Successfully logged in")
    except TimeoutException:
        raise Exception("Login failed - no redirect to expected page")

def login_without_balance(driver, wait):
    """Login with account that has no balance"""
    print(f"Navigating to login page: {LOGIN_URL}")
    driver.get(LOGIN_URL)
    time.sleep(3)
    
    print(f"Current URL: {driver.current_url}")
    
    # Check if already logged in
    if "/packageOrder" in driver.current_url or driver.current_url == "https://test-ip-tianqi.cd.xiaoxigroup.net/":
        print("Already logged in or redirected to main page")
        return
    
    # Find and fill phone input
    phone_input = wait.until(EC.element_to_be_clickable((By.ID, "__BVID__23")))
    phone_input.clear()
    phone_input.send_keys(PHONE_WITHOUT_BALANCE)
    print(f"Entered phone number: {PHONE_WITHOUT_BALANCE}")
    
    # Find and fill password input
    password_input = wait.until(EC.element_to_be_clickable((By.ID, "__BVID__24")))
    password_input.clear()
    password_input.send_keys(PASSWORD)
    print("Entered password")
    
    # Click login button
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '登录')]")))
    driver.execute_script("arguments[0].click();", login_button)
    print("Clicked login button")
    
    time.sleep(5)
    print(f"After login click, current URL: {driver.current_url}")
    
    # Wait for redirect
    try:
        wait.until(lambda d: "/packageOrder" in d.current_url or d.current_url == "https://test-ip-tianqi.cd.xiaoxigroup.net/")
        print("✅ Successfully logged in")
    except TimeoutException:
        raise Exception("Login failed - no redirect to expected page")

def navigate_to_package_order(driver, wait):
    """Navigate to package order page"""
    print(f"Navigating to package order page")
    
    if "/packageOrder" in driver.current_url:
        print("Already on package order page")
        return
    
    driver.get(PACKAGE_ORDER_URL)
    time.sleep(3)
    
    print(f"After navigation, current URL: {driver.current_url}")
    
    if "/login" in driver.current_url:
        print("Redirected to login page, attempting login again...")
        login_with_balance(driver, wait)
        driver.get(PACKAGE_ORDER_URL)
        time.sleep(3)

def select_package(driver, wait, package_name):
    """Select a package by name"""
    package = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//div[contains(text(), '{package_name}')]")))
    driver.execute_script("arguments[0].click();", package)
    time.sleep(2)
    print(f"Selected package: {package_name}")

def click_buy_now(driver, wait):
    """Click Buy Now button"""
    buy_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(text(), '立即购买')]")))
    driver.execute_script("arguments[0].click();", buy_button)
    time.sleep(1)
    print("Clicked Buy Now button")

def select_payment_method(driver, wait, method_name):
    """Select payment method"""
    method = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//div[contains(text(), '{method_name}')]")))
    driver.execute_script("arguments[0].click();", method)
    time.sleep(1)
    print(f"Selected payment method: {method_name}")

def click_pay_now(driver, wait):
    """Click Pay Now button"""
    pay_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(text(), '立即支付')]")))
    driver.execute_script("arguments[0].click();", pay_button)
    time.sleep(2)
    print("Clicked Pay Now button")

def click_recharge_now(driver, wait):
    """Click Recharge Now button (no balance scenario)"""
    try:
        recharge_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='buyBt hover text-center' and contains(text(), '立即充值')]")))
        print("Found recharge button with specific class")
    except TimeoutException:
        recharge_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(), '立即充值')]")))
        print("Found recharge button with general selector")
    
    driver.execute_script("arguments[0].click();", recharge_button)
    time.sleep(2)
    print("Clicked Recharge Now button")

def close_success_popup(driver, wait):
    """Close success popup"""
    close_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class, 'fee-header') and contains(text(), '×')]")))
    driver.execute_script("arguments[0].click();", close_button)
    time.sleep(1)
    print("Success popup closed")

def close_wechat_popup(driver, wait):
    """Close WeChat QR popup"""
    close_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//i[contains(@class, 'icon--x') and contains(@class, 'close-icon')]")))
    driver.execute_script("arguments[0].click();", close_button)
    time.sleep(1)
    print("WeChat popup closed")

# ===== Test Cases =====
class TestDynamicSupreme:
    """Test cases for Dynamic Supreme package"""
    
    def test_balance_payment(self, driver, wait):
        """Test balance payment with sufficient funds"""
        login_with_balance(driver, wait)
        navigate_to_package_order(driver, wait)
        select_package(driver, wait, "天启动态尊享")
        click_buy_now(driver, wait)
        select_payment_method(driver, wait, "余额")
        click_pay_now(driver, wait)
        
        # Verify success popup
        success_msg = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(), '套餐购买成功')]")))
        assert "套餐购买成功" in success_msg.text
        close_success_popup(driver, wait)
        print("✅ Balance payment test passed")
    
    def test_alipay_payment(self, driver, wait):
        """Test Alipay payment flow"""
        navigate_to_package_order(driver, wait)
        select_package(driver, wait, "天启动态尊享")
        click_buy_now(driver, wait)
        select_payment_method(driver, wait, "支付宝")
        click_pay_now(driver, wait)
        
        # Verify Alipay sandbox
        driver.switch_to.window(driver.window_handles[-1])
        wait.until(lambda d: "alipaydev.com" in d.current_url)
        assert "alipaydev.com" in driver.current_url
        driver.switch_to.window(driver.window_handles[0])
        print("✅ Alipay payment test passed")
    
    def test_wechat_payment(self, driver, wait):
        """Test WeChat payment flow"""
        navigate_to_package_order(driver, wait)
        select_package(driver, wait, "天启动态尊享")
        click_buy_now(driver, wait)
        select_payment_method(driver, wait, "微信")
        click_pay_now(driver, wait)
        
        # Verify WeChat QR
        qr_code = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(), '微信扫码支付')]")))
        assert qr_code.is_displayed()
        close_wechat_popup(driver, wait)
        print("✅ WeChat payment test passed")
    
    def test_no_balance(self, driver, wait):
        """Test wallet payment with no balance"""
        login_without_balance(driver, wait)
        navigate_to_package_order(driver, wait)
        select_package(driver, wait, "天启动态尊享")
        click_buy_now(driver, wait)
        select_payment_method(driver, wait, "余额")
        click_recharge_now(driver, wait)
        
        # Verify recharge redirect
        wait.until(lambda d: "tab=recharge" in d.current_url)
        assert "tab=recharge" in driver.current_url
        print("✅ No balance test passed")

class TestStaticIP:
    """Test cases for Static IP package"""
    
    def test_balance_payment(self, driver, wait):
        """Test balance payment with sufficient funds"""
        navigate_to_package_order(driver, wait)
        select_package(driver, wait, "静态IP-天启")
        click_buy_now(driver, wait)
        select_payment_method(driver, wait, "余额")
        click_pay_now(driver, wait)
        
        # Verify success popup
        success_msg = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(), '套餐购买成功')]")))
        assert "套餐购买成功" in success_msg.text
        close_success_popup(driver, wait)
        print("✅ Balance payment test passed")
    
    def test_alipay_payment(self, driver, wait):
        """Test Alipay payment flow"""
        navigate_to_package_order(driver, wait)
        select_package(driver, wait, "静态IP-天启")
        click_buy_now(driver, wait)
        select_payment_method(driver, wait, "支付宝")
        click_pay_now(driver, wait)
        
        # Verify Alipay sandbox
        driver.switch_to.window(driver.window_handles[-1])
        wait.until(lambda d: "alipaydev.com" in d.current_url)
        assert "alipaydev.com" in driver.current_url
        driver.switch_to.window(driver.window_handles[0])
        print("✅ Alipay payment test passed")
    
    def test_wechat_payment(self, driver, wait):
        """Test WeChat payment flow"""
        navigate_to_package_order(driver, wait)
        select_package(driver, wait, "静态IP-天启")
        click_buy_now(driver, wait)
        select_payment_method(driver, wait, "微信")
        click_pay_now(driver, wait)
        
        # Verify WeChat QR
        qr_code = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(), '微信扫码支付')]")))
        assert qr_code.is_displayed()
        close_wechat_popup(driver, wait)
        print("✅ WeChat payment test passed")
    
    def test_no_balance(self, driver, wait):
        """Test wallet payment with no balance"""
        navigate_to_package_order(driver, wait)
        select_package(driver, wait, "静态IP-天启")
        click_buy_now(driver, wait)
        select_payment_method(driver, wait, "余额")
        click_recharge_now(driver, wait)
        
        # Verify recharge redirect
        wait.until(lambda d: "tab=recharge" in d.current_url)
        assert "tab=recharge" in driver.current_url
        print("✅ No balance test passed")

class TestDynamicStandard:
    """Test cases for Dynamic Standard package"""
    
    def test_balance_payment(self, driver, wait):
        """Test balance payment with sufficient funds"""
        navigate_to_package_order(driver, wait)
        select_package(driver, wait, "天启动态标准套餐")
        click_buy_now(driver, wait)
        select_payment_method(driver, wait, "余额")
        click_pay_now(driver, wait)
        
        # Verify success popup
        success_msg = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(), '套餐购买成功')]")))
        assert "套餐购买成功" in success_msg.text
        close_success_popup(driver, wait)
        print("✅ Balance payment test passed")
    
    def test_alipay_payment(self, driver, wait):
        """Test Alipay payment flow"""
        navigate_to_package_order(driver, wait)
        select_package(driver, wait, "天启动态标准套餐")
        click_buy_now(driver, wait)
        select_payment_method(driver, wait, "支付宝")
        click_pay_now(driver, wait)
        
        # Verify Alipay sandbox
        driver.switch_to.window(driver.window_handles[-1])
        wait.until(lambda d: "alipaydev.com" in d.current_url)
        assert "alipaydev.com" in driver.current_url
        driver.switch_to.window(driver.window_handles[0])
        print("✅ Alipay payment test passed")
    
    def test_wechat_payment(self, driver, wait):
        """Test WeChat payment flow"""
        navigate_to_package_order(driver, wait)
        select_package(driver, wait, "天启动态标准套餐")
        click_buy_now(driver, wait)
        select_payment_method(driver, wait, "微信")
        click_pay_now(driver, wait)
        
        # Verify WeChat QR
        qr_code = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(), '微信扫码支付')]")))
        assert qr_code.is_displayed()
        close_wechat_popup(driver, wait)
        print("✅ WeChat payment test passed")
    
    def test_no_balance(self, driver, wait):
        """Test wallet payment with no balance"""
        navigate_to_package_order(driver, wait)
        select_package(driver, wait, "天启动态标准套餐")
        click_buy_now(driver, wait)
        select_payment_method(driver, wait, "余额")
        click_recharge_now(driver, wait)
        
        # Verify recharge redirect
        wait.until(lambda d: "tab=recharge" in d.current_url)
        assert "tab=recharge" in driver.current_url
        print("✅ No balance test passed")

class TestDynamicDedicated:
    """Test cases for Dynamic Dedicated package"""
    
    def test_balance_payment(self, driver, wait):
        """Test balance payment with sufficient funds"""
        navigate_to_package_order(driver, wait)
        select_package(driver, wait, "天启动态独享套餐")
        click_buy_now(driver, wait)
        select_payment_method(driver, wait, "余额")
        click_pay_now(driver, wait)
        
        # Verify success popup
        success_msg = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(), '套餐购买成功')]")))
        assert "套餐购买成功" in success_msg.text
        close_success_popup(driver, wait)
        print("✅ Balance payment test passed")
    
    def test_alipay_payment(self, driver, wait):
        """Test Alipay payment flow"""
        navigate_to_package_order(driver, wait)
        select_package(driver, wait, "天启动态独享套餐")
        click_buy_now(driver, wait)
        select_payment_method(driver, wait, "支付宝")
        click_pay_now(driver, wait)
        
        # Verify Alipay sandbox
        driver.switch_to.window(driver.window_handles[-1])
        wait.until(lambda d: "alipaydev.com" in d.current_url)
        assert "alipaydev.com" in driver.current_url
        driver.switch_to.window(driver.window_handles[0])
        print("✅ Alipay payment test passed")
    
    def test_wechat_payment(self, driver, wait):
        """Test WeChat payment flow"""
        navigate_to_package_order(driver, wait)
        select_package(driver, wait, "天启动态独享套餐")
        click_buy_now(driver, wait)
        select_payment_method(driver, wait, "微信")
        click_pay_now(driver, wait)
        
        # Verify WeChat QR
        qr_code = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(), '微信扫码支付')]")))
        assert qr_code.is_displayed()
        close_wechat_popup(driver, wait)
        print("✅ WeChat payment test passed")
    
    def test_no_balance(self, driver, wait):
        """Test wallet payment with no balance"""
        navigate_to_package_order(driver, wait)
        select_package(driver, wait, "天启动态独享套餐")
        click_buy_now(driver, wait)
        select_payment_method(driver, wait, "余额")
        click_recharge_now(driver, wait)
        
        # Verify recharge redirect
        wait.until(lambda d: "tab=recharge" in d.current_url)
        assert "tab=recharge" in driver.current_url
        print("✅ No balance test passed") 