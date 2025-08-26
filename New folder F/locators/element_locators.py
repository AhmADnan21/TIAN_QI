"""
Element Locators
Structured locators for login, package, payment, personal center, navigation, tables
"""

from selenium.webdriver.common.by import By

# ===== Login Page Locators =====
class LoginPageLocators:
    """Locators for login page elements"""
    
    # Input Fields
    PHONE_INPUT = (By.ID, "__BVID__23")
    PASSWORD_INPUT = (By.ID, "__BVID__24")
    
    # Buttons
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), '登录')]")
    REGISTER_BUTTON = (By.XPATH, "//button[contains(text(), '注册')]")
    FORGOT_PASSWORD_BUTTON = (By.XPATH, "//a[contains(text(), '忘记密码')]")
    
    # Messages
    ERROR_MESSAGE = (By.XPATH, "//div[contains(text(), '错误') or contains(text(), 'error') or contains(text(), '失败')]")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(text(), '登录成功')]")
    
    # Navigation
    LOGIN_FORM = (By.CLASS_NAME, "login-form")
    LOGIN_CONTAINER = (By.CLASS_NAME, "login-container")

# ===== Package Order Page Locators =====
class PackageOrderPageLocators:
    """Locators for package order page elements"""
    
    # Package Selection
    DYNAMIC_SUPREME_PACKAGE = (By.XPATH, "//div[contains(text(), '天启动态尊享')]")
    STATIC_IP_PACKAGE = (By.XPATH, "//div[contains(text(), '静态IP-天启')]")
    DYNAMIC_STANDARD_PACKAGE = (By.XPATH, "//div[contains(text(), '天启动态标准套餐')]")
    DYNAMIC_DEDICATED_PACKAGE = (By.XPATH, "//div[contains(text(), '天启动态独享套餐')]")
    
    # Action Buttons
    BUY_NOW_BUTTON = (By.XPATH, "//div[contains(text(), '立即购买')]")
    PAY_NOW_BUTTON = (By.XPATH, "//div[contains(text(), '立即支付')]")
    RECHARGE_NOW_BUTTON = (By.XPATH, "//div[contains(text(), '立即充值')]")
    RECHARGE_BUTTON_NO_BALANCE = (By.XPATH, "//div[@class='buyBt hover text-center' and contains(text(), '立即充值')]")
    
    # Payment Methods
    BALANCE_PAYMENT = (By.XPATH, "//div[contains(text(), '余额')]")
    ALIPAY_PAYMENT = (By.XPATH, "//div[contains(text(), '支付宝')]")
    WECHAT_PAYMENT = (By.XPATH, "//div[contains(text(), '微信')]")
    
    # Messages
    SUCCESS_POPUP = (By.XPATH, "//div[contains(text(), '套餐购买成功')]")
    SUCCESS_POPUP_CLOSE = (By.XPATH, "//div[contains(@class, 'fee-header') and contains(text(), '×')]")
    
    # WeChat QR
    WECHAT_QR_CODE = (By.XPATH, "//div[contains(text(), '微信扫码支付')]")
    WECHAT_POPUP_CLOSE = (By.XPATH, "//i[contains(@class, 'icon--x') and contains(@class, 'close-icon')]")
    
    # Page Elements
    PACKAGE_CONTAINER = (By.CLASS_NAME, "package-container")
    PAYMENT_POPUP = (By.CLASS_NAME, "payment-popup")

# ===== Personal Center Page Locators =====
class PersonalCenterPageLocators:
    """Locators for personal center page elements"""
    
    # Navigation
    ACCOUNT_MANAGER_TAB = (By.XPATH, "//a[contains(text(), '账户管理')]")
    RECHARGE_TAB = (By.XPATH, "//a[contains(text(), '充值')]")
    
    # Account Management
    ADD_PAID_ACCOUNT_BUTTON = (By.XPATH, "//button[contains(text(), '添加付费账户')]")
    PACKAGE_SELECTION_POPUP = (By.ID, "__BVID__66___BV_modal_header_")
    
    # Package Selection Dropdowns
    PACKAGE_DROPDOWN_WITH_BALANCE = (By.ID, "__BVID__548")
    PACKAGE_DROPDOWN_NO_BALANCE = (By.ID, "__BVID__98")
    
    # Account Input Fields
    ACCOUNT_INPUT_WITH_BALANCE = (By.ID, "__BVID__552")
    ACCOUNT_INPUT_NO_BALANCE = (By.ID, "__BVID__102")
    
    # Payment Methods (same as package order)
    BALANCE_PAYMENT = (By.XPATH, "//div[contains(text(), '余额')]")
    ALIPAY_PAYMENT = (By.XPATH, "//div[contains(text(), '支付宝')]")
    WECHAT_PAYMENT = (By.XPATH, "//div[contains(text(), '微信')]")
    
    # Action Buttons
    PAY_BUTTON = (By.XPATH, "//div[contains(text(), '确定')]")
    
    # Messages
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'ml-20') and contains(text(), '创建成功')]")
    INSUFFICIENT_BALANCE_ERROR = (By.XPATH, "//div[contains(@class, 'ml-20') and contains(text(), '账户余额不足')]")
    
    # WeChat QR (same as package order)
    WECHAT_QR_CODE = (By.XPATH, "//div[contains(text(), '微信扫码支付')]")
    WECHAT_POPUP_CLOSE = (By.XPATH, "//i[contains(@class, 'icon--x') and contains(@class, 'close-icon')]")

