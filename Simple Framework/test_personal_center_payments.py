import pytest
import time
import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ===== Configuration =====
LOGIN_URL = "https://test-ip-tianqi.cd.xiaoxigroup.net/login"
PERSONAL_CENTER_URL = "https://test-ip-tianqi.cd.xiaoxigroup.net/personal/accountManager"
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

def navigate_to_personal_center(driver, wait):
    """Navigate to Personal Center account manager page"""
    driver.get(PERSONAL_CENTER_URL)
    time.sleep(3)
    print(f"Navigated to Personal Center. Current URL: {driver.current_url}")

def click_add_paid_account(driver, wait):
    """Click the 添加付费账户 button"""
    add_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(), '添加付费账户')]")))
    driver.execute_script("arguments[0].click();", add_button)
    time.sleep(2)
    print("Clicked add paid account button")

def wait_for_package_popup(driver, wait):
    """Wait for the package selection popup to appear"""
    wait.until(EC.visibility_of_element_located((By.ID, "__BVID__66___BV_modal_header_")))
    time.sleep(5)
    print("Package selection popup appeared")

def select_package_type(driver, wait, package_name, dropdown_id="__BVID__548"):
    """Select package type in Personal Center popup"""
    dropdown = wait.until(EC.presence_of_element_located((By.ID, dropdown_id)))
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
        print(f"Selected {package_name} using Select class")
        time.sleep(1)
    else:
        raise Exception(f"Package name {package_name} not found in mapping")

def input_random_account(driver, wait, account_field_id="__BVID__552"):
    """Input random 8-character alphanumeric string in account field"""
    # Generate random 8-character alphanumeric string
    account = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    account_field = wait.until(EC.element_to_be_clickable((By.ID, account_field_id)))
    account_field.clear()
    account_field.send_keys(account)
    time.sleep(1)
    print(f"Entered account: {account}")

def select_payment_method_personal(driver, wait, method_name):
    """Select payment method in Personal Center popup"""
    method = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//div[contains(text(), '{method_name}')]")))
    driver.execute_script("arguments[0].click();", method)
    time.sleep(1)
    print(f"Selected payment method: {method_name}")

def click_pay_personal(driver, wait):
    """Click Pay button in Personal Center popup"""
    pay_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(text(), '确定')]")))
    driver.execute_script("arguments[0].click();", pay_button)
    print("Clicked 确定 button")
    time.sleep(2)
    print("Pay button clicked")

def verify_success_message(driver, wait):
    """Verify success message appears"""
    success_msg = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[contains(@class, 'ml-20') and contains(text(), '创建成功')]")))
    assert "创建成功" in success_msg.text
    print("✅ Success message verified")

def close_wechat_popup(driver, wait):
    """Close WeChat QR popup"""
    close_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//i[contains(@class, 'icon--x') and contains(@class, 'close-icon')]")))
    driver.execute_script("arguments[0].click();", close_button)
    time.sleep(1)
    print("WeChat popup closed")

def verify_alipay_sandbox(driver, wait):
    """Verify Alipay sandbox opens"""
    driver.switch_to.window(driver.window_handles[-1])
    wait.until(lambda d: "alipaydev.com" in d.current_url)
    assert "alipaydev.com" in driver.current_url
    print("✅ Alipay sandbox verified")
    # Switch back to main window
    driver.switch_to.window(driver.window_handles[0])

def verify_insufficient_balance_error(driver, wait):
    """Verify insufficient balance error message appears"""
    error_msg = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[contains(@class, 'ml-20') and contains(text(), '账户余额不足')]")))
    assert "账户余额不足" in error_msg.text
    print("✅ Insufficient balance error message verified")

