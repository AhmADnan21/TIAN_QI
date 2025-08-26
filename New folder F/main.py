"""
Main Execution Script
Demonstrates how to use the new automation framework
"""

import sys
import os
import logging
from pathlib import Path

# Add the framework directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from execution.test_execution_manager import TestExecutionManager
from config.test_data_config import PackageData, PaymentData
from selenium.webdriver.common.by import By

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('test_execution.log')
        ]
    )

def run_single_test_example():
    """Example of running a single test"""
    print("\n" + "="*60)
    print("SINGLE TEST EXAMPLE")
    print("="*60)
    
    with TestExecutionManager(browser_type="chrome", headless=False) as manager:
        # Define a simple test function
        def test_dynamic_supreme_balance_payment(framework, actions, test_case):
            try:
                # Login with balance
                actions.login_with_balance(test_case)
                
                # Select Dynamic Supreme package
                actions.select_package(PackageData.DYNAMIC_SUPREME, test_case)
                
                # Click buy now
                actions.click_buy_now(test_case)
                
                # Select balance payment
                actions.select_payment_method(PaymentData.BALANCE_PAYMENT, test_case)
                
                # Click pay now
                actions.click_pay_now(test_case)
                
                # Verify success popup
                with framework.track_step(test_case, "Verify Success", "Check purchase success message"):
                    success_msg = actions.element_helper.find_visible_element(
                        (By.XPATH, "//div[contains(text(), '套餐购买成功')]")
                    )
                    assert "套餐购买成功" in success_msg.text
                    
                    # Close success popup
                    with framework.track_step(test_case, "Close Success Popup", "Close the success popup"):
                        actions.element_helper.click_element(
                            (By.XPATH, "//div[contains(@class, 'fee-header') and contains(text(), '×')]"), 
                            use_js=True
                        )
                        actions.utility_helper.wait(1)
                
                return True
                
            except Exception as e:
                framework.logger.error(f"Test failed: {str(e)}")
                return False
        
        # Run the single test
        result = manager.run_single_test(
            test_dynamic_supreme_balance_payment,
            "Dynamic Supreme Balance Payment Test",
            "Test balance payment for Dynamic Supreme package"
        )
        
        print(f"Single test result: {'PASSED' if result else 'FAILED'}")
        
        # Generate report
        report_file = manager.generate_final_report()
        if report_file:
            print(f"Report generated: {report_file}")

def run_package_payment_tests_example():
    """Example of running package payment tests"""
    print("\n" + "="*60)
    print("PACKAGE PAYMENT TESTS EXAMPLE")
    print("="*60)
    
    with TestExecutionManager(browser_type="chrome", headless=False) as manager:
        # Run payment tests for Dynamic Supreme package
        results = manager.run_package_payment_tests(
            PackageData.DYNAMIC_SUPREME,
            [PaymentData.BALANCE_PAYMENT, PaymentData.ALIPAY_PAYMENT, PaymentData.WECHAT_PAYMENT]
        )
        
        print("Package Payment Tests Results:")
        print(f"  Total tests: {results['summary']['total']}")
        print(f"  Passed: {results['summary']['passed']}")
        print(f"  Failed: {results['summary']['failed']}")
        print(f"  Success rate: {results['summary']['success_rate']:.1f}%")
        
        # Generate report
        report_file = manager.generate_final_report()
        if report_file:
            print(f"Report generated: {report_file}")

def run_personal_center_tests_example():
    """Example of running personal center tests"""
    print("\n" + "="*60)
    print("PERSONAL CENTER TESTS EXAMPLE")
    print("="*60)
    
    with TestExecutionManager(browser_type="chrome", headless=False) as manager:
        # Run personal center tests for Static IP package
        results = manager.run_personal_center_tests(
            PackageData.STATIC_IP,
            [PaymentData.BALANCE_PAYMENT, PaymentData.ALIPAY_PAYMENT, PaymentData.WECHAT_PAYMENT]
        )
        
        print("Personal Center Tests Results:")
        print(f"  Total tests: {results['summary']['total']}")
        print(f"  Passed: {results['summary']['passed']}")
        print(f"  Failed: {results['summary']['failed']}")
        print(f"  Success rate: {results['summary']['success_rate']:.1f}%")
        
        # Generate report
        report_file = manager.generate_final_report()
        if report_file:
            print(f"Report generated: {report_file}")

