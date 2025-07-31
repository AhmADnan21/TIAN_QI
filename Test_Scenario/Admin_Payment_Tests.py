# ===== Imports =====
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pytest
import os
import time
from datetime import datetime
import logging
import sys
import traceback
import random
import string
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_reports.test_report import TestReport, TestCase, TestStep, track_step, create_test_case

# ===== Global Configuration =====
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)  # Increased timeout for admin panel
driver.maximize_window()

report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")

# ===== Admin Panel Configuration =====
SSO_LOGIN_URL = "https://sso.xiaoxitech.com/login?project=fztpumkh&cb=https%3A%2F%2Ftest-admin-shenlong.cd.xiaoxigroup.net%2Flogin"
USER_DETAIL_URL = "https://test-admin-shenlong.cd.xiaoxigroup.net/client/userDetail?userId=10711&roles=300&show=false&brand=2"
USERNAME = "khordichze"
PASSWORD = "zxXI@16981098"

# ===== Package Mapping =====
PACKAGE_MAPPING = {
    "天启动态尊享": "天启动态尊享",
    "静态IP-天启": "静态IP-天启", 
    "天启动态标准套餐": "天启动态标准套餐",
    "天启动态独享套餐": "天启动态独享套餐"
}

# ===== Package Arrow Key Mapping =====
PACKAGE_ARROW_MAPPING = {
    "天启动态尊享": 2,
    "天启动态标准套餐": 6,
    "天启动态独享套餐": 7
}

