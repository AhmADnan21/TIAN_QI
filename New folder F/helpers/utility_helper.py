"""
Utility Helper
Utility methods for common operations
"""

import os
import time
import random
import string
import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
import logging

class UtilityHelper:
    """Utility helper class for common operations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    # ===== Random Data Generation =====
    @staticmethod
    def generate_random_string(length=8, include_uppercase=True, include_digits=True, include_special=False):
        """Generate random alphanumeric string"""
        chars = string.ascii_lowercase
        if include_uppercase:
            chars += string.ascii_uppercase
        if include_digits:
            chars += string.digits
        if include_special:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        return ''.join(random.choices(chars, k=length))
    
    @staticmethod
    def generate_random_email(domain="test.com"):
        """Generate random email address"""
        username = UtilityHelper.generate_random_string(8, include_uppercase=False)
        return f"{username}@{domain}"
    
    @staticmethod
    def generate_random_phone(country_code="1", length=10):
        """Generate random phone number"""
        digits = ''.join(random.choices(string.digits, k=length))
        return f"{country_code}{digits}"
    
    @staticmethod
    def generate_random_number(min_value=1, max_value=1000):
        """Generate random number within range"""
        return random.randint(min_value, max_value)
    
    @staticmethod
    def generate_random_float(min_value=0.0, max_value=1000.0, decimal_places=2):
        """Generate random float within range"""
        return round(random.uniform(min_value, max_value), decimal_places)
    
    @staticmethod
    def generate_random_date(start_date=None, end_date=None):
        """Generate random date within range"""
        if not start_date:
            start_date = datetime.now() - timedelta(days=365)
        if not end_date:
            end_date = datetime.now() + timedelta(days=365)
        
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + timedelta(days=random_number_of_days)
        
        return random_date
    
    @staticmethod
    def generate_random_boolean():
        """Generate random boolean value"""
        return random.choice([True, False])
    
    @staticmethod
    def generate_random_choice(choices):
        """Generate random choice from list"""
        return random.choice(choices)
    
    # ===== File Operations =====
    @staticmethod
    def create_directory(directory_path):
        """Create directory if it doesn't exist"""
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        return directory_path
    
    @staticmethod
    def file_exists(file_path):
        """Check if file exists"""
        return Path(file_path).exists()
    
    @staticmethod
    def directory_exists(directory_path):
        """Check if directory exists"""
        return Path(directory_path).exists()
    
    @staticmethod
    def delete_file(file_path):
        """Delete file if it exists"""
        if UtilityHelper.file_exists(file_path):
            Path(file_path).unlink()
            return True
        return False
    
    @staticmethod
    def delete_directory(directory_path):
        """Delete directory and all contents"""
        if UtilityHelper.directory_exists(directory_path):
            import shutil
            shutil.rmtree(directory_path)
            return True
        return False
    
    @staticmethod
    def get_file_size(file_path):
        """Get file size in bytes"""
        if UtilityHelper.file_exists(file_path):
            return Path(file_path).stat().st_size
        return 0
    
    @staticmethod
    def get_file_extension(file_path):
        """Get file extension"""
        return Path(file_path).suffix
    
    @staticmethod
    def get_filename_without_extension(file_path):
        """Get filename without extension"""
        return Path(file_path).stem
    
    @staticmethod
    def get_filename(file_path):
        """Get filename with extension"""
        return Path(file_path).name
    
    @staticmethod
    def get_directory_path(file_path):
        """Get directory path from file path"""
        return str(Path(file_path).parent)
    
    @staticmethod
    def list_files_in_directory(directory_path, pattern="*"):
        """List files in directory matching pattern"""
        if UtilityHelper.directory_exists(directory_path):
            return list(Path(directory_path).glob(pattern))
        return []
    
    @staticmethod
    def copy_file(source_path, destination_path):
        """Copy file from source to destination"""
        if UtilityHelper.file_exists(source_path):
            import shutil
            shutil.copy2(source_path, destination_path)
            return True
        return False
    
    @staticmethod
    def move_file(source_path, destination_path):
        """Move file from source to destination"""
        if UtilityHelper.file_exists(source_path):
            import shutil
            shutil.move(source_path, destination_path)
            return True
        return False
    
    # ===== JSON Operations =====
    @staticmethod
    def read_json_file(file_path):
        """Read JSON file and return data"""
        if UtilityHelper.file_exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        return None
    
    @staticmethod
    def write_json_file(file_path, data, indent=2):
        """Write data to JSON file"""
        UtilityHelper.create_directory(UtilityHelper.get_directory_path(file_path))
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=indent, ensure_ascii=False)
    
    @staticmethod
    def update_json_file(file_path, data, indent=2):
        """Update existing JSON file with new data"""
        existing_data = UtilityHelper.read_json_file(file_path) or {}
        existing_data.update(data)
        UtilityHelper.write_json_file(file_path, existing_data, indent)
    
    # ===== CSV Operations =====
    @staticmethod
    def read_csv_file(file_path, delimiter=','):
        """Read CSV file and return data as list of dictionaries"""
        if UtilityHelper.file_exists(file_path):
            data = []
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=delimiter)
                for row in reader:
                    data.append(row)
            return data
        return []
    
    @staticmethod
    def write_csv_file(file_path, data, fieldnames=None, delimiter=','):
        """Write data to CSV file"""
        if not data:
            return
        
        if not fieldnames:
            fieldnames = data[0].keys()
        
        UtilityHelper.create_directory(UtilityHelper.get_directory_path(file_path))
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(data)
    
    # ===== Time and Date Operations =====
    @staticmethod
    def get_current_timestamp():
        """Get current timestamp"""
        return datetime.now()
    
    @staticmethod
    def get_current_timestamp_string(format_str="%Y%m%d_%H%M%S"):
        """Get current timestamp as string"""
        return datetime.now().strftime(format_str)
    
    @staticmethod
    def format_timestamp(timestamp, format_str="%Y-%m-%d %H:%M:%S"):
        """Format timestamp to string"""
        if isinstance(timestamp, datetime):
            return timestamp.strftime(format_str)
        return str(timestamp)
    
    @staticmethod
    def parse_timestamp(timestamp_str, format_str="%Y-%m-%d %H:%M:%S"):
        """Parse timestamp string to datetime object"""
        return datetime.strptime(timestamp_str, format_str)
    
    @staticmethod
    def add_days_to_date(date, days):
        """Add days to date"""
        if isinstance(date, str):
            date = UtilityHelper.parse_timestamp(date)
        return date + timedelta(days=days)
    
    @staticmethod
    def subtract_days_from_date(date, days):
        """Subtract days from date"""
        if isinstance(date, str):
            date = UtilityHelper.parse_timestamp(date)
        return date - timedelta(days=days)
    
    @staticmethod
    def get_date_difference(date1, date2):
        """Get difference between two dates in days"""
        if isinstance(date1, str):
            date1 = UtilityHelper.parse_timestamp(date1)
        if isinstance(date2, str):
            date2 = UtilityHelper.parse_timestamp(date2)
        return (date2 - date1).days
    
    # ===== String Operations =====
    @staticmethod
    def remove_special_characters(text, keep_spaces=True):
        """Remove special characters from string"""
        import re
        if keep_spaces:
            return re.sub(r'[^a-zA-Z0-9\s]', '', text)
        else:
            return re.sub(r'[^a-zA-Z0-9]', '', text)
    
    @staticmethod
    def normalize_string(text):
        """Normalize string (remove extra spaces, lowercase)"""
        return ' '.join(text.strip().lower().split())
    
    @staticmethod
    def truncate_string(text, max_length, suffix="..."):
        """Truncate string to maximum length"""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def extract_numbers_from_string(text):
        """Extract numbers from string"""
        import re
        return re.findall(r'\d+', text)
    
    @staticmethod
    def extract_emails_from_string(text):
        """Extract email addresses from string"""
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)
    
    # ===== Validation Methods =====
    @staticmethod
    def is_valid_email(email):
        """Validate email address format"""
        import re
        email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        return re.match(email_pattern, email) is not None
    
    @staticmethod
    def is_valid_phone(phone):
        """Validate phone number format"""
        import re
        phone_pattern = r'^\+?1?\d{9,15}$'
        return re.match(phone_pattern, phone) is not None
    
    @staticmethod
    def is_valid_url(url):
        """Validate URL format"""
        import re
        url_pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$'
        return re.match(url_pattern, url) is not None
    
    @staticmethod
    def is_numeric(value):
        """Check if value is numeric"""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_integer(value):
        """Check if value is integer"""
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False
    
    # ===== Wait and Sleep Methods =====
    @staticmethod
    def wait(seconds):
        """Wait for specified number of seconds"""
        time.sleep(seconds)
    
    @staticmethod
    def wait_random(min_seconds=1, max_seconds=3):
        """Wait for random number of seconds"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    # ===== Data Conversion Methods =====
    @staticmethod
    def convert_to_int(value, default=0):
        """Convert value to integer with default"""
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def convert_to_float(value, default=0.0):
        """Convert value to float with default"""
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def convert_to_string(value, default=""):
        """Convert value to string with default"""
        try:
            return str(value)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def convert_to_boolean(value, default=False):
        """Convert value to boolean with default"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        if isinstance(value, (int, float)):
            return value != 0
        return default 