# ===== Navigation Locators =====
class NavigationLocators:
    """Locators for navigation elements"""
    
    # Main Navigation
    HOME_LINK = (By.XPATH, "//a[contains(text(), '首页')]")
    PACKAGE_ORDER_LINK = (By.XPATH, "//a[contains(text(), '套餐订购')]")
    PERSONAL_CENTER_LINK = (By.XPATH, "//a[contains(text(), '个人中心')]")
    
    # User Menu
    USER_MENU = (By.CLASS_NAME, "user-menu")
    LOGOUT_BUTTON = (By.XPATH, "//a[contains(text(), '退出登录')]")
    PROFILE_BUTTON = (By.XPATH, "//a[contains(text(), '个人资料')]")
    
    # Breadcrumbs
    BREADCRUMB_CONTAINER = (By.CLASS_NAME, "breadcrumb")
    BREADCRUMB_ITEMS = (By.CLASS_NAME, "breadcrumb-item")

# ===== Table Locators =====
class TableLocators:
    """Locators for table elements"""
    
    # Account Table
    ACCOUNT_TABLE = (By.CLASS_NAME, "account-table")
    ACCOUNT_TABLE_ROWS = (By.XPATH, "//table[@class='account-table']//tr")
    ACCOUNT_TABLE_HEADERS = (By.XPATH, "//table[@class='account-table']//th")
    
    # Package Table
    PACKAGE_TABLE = (By.CLASS_NAME, "package-table")
    PACKAGE_TABLE_ROWS = (By.XPATH, "//table[@class='package-table']//tr")
    PACKAGE_TABLE_HEADERS = (By.XPATH, "//table[@class='package-table']//th")
    
    # Payment Table
    PAYMENT_TABLE = (By.CLASS_NAME, "payment-table")
    PAYMENT_TABLE_ROWS = (By.XPATH, "//table[@class='payment-table']//tr")
    PAYMENT_TABLE_HEADERS = (By.XPATH, "//table[@class='payment-table']//th")
    
    # Generic Table Methods
    @staticmethod
    def get_table_row_by_index(table_class, row_index):
        """Get table row by index"""
        return (By.XPATH, f"//table[@class='{table_class}']//tr[{row_index + 1}]")
    
    @staticmethod
    def get_table_cell_by_position(table_class, row_index, col_index):
        """Get table cell by position"""
        return (By.XPATH, f"//table[@class='{table_class}']//tr[{row_index + 1}]//td[{col_index + 1}]")

# ===== Common Element Locators =====
class CommonLocators:
    """Common locators used across multiple pages"""
    
    # Loading Indicators
    LOADING_SPINNER = (By.CLASS_NAME, "loading-spinner")
    LOADING_OVERLAY = (By.CLASS_NAME, "loading-overlay")
    
    # Modal/Popup Elements
    MODAL_OVERLAY = (By.CLASS_NAME, "modal-overlay")
    MODAL_CLOSE_BUTTON = (By.CLASS_NAME, "modal-close")
    POPUP_CLOSE_BUTTON = (By.CLASS_NAME, "popup-close")
    
    # Form Elements
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(), '取消')]")
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(), '确认')]")
    
    # Alert Messages
    SUCCESS_ALERT = (By.CLASS_NAME, "alert-success")
    ERROR_ALERT = (By.CLASS_NAME, "alert-error")
    WARNING_ALERT = (By.CLASS_NAME, "alert-warning")
    INFO_ALERT = (By.CLASS_NAME, "alert-info")
    
    # Page Elements
    PAGE_TITLE = (By.TAG_NAME, "h1")
    PAGE_HEADER = (By.CLASS_NAME, "page-header")
    MAIN_CONTENT = (By.CLASS_NAME, "main-content")
    
    # Utility Elements
    BACK_BUTTON = (By.XPATH, "//button[contains(text(), '返回')]")
    REFRESH_BUTTON = (By.XPATH, "//button[contains(text(), '刷新')]")
    SEARCH_INPUT = (By.CLASS_NAME, "search-input")
    SEARCH_BUTTON = (By.CLASS_NAME, "search-button") 