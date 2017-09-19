from selenium.webdriver.common.by import By

from pages.page import Page


class Auth0(Page):
    _login_with_ldap_button_locator = (By.CSS_SELECTOR, '.auth0-lock-ldap-button.auth0-lock-ldap-big-button')
    _ldap_email_field_locator = (By.CSS_SELECTOR, '.auth0-lock-input-email .auth0-lock-input')
    _ldap_password_field_locator = (By.CSS_SELECTOR, '.auth0-lock-input-password .auth0-lock-input')
    _login_button_locator = (By.CSS_SELECTOR, '.auth0-lock-submit')
    _ldap_only_username_locator = (By.CSS_SELECTOR, 'div[class*="auth0-lock-input-username"] input')
    _ldap_only_password_locator = (By.CSS_SELECTOR, 'div[class*="auth0-lock-input-password"] input')
    _login_with_email_button_locator = (By.CSS_SELECTOR, '.auth0-lock-passwordless-button.auth0-lock-passwordless-big-button')
    _email_input_locator = (By.CSS_SELECTOR, '.auth0-lock-passwordless-pane>div>div>input')
    _send_email_button_locator = (By.CSS_SELECTOR, '.auth0-lock-passwordless-submit')
    _use_different_account_locator = (By.CSS_SELECTOR, '.auth0-lock-alternative-link')

    def login_with_ldap(self, email, password, ldap_only=False):
        if ldap_only:
            self.wait_for_element_visible(*self._ldap_only_username_locator)
            self.selenium.find_element(*self._ldap_only_username_locator).send_keys(email)
            self.selenium.find_element(*self._ldap_only_password_locator).send_keys(password)
        else:
            if self.is_element_present(*self._use_different_account_locator):
                self.selenium.find_element(*self._use_different_account_locator).click()
            self.wait_for_element_visible(*self._login_with_ldap_button_locator)
            self.selenium.find_element(*self._login_with_ldap_button_locator).click()
            self.selenium.find_element(*self._ldap_email_field_locator).send_keys(email)
            self.selenium.find_element(*self._ldap_password_field_locator).send_keys(password)
        self.selenium.find_element(*self._login_button_locator).click()

    def request_login_link(self, username):
        if self.is_element_visible(*self._use_different_account_locator):
            self.selenium.find_element(*self._use_different_account_locator).click()
        self.wait_for_element_visible(*self._login_with_email_button_locator)
        self.selenium.find_element(*self._login_with_email_button_locator).click()
        self.wait_for_element_visible(*self._email_input_locator)
        self.selenium.find_element(*self._email_input_locator).send_keys(username)
        self.selenium.find_element(*self._send_email_button_locator).click()