# ===== Test Cases =====
class TestPersonalCenterDynamicSupreme:
    """Test cases for Dynamic Supreme package in Personal Center"""
    
    def test_balance_payment(self, driver, wait):
        """Test balance payment for Dynamic Supreme in Personal Center"""
        login_with_balance(driver, wait)
        navigate_to_personal_center(driver, wait)
        click_add_paid_account(driver, wait)
        wait_for_package_popup(driver, wait)
        select_package_type(driver, wait, "天启动态尊享")
        input_random_account(driver, wait)
        select_payment_method_personal(driver, wait, "余额")
        click_pay_personal(driver, wait)
        verify_success_message(driver, wait)
        print("✅ Personal Center Dynamic Supreme Balance test passed")
    
    def test_alipay_payment(self, driver, wait):
        """Test Alipay payment for Dynamic Supreme in Personal Center"""
        navigate_to_personal_center(driver, wait)
        click_add_paid_account(driver, wait)
        wait_for_package_popup(driver, wait)
        select_package_type(driver, wait, "天启动态尊享")
        input_random_account(driver, wait)
        select_payment_method_personal(driver, wait, "支付宝")
        click_pay_personal(driver, wait)
        verify_alipay_sandbox(driver, wait)
        print("✅ Personal Center Dynamic Supreme Alipay test passed")
    
    def test_wechat_payment(self, driver, wait):
        """Test WeChat payment for Dynamic Supreme in Personal Center"""
        navigate_to_personal_center(driver, wait)
        click_add_paid_account(driver, wait)
        wait_for_package_popup(driver, wait)
        select_package_type(driver, wait, "天启动态尊享")
        input_random_account(driver, wait)
        select_payment_method_personal(driver, wait, "微信")
        click_pay_personal(driver, wait)
        close_wechat_popup(driver, wait)
        print("✅ Personal Center Dynamic Supreme WeChat test passed")
    
    def test_no_balance(self, driver, wait):
        """Test wallet payment with no balance for Dynamic Supreme in Personal Center"""
        navigate_to_personal_center(driver, wait)
        click_add_paid_account(driver, wait)
        wait_for_package_popup(driver, wait)
        select_package_type(driver, wait, "天启动态尊享", "__BVID__98")
        input_random_account(driver, wait, "__BVID__102")
        select_payment_method_personal(driver, wait, "余额")
        click_pay_personal(driver, wait)
        verify_insufficient_balance_error(driver, wait)
        print("✅ Personal Center Dynamic Supreme Wallet No Balance test passed")

class TestPersonalCenterStaticIP:
    """Test cases for Static IP package in Personal Center"""
    
    def test_balance_payment(self, driver, wait):
        """Test balance payment for Static IP in Personal Center"""
        navigate_to_personal_center(driver, wait)
        click_add_paid_account(driver, wait)
        wait_for_package_popup(driver, wait)
        select_package_type(driver, wait, "静态IP-天启")
        input_random_account(driver, wait)
        select_payment_method_personal(driver, wait, "余额")
        click_pay_personal(driver, wait)
        verify_success_message(driver, wait)
        print("✅ Personal Center Static IP Balance test passed")
    
    def test_alipay_payment(self, driver, wait):
        """Test Alipay payment for Static IP in Personal Center"""
        navigate_to_personal_center(driver, wait)
        click_add_paid_account(driver, wait)
        wait_for_package_popup(driver, wait)
        select_package_type(driver, wait, "静态IP-天启")
        input_random_account(driver, wait)
        select_payment_method_personal(driver, wait, "支付宝")
        click_pay_personal(driver, wait)
        verify_alipay_sandbox(driver, wait)
        print("✅ Personal Center Static IP Alipay test passed")
    
    def test_wechat_payment(self, driver, wait):
        """Test WeChat payment for Static IP in Personal Center"""
        navigate_to_personal_center(driver, wait)
        click_add_paid_account(driver, wait)
        wait_for_package_popup(driver, wait)
        select_package_type(driver, wait, "静态IP-天启")
        input_random_account(driver, wait)
        select_payment_method_personal(driver, wait, "微信")
        click_pay_personal(driver, wait)
        close_wechat_popup(driver, wait)
        print("✅ Personal Center Static IP WeChat test passed")
    
    def test_no_balance(self, driver, wait):
        """Test wallet payment with no balance for Static IP in Personal Center"""
        navigate_to_personal_center(driver, wait)
        click_add_paid_account(driver, wait)
        wait_for_package_popup(driver, wait)
        select_package_type(driver, wait, "静态IP-天启", "__BVID__98")
        input_random_account(driver, wait, "__BVID__102")
        select_payment_method_personal(driver, wait, "余额")
        click_pay_personal(driver, wait)
        verify_insufficient_balance_error(driver, wait)
        print("✅ Personal Center Static IP Wallet No Balance test passed")