# ===== Utility Functions =====
def create_report_dir():
    """Creates a unique report directory with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_dir = os.path.join(report_dir, f"Admin_Payment_Tests_{timestamp}")
    os.makedirs(test_dir, exist_ok=True)
    return test_dir

def login_to_admin_panel(test_case):
    """Login to admin panel using username and password with manual captcha"""
    with track_step(test_case, "Admin Login", "Login to admin panel using username/password"):
        try:
            print("Navigating to SSO login page...")
            driver.get(SSO_LOGIN_URL)
            time.sleep(3)
            
            # Step 1: Click on username/password login option
            try:
                username_login_btn = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//span[contains(text(), '用户名密码登录')]")))
                driver.execute_script("arguments[0].click();", username_login_btn)
                print("✅ Clicked on username/password login")
                time.sleep(2)
            except Exception as e:
                print(f"❌ Failed to click username/password login: {str(e)}")
                return False
            
            # Step 2: Enter username
            try:
                username_field = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//input[@type='text' and @placeholder='用户名' and @class='el-input__inner']")))
                username_field.clear()
                username_field.send_keys(USERNAME)
                print(f"✅ Entered username: {USERNAME}")
                time.sleep(1)
            except Exception as e:
                print(f"❌ Failed to enter username: {str(e)}")
                return False
            
            # Step 3: Enter password
            try:
                password_field = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//input[@type='password' and @placeholder='密码' and @class='el-input__inner']")))
                password_field.clear()
                password_field.send_keys(PASSWORD)
                print("✅ Entered password")
                time.sleep(1)
            except Exception as e:
                print(f"❌ Failed to enter password: {str(e)}")
                return False
            
            # Step 4: Click on captcha field and wait for manual input
            print("Handling captcha...")
            try:
                captcha_field = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//input[@type='text' and @placeholder='验证码' and @class='el-input__inner']")))
                driver.execute_script("arguments[0].click();", captcha_field)
                
                # Wait up to 15 minutes for user to complete captcha and login
                max_wait_time = 900  # 15 minutes
                start_time = time.time()
                last_url = driver.current_url
                
                while time.time() - start_time < max_wait_time:
                    current_url = driver.current_url
                    
                    # Only log URL if it has changed
                    if current_url != last_url:
                        print(f"Current URL: {current_url}")
                        last_url = current_url
                    
                    # Check if we've been redirected to admin panel
                    if "test-admin-shenlong.cd.xiaoxigroup.net/sellerIndex" in current_url:
                        print("✅ Successfully logged in to admin panel!")
                        return True
                    
                    time.sleep(10)
                
                print("❌ Login failed - timeout waiting for manual captcha completion")
                return False
                
            except Exception as e:
                print(f"❌ Failed to handle captcha: {str(e)}")
                return False
                
        except Exception as e:
            return False

def navigate_to_user_detail(test_case):
    """Navigate to user detail page"""
    with track_step(test_case, "Navigate to User Detail", "Navigate to user detail page"):
        try:
            print(f"Navigating to 流量业务管理后台 page")
            driver.get(USER_DETAIL_URL)
            time.sleep(5)  # Increased wait time for page load
            
            print(f"Current URL: {driver.current_url}")
            
            # Verify we're on the user detail page
            if "userDetail" in driver.current_url:
                print("✅ Successfully navigated to user detail page")
                return True
            else:
                print("❌ Navigation failed - not on user detail page")
                return False
                
        except Exception as e:
            return False

def click_add_vpn_button(test_case):
    """Click the 添加VPN button"""
    with track_step(test_case, "Click Add VPN", "Click 添加VPN button"):
        try:
            # Try to find button by text first
            add_vpn_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(), '添加VPN')]")))
            print("Found 添加VPN button by text")
            driver.execute_script("arguments[0].click();", add_vpn_button)
            print("Clicked 添加VPN button")
            time.sleep(3)
            return True
            
        except TimeoutException:
            # Fallback to full XPath
            try:
                add_vpn_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/button[6]/span")))
                print("Found 添加VPN button by XPath")
                driver.execute_script("arguments[0].click();", add_vpn_button)
                print("Clicked 添加VPN button")
                time.sleep(3)
                return True
                
            except Exception as e:
                print(f"Failed to click 添加VPN button: {str(e)}")
                return False

def wait_for_add_vpn_popup(test_case):
    """Wait for the 添加VPN popup to appear"""
    with track_step(test_case, "Wait for Popup", "Wait for 添加VPN popup to appear"):
        try:
            # Wait for popup title
            popup_title = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//span[@class='el-dialog__title' and contains(text(), '添加VPN')]")))
            print("✅ 添加VPN popup appeared")
            time.sleep(2)
            return True
            
        except TimeoutException:
            # Fallback to full XPath
            try:
                popup_title = wait.until(EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div/div[2]/div/div[3]/div/div[1]/span")))
                print("✅ 添加VPN popup appeared (XPath)")
                time.sleep(2)
                return True
                
            except Exception as e:
                print(f"Failed to find 添加VPN popup: {str(e)}")
                return False

def select_package_type(package_name, test_case):
    """Select package type from dropdown using arrow key navigation"""
    with track_step(test_case, "Select Package Type", f"Select {package_name} using arrow keys"):
        try:
            # Validate package name
            if package_name not in PACKAGE_MAPPING:
                raise Exception(f"Package name {package_name} not found in mapping")
            
            # 1. Click the dropdown to open it
            dropdown = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//input[@placeholder='请选择套餐类型' or contains(@placeholder, '套餐')]")))
            dropdown.click()
            time.sleep(2)  # Give time for the dropdown to render

            # 2. Use arrow key navigation based on package
            action = ActionChains(driver)
            
            if package_name == "静态IP-天启":
                # Default package - no action needed
                print("✅ Default package selected (静态IP-天启) - no action needed")
                return True
                
            elif package_name in PACKAGE_ARROW_MAPPING:
                # Use arrow keys to navigate to the desired option
                arrow_count = PACKAGE_ARROW_MAPPING[package_name]
                print(f"Navigating to {package_name} using {arrow_count} arrow down presses...")
                
                for i in range(arrow_count):
                    action.send_keys(Keys.ARROW_DOWN).perform()
                    time.sleep(0.3)  # Small delay between arrow presses
                
                # Press Enter to select the option
                action.send_keys(Keys.ENTER).perform()
                time.sleep(2)  # Wait for selection to register
                
                print(f"✅ Selected package: {package_name} using arrow keys")
                return True
                
            else:
                raise Exception(f"Package {package_name} not handled in arrow key logic")

        except TimeoutException as e:
            print(f"Timeout selecting package {package_name}: {str(e)}")
            return False
        except Exception as e:
            print(f"Failed to select package {package_name}: {str(e)}")
            return False

def input_random_username(test_case):
    """Input random 8-character alphanumeric string in username field"""
    with track_step(test_case, "Input Username", "Input random 8-character username"):
        try:
            # Generate random 8-character alphanumeric string
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            
            # Find username field using the correct XPath
            username_field = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/div/div[3]/div/div[2]/form/div/div[5]/div/div/div/div/div[1]/input")))
            username_field.clear()
            username_field.send_keys(username)
            time.sleep(1)
            print(f"Entered username: {username}")
            return True
            
        except Exception as e:
            print(f"Failed to input username: {str(e)}")
            return False

def select_payment_type(payment_type, test_case):
    """Select payment type (Pending Order or Balance Payment)"""
    with track_step(test_case, "Select Payment Type", f"Select {payment_type}"):
        try:
            if payment_type == "生成待支付订单":
                # Select Pending Order option
                pending_option = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//span[@class='el-radio__label' and contains(text(), '生成待支付订单')]")))
                driver.execute_script("arguments[0].click();", pending_option)
                print("Selected: 生成待支付订单")
                
            elif payment_type == "用户余额抵扣":
                # Select Balance Payment option
                balance_option = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//span[@class='el-radio__label' and contains(text(), '用户余额抵扣')]")))
                driver.execute_script("arguments[0].click();", balance_option)
                print("Selected: 用户余额抵扣")
                
            time.sleep(1)
            return True
            
        except Exception as e:
                print(f"Failed to select payment type {payment_type}: {str(e)}")
                return False

def click_confirm_button(test_case):
    """Click the 确定 (Confirm) button"""
    with track_step(test_case, "Click Confirm", "Click 确定 button"):
        try:
            confirm_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div[2]/div/div[3]/div/div[3]/div/button[2]/span")))
            driver.execute_script("arguments[0].click();", confirm_button)
            print("Clicked 确定 button")
            time.sleep(0.5)
            return True
                
        except Exception as e:
            print(f"Failed to click 确定 button: {str(e)}")
            return False

def verify_success_message(test_case):
    """Verify that a success message appears"""
    with track_step(test_case, "Verify Success", "Check for success message"):
        try:
            # Wait for the specific success message "添加成功" using the correct XPath
            success_msg = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/p")))
            if "添加成功" in success_msg.text:
                print(f"✅ Success message found: {success_msg.text}")
                return True
            else:
                print(f"❌ Unexpected message found: {success_msg.text}")
                return False
            
        except TimeoutException:
            print("❌ No success message found")
            return False
        except Exception as e:
            print(f"Failed to verify success message: {str(e)}")
            return False

# ===== Test Cases =====
def test_dynamic_supreme_pending_order(report_dir, test_case):
    """Test Dynamic Supreme with Pending Order payment"""
    test_case.start()
    try:
        navigate_to_user_detail(test_case)
        click_add_vpn_button(test_case)
        wait_for_add_vpn_popup(test_case)
        select_package_type("天启动态尊享", test_case)
        input_random_username(test_case)
        select_payment_type("生成待支付订单", test_case)
        click_confirm_button(test_case)
        verify_success_message(test_case)
        return True
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_dynamic_supreme_balance_payment(report_dir, test_case):
    """Test Dynamic Supreme with Balance Payment"""
    test_case.start()
    try:
        navigate_to_user_detail(test_case)
        click_add_vpn_button(test_case)
        wait_for_add_vpn_popup(test_case)
        select_package_type("天启动态尊享", test_case)
        input_random_username(test_case)
        select_payment_type("用户余额抵扣", test_case)
        click_confirm_button(test_case)
        verify_success_message(test_case)
        return True
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_dynamic_dedicated_pending_order(report_dir, test_case):
    """Test Dynamic Dedicated with Pending Order payment"""
    test_case.start()
    try:
        navigate_to_user_detail(test_case)
        click_add_vpn_button(test_case)
        wait_for_add_vpn_popup(test_case)
        select_package_type("天启动态独享套餐", test_case)
        input_random_username(test_case)
        select_payment_type("生成待支付订单", test_case)
        click_confirm_button(test_case)
        verify_success_message(test_case)
        return True
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_dynamic_dedicated_balance_payment(report_dir, test_case):
    """Test Dynamic Dedicated with Balance Payment"""
    test_case.start()
    try:
        navigate_to_user_detail(test_case)
        click_add_vpn_button(test_case)
        wait_for_add_vpn_popup(test_case)
        select_package_type("天启动态独享套餐", test_case)
        input_random_username(test_case)
        select_payment_type("用户余额抵扣", test_case)
        click_confirm_button(test_case)
        verify_success_message(test_case)
        return True
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_static_premium_pending_order(report_dir, test_case):
    """Test Static Premium with Pending Order payment"""
    test_case.start()
    try:
        navigate_to_user_detail(test_case)
        click_add_vpn_button(test_case)
        wait_for_add_vpn_popup(test_case)
        select_package_type("静态IP-天启", test_case)
        input_random_username(test_case)
        select_payment_type("生成待支付订单", test_case)
        click_confirm_button(test_case)
        verify_success_message(test_case)
        return True
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_static_premium_balance_payment(report_dir, test_case):
    """Test Static Premium with Balance Payment"""
    test_case.start()
    try:
        navigate_to_user_detail(test_case)
        click_add_vpn_button(test_case)
        wait_for_add_vpn_popup(test_case)
        select_package_type("静态IP-天启", test_case)
        input_random_username(test_case)
        select_payment_type("用户余额抵扣", test_case)
        click_confirm_button(test_case)
        verify_success_message(test_case)
        return True
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_fixed_long_term_pending_order(report_dir, test_case):
    """Test Fixed Long-Term with Pending Order payment"""
    test_case.start()
    try:
        navigate_to_user_detail(test_case)
        click_add_vpn_button(test_case)
        wait_for_add_vpn_popup(test_case)
        select_package_type("天启动态标准套餐", test_case)
        input_random_username(test_case)
        select_payment_type("生成待支付订单", test_case)
        click_confirm_button(test_case)
        verify_success_message(test_case)
        return True
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

def test_fixed_long_term_balance_payment(report_dir, test_case):
    """Test Fixed Long-Term with Balance Payment"""
    test_case.start()
    try:
        navigate_to_user_detail(test_case)
        click_add_vpn_button(test_case)
        wait_for_add_vpn_popup(test_case)
        select_package_type("天启动态标准套餐", test_case)
        input_random_username(test_case)
        select_payment_type("用户余额抵扣", test_case)
        click_confirm_button(test_case)
        verify_success_message(test_case)
        return True
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False
    finally:
        test_case.complete()

# ===== Main Execution =====
def main():
    report_dir = create_report_dir()
    test_report = TestReport(report_dir)
    test_report.start()

    test_results = {
        "1.1_dynamic_supreme_pending": False,
        "1.2_dynamic_supreme_balance": False,
        "2.1_dynamic_dedicated_pending": False,
        "2.2_dynamic_dedicated_balance": False,
        "3.1_static_premium_pending": False,
        "3.2_static_premium_balance": False,
        "4.1_fixed_long_term_pending": False,
        "4.2_fixed_long_term_balance": False
    }
    
    login_success = False

    try:
        # First, attempt to login to admin panel
        print("\n" + "="*60)
        print("ADMIN PANEL LOGIN")
        print("="*60)
        
        login_test_case = create_test_case("Admin Panel Login", "Login to admin panel using token URL")
        login_success = login_to_admin_panel(login_test_case)
        test_report.add_test_case(login_test_case)
        
        # If login fails, stop all testing
        if not login_success:
            print("\n❌ LOGIN FAILED - STOPPING ALL TESTS")
            print("Cannot proceed with testing without successful login")
            return
        
        print("\n✅ LOGIN SUCCESSFUL - PROCEEDING WITH TESTS")
        
        # 1. Dynamic Supreme Tests
        print("\n" + "="*60)
        print("1. DYNAMIC SUPREME TESTS")
        print("="*60)
        
        # 1.1 Pending Order Payment Test
        print("\n--- 1.1 Pending Order Payment Test ---")
        test_case1 = create_test_case("1.1 Dynamic Supreme - Pending Order", "Test Dynamic Supreme with Pending Order payment")
        test_results["1.1_dynamic_supreme_pending"] = test_dynamic_supreme_pending_order(report_dir, test_case1)
        test_report.add_test_case(test_case1)

        # 1.2 Balance Payment Test
        print("\n--- 1.2 Balance Payment Test ---")
        test_case2 = create_test_case("1.2 Dynamic Supreme - Balance Payment", "Test Dynamic Supreme with Balance Payment")
        test_results["1.2_dynamic_supreme_balance"] = test_dynamic_supreme_balance_payment(report_dir, test_case2)
        test_report.add_test_case(test_case2)

        # 2. Dynamic Dedicated Tests
        print("\n" + "="*60)
        print("2. DYNAMIC DEDICATED TESTS")
        print("="*60)
        
        # 2.1 Pending Order Payment Test
        print("\n--- 2.1 Pending Order Payment Test ---")
        test_case3 = create_test_case("2.1 Dynamic Dedicated - Pending Order", "Test Dynamic Dedicated with Pending Order payment")
        test_results["2.1_dynamic_dedicated_pending"] = test_dynamic_dedicated_pending_order(report_dir, test_case3)
        test_report.add_test_case(test_case3)

        # 2.2 Balance Payment Test
        print("\n--- 2.2 Balance Payment Test ---")
        test_case4 = create_test_case("2.2 Dynamic Dedicated - Balance Payment", "Test Dynamic Dedicated with Balance Payment")
        test_results["2.2_dynamic_dedicated_balance"] = test_dynamic_dedicated_balance_payment(report_dir, test_case4)
        test_report.add_test_case(test_case4)

        # 3. Static Premium Tests
        print("\n" + "="*60)
        print("3. STATIC PREMIUM TESTS")
        print("="*60)
        
        # 3.1 Pending Order Payment Test
        print("\n--- 3.1 Pending Order Payment Test ---")
        test_case5 = create_test_case("3.1 Static Premium - Pending Order", "Test Static Premium with Pending Order payment")
        test_results["3.1_static_premium_pending"] = test_static_premium_pending_order(report_dir, test_case5)
        test_report.add_test_case(test_case5)

        # 3.2 Balance Payment Test
        print("\n--- 3.2 Balance Payment Test ---")
        test_case6 = create_test_case("3.2 Static Premium - Balance Payment", "Test Static Premium with Balance Payment")
        test_results["3.2_static_premium_balance"] = test_static_premium_balance_payment(report_dir, test_case6)
        test_report.add_test_case(test_case6)

        # 4. Fixed Long-Term Tests
        print("\n" + "="*60)
        print("4. FIXED LONG-TERM TESTS")
        print("="*60)
        
        # 4.1 Pending Order Payment Test
        print("\n--- 4.1 Pending Order Payment Test ---")
        test_case7 = create_test_case("4.1 Fixed Long-Term - Pending Order", "Test Fixed Long-Term with Pending Order payment")
        test_results["4.1_fixed_long_term_pending"] = test_fixed_long_term_pending_order(report_dir, test_case7)
        test_report.add_test_case(test_case7)

        # 4.2 Balance Payment Test
        print("\n--- 4.2 Balance Payment Test ---")
        test_case8 = create_test_case("4.2 Fixed Long-Term - Balance Payment", "Test Fixed Long-Term with Balance Payment")
        test_results["4.2_fixed_long_term_balance"] = test_fixed_long_term_balance_payment(report_dir, test_case8)
        test_report.add_test_case(test_case8)

    finally:
        test_report.complete()
        driver.quit()
        
        # Print final results in organized format
        print("\n" + "="*60)
        print("FINAL TEST RESULTS")
        print("="*60)
        
        # Check if any tests were actually run
        if not any(test_results.values()) and not login_success:
            print("\n❌ NO TESTS EXECUTED - LOGIN FAILED")
            print("All tests were skipped due to login failure")
            report_file = test_report.generate_html_report()
            print(f"\nLogin failure report generated: {report_file}")
            return
        
        print("\n1. DYNAMIC SUPREME:")
        print(f"   1.1 Pending Order Payment Test: {'✅ PASSED' if test_results['1.1_dynamic_supreme_pending'] else '❌ FAILED'}")
        print(f"   1.2 Balance Payment Test: {'✅ PASSED' if test_results['1.2_dynamic_supreme_balance'] else '❌ FAILED'}")
        
        print("\n2. DYNAMIC DEDICATED:")
        print(f"   2.1 Pending Order Payment Test: {'✅ PASSED' if test_results['2.1_dynamic_dedicated_pending'] else '❌ FAILED'}")
        print(f"   2.2 Balance Payment Test: {'✅ PASSED' if test_results['2.2_dynamic_dedicated_balance'] else '❌ FAILED'}")
        
        print("\n3. STATIC PREMIUM:")
        print(f"   3.1 Pending Order Payment Test: {'✅ PASSED' if test_results['3.1_static_premium_pending'] else '❌ FAILED'}")
        print(f"   3.2 Balance Payment Test: {'✅ PASSED' if test_results['3.2_static_premium_balance'] else '❌ FAILED'}")
        
        print("\n4. FIXED LONG-TERM:")
        print(f"   4.1 Pending Order Payment Test: {'✅ PASSED' if test_results['4.1_fixed_long_term_pending'] else '❌ FAILED'}")
        print(f"   4.2 Balance Payment Test: {'✅ PASSED' if test_results['4.2_fixed_long_term_balance'] else '❌ FAILED'}")
        
        # Calculate summary
        passed_count = sum(1 for result in test_results.values() if result)
        total_count = len(test_results)
        
        print(f"\nSUMMARY: {passed_count}/{total_count} tests passed")
        
        report_file = test_report.generate_html_report()
        print(f"\nDetailed report generated: {report_file}")

if __name__ == "__main__":
    main() 