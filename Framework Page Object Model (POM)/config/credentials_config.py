"""
Credentials Configuration
User accounts grouped by type (with/without balance, admin, etc.)
"""

# ===== User Credentials =====
class UserCredentials:
    """User account credentials organized by type"""
    
    # ===== Regular Users =====
    USERS_WITH_BALANCE = {
        "user_with_balance_1": {
            "phone": "15332595364",
            "password": "Test@123",
            "balance": "1000.00",
            "description": "User with sufficient balance for all packages"
        },
        "user_with_balance_2": {
            "phone": "15332595365",
            "password": "Test@123",
            "balance": "500.00",
            "description": "User with moderate balance"
        }
    }
    
    USERS_WITHOUT_BALANCE = {
        "user_no_balance_1": {
            "phone": "15658873355",
            "password": "Test@123",
            "balance": "0.00",
            "description": "User with zero balance"
        },
        "user_no_balance_2": {
            "phone": "15658873356",
            "password": "Test@123",
            "balance": "10.00",
            "description": "User with insufficient balance"
        }
    }
    
    # ===== Admin Users =====
    ADMIN_USERS = {
        "admin_user": {
            "phone": "admin@test.com",
            "password": "Admin@123",
            "role": "admin",
            "description": "Administrator account"
        }
    }
    
    # ===== Test Users =====
    TEST_USERS = {
        "test_user_1": {
            "phone": "testuser1@test.com",
            "password": "Test@123",
            "description": "General test user 1"
        },
        "test_user_2": {
            "phone": "testuser2@test.com",
            "password": "Test@123",
            "description": "General test user 2"
        }
    }
    
    @classmethod
    def get_user_with_balance(cls, user_key="user_with_balance_1"):
        """Get user credentials with balance"""
        return cls.USERS_WITH_BALANCE.get(user_key)
    
    @classmethod
    def get_user_without_balance(cls, user_key="user_no_balance_1"):
        """Get user credentials without balance"""
        return cls.USERS_WITHOUT_BALANCE.get(user_key)
    
    @classmethod
    def get_admin_user(cls, user_key="admin_user"):
        """Get admin user credentials"""
        return cls.ADMIN_USERS.get(user_key)
    
    @classmethod
    def get_test_user(cls, user_key="test_user_1"):
        """Get test user credentials"""
        return cls.TEST_USERS.get(user_key)
    
    @classmethod
    def get_all_users_with_balance(cls):
        """Get all users with balance"""
        return cls.USERS_WITH_BALANCE
    
    @classmethod
    def get_all_users_without_balance(cls):
        """Get all users without balance"""
        return cls.USERS_WITHOUT_BALANCE
    
    @classmethod
    def get_all_admin_users(cls):
        """Get all admin users"""
        return cls.ADMIN_USERS
    
    @classmethod
    def get_all_test_users(cls):
        """Get all test users"""
        return cls.TEST_USERS

# ===== Environment-Specific Credentials =====
class EnvironmentCredentials:
    """Credentials for different environments"""
    
    TEST_ENV = {
        "default_user_with_balance": UserCredentials.get_user_with_balance(),
        "default_user_without_balance": UserCredentials.get_user_without_balance(),
        "default_admin": UserCredentials.get_admin_user()
    }
    
    STAGING_ENV = {
        "default_user_with_balance": {
            "phone": "staging_user@test.com",
            "password": "Staging@123",
            "balance": "1000.00"
        },
        "default_user_without_balance": {
            "phone": "staging_no_balance@test.com",
            "password": "Staging@123",
            "balance": "0.00"
        }
    }
    
    PROD_ENV = {
        "default_user_with_balance": {
            "phone": "prod_user@test.com",
            "password": "Prod@123",
            "balance": "1000.00"
        },
        "default_user_without_balance": {
            "phone": "prod_no_balance@test.com",
            "password": "Prod@123",
            "balance": "0.00"
        }
    }
    
    @classmethod
    def get_credentials_for_env(cls, environment="test"):
        """Get credentials for specified environment"""
        env_map = {
            "test": cls.TEST_ENV,
            "staging": cls.STAGING_ENV,
            "prod": cls.PROD_ENV
        }
        return env_map.get(environment.lower(), cls.TEST_ENV)
    
    @classmethod
    def get_user_with_balance_for_env(cls, environment="test"):
        """Get user with balance for specified environment"""
        env_creds = cls.get_credentials_for_env(environment)
        return env_creds.get("default_user_with_balance")
    
    @classmethod
    def get_user_without_balance_for_env(cls, environment="test"):
        """Get user without balance for specified environment"""
        env_creds = cls.get_credentials_for_env(environment)
        return env_creds.get("default_user_without_balance") 