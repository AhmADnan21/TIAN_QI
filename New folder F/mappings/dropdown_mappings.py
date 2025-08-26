"""
Dropdown Mappings
Package, country, language, and payment mappings
"""

# ===== Package Mappings =====
class PackageMappings:
    """Mappings for package selection dropdowns"""
    
    # Package Names to Values (for dropdowns)
    PACKAGE_NAME_TO_VALUE = {
        "天启动态尊享": "70",
        "静态IP-天启": "64",
        "天启动态标准套餐": "28",
        "天启动态独享套餐": "30"
    }
    
    # Package Values to Names (reverse mapping)
    PACKAGE_VALUE_TO_NAME = {
        "70": "天启动态尊享",
        "64": "静态IP-天启",
        "28": "天启动态标准套餐",
        "30": "天启动态独享套餐"
    }
    
    # Package Names to English
    PACKAGE_NAME_TO_ENGLISH = {
        "天启动态尊享": "Dynamic Supreme",
        "静态IP-天启": "Static IP",
        "天启动态标准套餐": "Dynamic Standard",
        "天启动态独享套餐": "Dynamic Dedicated"
    }
    
    # Package Categories
    PACKAGE_CATEGORIES = {
        "DYNAMIC": ["天启动态尊享", "天启动态标准套餐", "天启动态独享套餐"],
        "STATIC": ["静态IP-天启"]
    }
    
    @classmethod
    def get_package_value(cls, package_name):
        """Get package value by name"""
        return cls.PACKAGE_NAME_TO_VALUE.get(package_name)
    
    @classmethod
    def get_package_name(cls, package_value):
        """Get package name by value"""
        return cls.PACKAGE_VALUE_TO_NAME.get(package_value)
    
    @classmethod
    def get_package_english_name(cls, package_name):
        """Get English name for package"""
        return cls.PACKAGE_NAME_TO_ENGLISH.get(package_name)
    
    @classmethod
    def get_packages_by_category(cls, category):
        """Get packages by category"""
        return cls.PACKAGE_CATEGORIES.get(category, [])

# ===== Country Mappings =====
class CountryMappings:
    """Mappings for country selection dropdowns"""
    
    # Country Names to Codes
    COUNTRY_NAME_TO_CODE = {
        "中国": "CN",
        "美国": "US",
        "日本": "JP",
        "韩国": "KR",
        "新加坡": "SG",
        "香港": "HK",
        "台湾": "TW",
        "英国": "GB",
        "德国": "DE",
        "法国": "FR"
    }
    
    # Country Codes to Names
    COUNTRY_CODE_TO_NAME = {
        "CN": "中国",
        "US": "美国",
        "JP": "日本",
        "KR": "韩国",
        "SG": "新加坡",
        "HK": "香港",
        "TW": "台湾",
        "GB": "英国",
        "DE": "德国",
        "FR": "法国"
    }
    
    # Country Names to English
    COUNTRY_NAME_TO_ENGLISH = {
        "中国": "China",
        "美国": "United States",
        "日本": "Japan",
        "韩国": "South Korea",
        "新加坡": "Singapore",
        "香港": "Hong Kong",
        "台湾": "Taiwan",
        "英国": "United Kingdom",
        "德国": "Germany",
        "法国": "France"
    }
    
    @classmethod
    def get_country_code(cls, country_name):
        """Get country code by name"""
        return cls.COUNTRY_NAME_TO_CODE.get(country_name)
    
    @classmethod
    def get_country_name(cls, country_code):
        """Get country name by code"""
        return cls.COUNTRY_CODE_TO_NAME.get(country_code)
    
    @classmethod
    def get_country_english_name(cls, country_name):
        """Get English name for country"""
        return cls.COUNTRY_NAME_TO_ENGLISH.get(country_name)

# ===== Language Mappings =====
class LanguageMappings:
    """Mappings for language selection dropdowns"""
    
    # Language Names to Codes
    LANGUAGE_NAME_TO_CODE = {
        "中文": "zh-CN",
        "English": "en-US",
        "日本語": "ja-JP",
        "한국어": "ko-KR"
    }
    
    # Language Codes to Names
    LANGUAGE_CODE_TO_NAME = {
        "zh-CN": "中文",
        "en-US": "English",
        "ja-JP": "日本語",
        "ko-KR": "한국어"
    }
    
    # Language Names to English
    LANGUAGE_NAME_TO_ENGLISH = {
        "中文": "Chinese",
        "English": "English",
        "日本語": "Japanese",
        "한국어": "Korean"
    }
    
    @classmethod
    def get_language_code(cls, language_name):
        """Get language code by name"""
        return cls.LANGUAGE_NAME_TO_CODE.get(language_name)
    
    @classmethod
    def get_language_name(cls, language_code):
        """Get language name by code"""
        return cls.LANGUAGE_CODE_TO_NAME.get(language_code)
    
    @classmethod
    def get_language_english_name(cls, language_name):
        """Get English name for language"""
        return cls.LANGUAGE_NAME_TO_ENGLISH.get(language_name)