def run_no_balance_tests_example():
    """Example of running no balance tests"""
    print("\n" + "="*60)
    print("NO BALANCE TESTS EXAMPLE")
    print("="*60)
    
    with TestExecutionManager(browser_type="chrome", headless=False) as manager:
        # Run no balance tests
        results = manager.run_no_balance_tests()
        
        print("No Balance Tests Results:")
        print(f"  Total tests: {results['summary']['total']}")
        print(f"  Passed: {results['summary']['passed']}")
        print(f"  Failed: {results['summary']['failed']}")
        print(f"  Success rate: {results['summary']['success_rate']:.1f}%")
        
        # Generate report
        report_file = manager.generate_final_report()
        if report_file:
            print(f"Report generated: {report_file}")

def run_complete_test_suite_example():
    """Example of running the complete test suite"""
    print("\n" + "="*60)
    print("COMPLETE TEST SUITE EXAMPLE")
    print("="*60)
    
    with TestExecutionManager(browser_type="chrome", headless=False) as manager:
        # Run complete test suite
        complete_results = manager.run_complete_test_suite()
        
        # Print overall summary
        overall_summary = complete_results.get("overall_summary", {})
        print("Complete Test Suite Results:")
        print(f"  Total tests: {overall_summary.get('total_tests', 0)}")
        print(f"  Passed: {overall_summary.get('total_passed', 0)}")
        print(f"  Failed: {overall_summary.get('total_failed', 0)}")
        print(f"  Success rate: {overall_summary.get('success_rate', 0):.1f}%")
        print(f"  Execution time: {overall_summary.get('execution_time', 'N/A')}")
        
        # Print detailed results by category
        for category, results in complete_results.items():
            if category != "overall_summary" and "summary" in results:
                summary = results["summary"]
                print(f"\n{category.upper()}:")
                print(f"  Total tests: {summary.get('total', 0)}")
                print(f"  Passed: {summary.get('passed', 0)}")
                print(f"  Failed: {summary.get('failed', 0)}")
                print(f"  Success rate: {summary.get('success_rate', 0):.1f}%")
        
        # Generate report
        report_file = manager.generate_final_report()
        if report_file:
            print(f"\nReport generated: {report_file}")

def main():
    """Main execution function"""
    setup_logging()
    
    print("="*60)
    print("AUTOMATION FRAMEWORK DEMONSTRATION")
    print("="*60)
    print("This script demonstrates the new automation framework capabilities.")
    print("Choose an option to run:")
    print("1. Single Test Example")
    print("2. Package Payment Tests Example")
    print("3. Personal Center Tests Example")
    print("4. No Balance Tests Example")
    print("5. Complete Test Suite Example")
    print("6. Run All Examples")
    print("0. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (0-6): ").strip()
            
            if choice == "0":
                print("Exiting...")
                break
            elif choice == "1":
                run_single_test_example()
            elif choice == "2":
                run_package_payment_tests_example()
            elif choice == "3":
                run_personal_center_tests_example()
            elif choice == "4":
                run_no_balance_tests_example()
            elif choice == "5":
                run_complete_test_suite_example()
            elif choice == "6":
                print("\nRunning all examples...")
                run_single_test_example()
                run_package_payment_tests_example()
                run_personal_center_tests_example()
                run_no_balance_tests_example()
                run_complete_test_suite_example()
            else:
                print("Invalid choice. Please enter a number between 0 and 6.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 