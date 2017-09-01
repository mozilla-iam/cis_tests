from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.auth0 import Auth0
from pages.page import Page
from pages.two_factor_authentication import TwoFactorAuthentication


class Base(Page):
    _sign_in_button = (By.ID, 'nav-login')

    def click_sign_in_button(self):
        self.selenium.find_element(*self._sign_in_button).click()
        return Auth0(self.base_url, self.selenium)

    def login_with_ldap(self, ldap_email, ldap_password):
        auth0 = self.click_sign_in_button()
        auth0.login_with_ldap(ldap_email, ldap_password)
        return TwoFactorAuthentication(self.base_url, self.selenium)

    @property
    def header(self):
        return self.Header(self.base_url, self.selenium)

    class Header(Page):
        _profile_menu_locator = (By.CSS_SELECTOR, '#nav-main > a.dropdown-toggle i')
        _dropdown_menu_locator = (By.CSS_SELECTOR, 'ul.dropdown-menu')
        _groups_menu_item_locator = (By.ID, 'nav-groups')
        _invite_menu_item_locator = (By.ID, 'nav-invite')
        _settings_menu_item_locator = (By.ID, 'nav-edit-profile')
        _logout_menu_item_locator = (By.ID, 'nav-logout')

        def click_options(self):
            self.wait_for_element_present(*self._profile_menu_locator)
            self.selenium.find_element(*self._profile_menu_locator).click()
            WebDriverWait(self.selenium, self.timeout).until(lambda s: self.selenium.find_element(*self._dropdown_menu_locator))

        def click_settings_menu_item(self):
            self.click_options()
            self.selenium.find_element(*self._settings_menu_item_locator).click()
            from pages.settings import Settings
            return Settings(self.base_url, self.selenium)
