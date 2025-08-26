"""
Test Data Configuration
App URLs and reusable test data
"""

# ===== Application URLs =====
class AppURLs:
    """Application URLs for different environments"""
    
    # Base URLs
    TEST_ENV = "https://test-ip-tianqi.cd.xiaoxigroup.net"
    STAGING_ENV = "https://staging-ip-tianqi.cd.xiaoxigroup.net"
    PROD_ENV = "https://ip-tianqi.cd.xiaoxigroup.net"
    
    # Page URLs
    LOGIN_PAGE = "/login"
    PACKAGE_ORDER_PAGE = "/packageOrder"
    PERSONAL_CENTER_PAGE = "/personal/accountManager"
    RECHARGE_PAGE = "/personal/recharge"
    
    @classmethod
    def get_base_url(cls, environment="test"):
        """Get base URL for specified environment"""
        env_map = {
            "test": cls.TEST_ENV,
            "staging": cls.STAGING_ENV,
            "prod": cls.PROD_ENV
        }
        return env_map.get(environment.lower(), cls.TEST_ENV)
    
    @classmethod
    def get_login_url(cls, environment="test"):
        """Get login URL for specified environment"""
        return cls.get_base_url(environment) + cls.LOGIN_PAGE
    
    @classmethod
    def get_package_order_url(cls, environment="test"):
        """Get package order URL for specified environment"""
        return cls.get_base_url(environment) + cls.PACKAGE_ORDER_PAGE
    
    @classmethod
    def get_personal_center_url(cls, environment="test"):
        """Get personal center URL for specified environment"""
        return cls.get_base_url(environment) + cls.PERSONAL_CENTER_PAGE

# ===== Test Data =====
class TestData:
    """Reusable test data"""
    
    # Wait Times
    SHORT_WAIT = 2
    MEDIUM_WAIT = 5
    LONG_WAIT = 10
    
    # Test Account Information
    ACCOUNT_WITH_BALANCE = {
        "phone": "15332595364",
        "password": "Test@123",
        "balance": "1000.00"
    }
    
    ACCOUNT_WITHOUT_BALANCE = {
        "phone": "15658873355",
        "password": "Test@123",
        "balance": "0.00"
    }
    
    # Random Data Generators
    @staticmethod
    def generate_random_string(length=8):
        """Generate random alphanumeric string"""
        import random
        import string
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    @staticmethod
    def generate_random_email():
        """Generate random email address"""
        import random
        import string
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        domain = ''.join(random.choices(string.ascii_lowercase, k=6))
        return f"{username}@{domain}.com"
    
    @staticmethod
    def generate_random_phone():
        """Generate random phone number"""
        import random
        return f"1{random.randint(3000000000, 9999999999)}"

# ===== Package Information =====
class PackageData:
    """Package-related test data"""
    
    # Package Names
    DYNAMIC_SUPREME = "天启动态尊享"
    STATIC_IP = "静态IP-天启"
    DYNAMIC_STANDARD = "天启动态标准套餐"
    DYNAMIC_DEDICATED = "天启动态独享套餐"
    
    # Package Values (for dropdowns)
    PACKAGE_VALUES = {
        DYNAMIC_SUPREME: "70",
        STATIC_IP: "64",
        DYNAMIC_STANDARD: "28",
        DYNAMIC_DEDICATED: "30"
    }
    
    # Package Prices
    PACKAGE_PRICES = {
        DYNAMIC_SUPREME: "99.00",
        STATIC_IP: "199.00",
        DYNAMIC_STANDARD: "49.00",
        DYNAMIC_DEDICATED: "149.00"
    }

# ===== Payment Information =====
class PaymentData:
    """Payment-related test data"""
    
    # Payment Methods
    BALANCE_PAYMENT = "余额"
    ALIPAY_PAYMENT = "支付宝"
    WECHAT_PAYMENT = "微信"
    
    # Payment Method Values
    PAYMENT_METHODS = [BALANCE_PAYMENT, ALIPAY_PAYMENT, WECHAT_PAYMENT]
    
    # Expected URLs for payment verification
    ALIPAY_SANDBOX_URL = "alipaydev.com"
    WECHAT_QR_TEXT = "微信扫码支付"

# ===== Error Messages =====
class ErrorMessages:
    """Expected error messages"""
    
    INSUFFICIENT_BALANCE = "账户余额不足"
    LOGIN_FAILED = "登录失败"
    PAYMENT_FAILED = "支付失败"
    NETWORK_ERROR = "网络错误"
    
    # Success Messages
    LOGIN_SUCCESS = "登录成功"
    PAYMENT_SUCCESS = "套餐购买成功"
    ACCOUNT_CREATED = "创建成功" 