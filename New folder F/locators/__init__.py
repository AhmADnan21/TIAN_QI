"""
Locators Module
Contains all element locators organized by page
"""

from .element_locators import (
    LoginPageLocators,
    PackageOrderPageLocators,
    PersonalCenterPageLocators,
    NavigationLocators,
    TableLocators,
    CommonLocators
)

__all__ = [
    'LoginPageLocators',
    'PackageOrderPageLocators', 
    'PersonalCenterPageLocators',
    'NavigationLocators',
    'TableLocators',
    'CommonLocators'
] 