class TestPersonalCenterDynamicStandard:
    """Test cases for Dynamic Standard package in Personal Center"""
    
    def test_balance_payment(self, driver, wait):
        """Test balance payment for Dynamic Standard in Personal Center"""
        navigate_to_personal_center(driver, wait)
        click_add_paid_account(driver, wait)
        wait_for_package_popup(driver, wait)
        select_package_type(driver, wait, "天启动态标准套餐")
        input_random_account(driver, wait)
        select_payment_method_personal(driver, wait, "余额")
        click_pay_personal(driver, wait)
        verify_success_message(driver, wait)
        print("✅ Personal Center Dynamic Standard Balance test passed")
    
    def test_alipay_payment(self, driver, wait):
        """Test Alipay payment for Dynamic Standard in Personal Center"""
        navigate_to_personal_center(driver, wait)
        click_add_paid_account(driver, wait)
        wait_for_package_popup(driver, wait)
        select_package_type(driver, wait, "天启动态标准套餐")
        input_random_account(driver, wait)
        select_payment_method_personal(driver, wait, "支付宝")
        click_pay_personal(driver, wait)
        verify_alipay_sandbox(driver, wait)
        print("✅ Personal Center Dynamic Standard Alipay test passed")
    
    def test_wechat_payment(self, driver, wait):
        """Test WeChat payment for Dynamic Standard in Personal Center"""
        navigate_to_personal_center(driver, wait)
        click_add_paid_account(driver, wait)
        wait_for_package_popup(driver, wait)
        select_package_type(driver, wait, "天启动态标准套餐")
        input_random_account(driver, wait)
        select_payment_method_personal(driver, wait, "微信")
        click_pay_personal(driver, wait)
        close_wechat_popup(driver, wait)
        print("✅ Personal Center Dynamic Standard WeChat test passed")
    
    def test_no_balance(self, driver, wait):
        """Test wallet payment with no balance for Dynamic Standard in Personal Center"""
        navigate_to_personal_center(driver, wait)
        click_add_paid_account(driver, wait)
        wait_for_package_popup(driver, wait)
        select_package_type(driver, wait, "天启动态标准套餐", "__BVID__98")
        input_random_account(driver, wait, "__BVID__102")
        select_payment_method_personal(driver, wait, "余额")
        click_pay_personal(driver, wait)
        verify_insufficient_balance_error(driver, wait)
        print("✅ Personal Center Dynamic Standard Wallet No Balance test passed")

class TestPersonalCenterDynamicDedicated:
    """Test cases for Dynamic Dedicated package in Personal Center"""
    
    def test_balance_payment(self, driver, wait):
        """Test balance payment for Dynamic Dedicated in Personal Center"""
        navigate_to_personal_center(driver, wait)
        click_add_paid_account(driver, wait)
        wait_for_package_popup(driver, wait)
        select_package_type(driver, wait, "天启动态独享套餐")
        input_random_account(driver, wait)
        select_payment_method_personal(driver, wait, "余额")
        click_pay_personal(driver, wait)
        verify_success_message(driver, wait)
        print("✅ Personal Center Dynamic Dedicated Balance test passed")
    
    def test_alipay_payment(self, driver, wait):
        """Test Alipay payment for Dynamic Dedicated in Personal Center"""
        navigate_to_personal_center(driver, wait)
        click_add_paid_account(driver, wait)
        wait_for_package_popup(driver, wait)
        select_package_type(driver, wait, "天启动态独享套餐")
        input_random_account(driver, wait)
        select_payment_method_personal(driver, wait, "支付宝")
        click_pay_personal(driver, wait)
        verify_alipay_sandbox(driver, wait)
        print("✅ Personal Center Dynamic Dedicated Alipay test passed")
    
    def test_wechat_payment(self, driver, wait):
        """Test WeChat payment for Dynamic Dedicated in Personal Center"""
        navigate_to_personal_center(driver, wait)
        click_add_paid_account(driver, wait)
        wait_for_package_popup(driver, wait)
        select_package_type(driver, wait, "天启动态独享套餐")
        input_random_account(driver, wait)
        select_payment_method_personal(driver, wait, "微信")
        click_pay_personal(driver, wait)
        close_wechat_popup(driver, wait)
        print("✅ Personal Center Dynamic Dedicated WeChat test passed")
    
    def test_no_balance(self, driver, wait):
        """Test wallet payment with no balance for Dynamic Dedicated in Personal Center"""
        navigate_to_personal_center(driver, wait)
        click_add_paid_account(driver, wait)
        wait_for_package_popup(driver, wait)
        select_package_type(driver, wait, "天启动态独享套餐", "__BVID__98")
        input_random_account(driver, wait, "__BVID__102")
        select_payment_method_personal(driver, wait, "余额")
        click_pay_personal(driver, wait)
        verify_insufficient_balance_error(driver, wait)
        print("✅ Personal Center Dynamic Dedicated Wallet No Balance test passed") 