# ===== Payment Mappings =====
class PaymentMappings:
    """Mappings for payment method selection"""
    
    # Payment Method Names to Values
    PAYMENT_NAME_TO_VALUE = {
        "余额": "balance",
        "支付宝": "alipay",
        "微信": "wechat",
        "银行卡": "bank_card",
        "信用卡": "credit_card"
    }
    
    # Payment Method Values to Names
    PAYMENT_VALUE_TO_NAME = {
        "balance": "余额",
        "alipay": "支付宝",
        "wechat": "微信",
        "bank_card": "银行卡",
        "credit_card": "信用卡"
    }
    
    # Payment Method Names to English
    PAYMENT_NAME_TO_ENGLISH = {
        "余额": "Balance",
        "支付宝": "Alipay",
        "微信": "WeChat",
        "银行卡": "Bank Card",
        "信用卡": "Credit Card"
    }
    
    # Payment Method Categories
    PAYMENT_CATEGORIES = {
        "DIGITAL_WALLET": ["余额", "支付宝", "微信"],
        "BANK_CARD": ["银行卡", "信用卡"]
    }
    
    # Payment Method Icons
    PAYMENT_ICONS = {
        "余额": "wallet-icon",
        "支付宝": "alipay-icon",
        "微信": "wechat-icon",
        "银行卡": "bank-icon",
        "信用卡": "credit-card-icon"
    }
    
    @classmethod
    def get_payment_value(cls, payment_name):
        """Get payment value by name"""
        return cls.PAYMENT_NAME_TO_VALUE.get(payment_name)
    
    @classmethod
    def get_payment_name(cls, payment_value):
        """Get payment name by value"""
        return cls.PAYMENT_VALUE_TO_NAME.get(payment_value)
    
    @classmethod
    def get_payment_english_name(cls, payment_name):
        """Get English name for payment method"""
        return cls.PAYMENT_NAME_TO_ENGLISH.get(payment_name)
    
    @classmethod
    def get_payments_by_category(cls, category):
        """Get payment methods by category"""
        return cls.PAYMENT_CATEGORIES.get(category, [])
    
    @classmethod
    def get_payment_icon(cls, payment_name):
        """Get payment method icon class"""
        return cls.PAYMENT_ICONS.get(payment_name)

# ===== Currency Mappings =====
class CurrencyMappings:
    """Mappings for currency selection"""
    
    # Currency Names to Codes
    CURRENCY_NAME_TO_CODE = {
        "人民币": "CNY",
        "美元": "USD",
        "日元": "JPY",
        "韩元": "KRW",
        "新加坡元": "SGD",
        "港币": "HKD",
        "新台币": "TWD",
        "英镑": "GBP",
        "欧元": "EUR"
    }
    
    # Currency Codes to Names
    CURRENCY_CODE_TO_NAME = {
        "CNY": "人民币",
        "USD": "美元",
        "JPY": "日元",
        "KRW": "韩元",
        "SGD": "新加坡元",
        "HKD": "港币",
        "TWD": "新台币",
        "GBP": "英镑",
        "EUR": "欧元"
    }
    
    # Currency Symbols
    CURRENCY_SYMBOLS = {
        "CNY": "¥",
        "USD": "$",
        "JPY": "¥",
        "KRW": "₩",
        "SGD": "S$",
        "HKD": "HK$",
        "TWD": "NT$",
        "GBP": "£",
        "EUR": "€"
    }
    
    @classmethod
    def get_currency_code(cls, currency_name):
        """Get currency code by name"""
        return cls.CURRENCY_NAME_TO_CODE.get(currency_name)
    
    @classmethod
    def get_currency_name(cls, currency_code):
        """Get currency name by code"""
        return cls.CURRENCY_CODE_TO_NAME.get(currency_code)
    
    @classmethod
    def get_currency_symbol(cls, currency_code):
        """Get currency symbol by code"""
        return cls.CURRENCY_SYMBOLS.get(currency_code)

# ===== Time Period Mappings =====
class TimePeriodMappings:
    """Mappings for time period selection"""
    
    # Time Period Names to Values
    TIME_PERIOD_NAME_TO_VALUE = {
        "1个月": "1",
        "3个月": "3",
        "6个月": "6",
        "12个月": "12",
        "24个月": "24"
    }
    
    # Time Period Values to Names
    TIME_PERIOD_VALUE_TO_NAME = {
        "1": "1个月",
        "3": "3个月",
        "6": "6个月",
        "12": "12个月",
        "24": "24个月"
    }
    
    # Time Period Names to English
    TIME_PERIOD_NAME_TO_ENGLISH = {
        "1个月": "1 Month",
        "3个月": "3 Months",
        "6个月": "6 Months",
        "12个月": "12 Months",
        "24个月": "24 Months"
    }
    
    @classmethod
    def get_time_period_value(cls, time_period_name):
        """Get time period value by name"""
        return cls.TIME_PERIOD_NAME_TO_VALUE.get(time_period_name)
    
    @classmethod
    def get_time_period_name(cls, time_period_value):
        """Get time period name by value"""
        return cls.TIME_PERIOD_VALUE_TO_NAME.get(time_period_value)
    
    @classmethod
    def get_time_period_english_name(cls, time_period_name):
        """Get English name for time period"""
        return cls.TIME_PERIOD_NAME_TO_ENGLISH.get(time_period_name) 