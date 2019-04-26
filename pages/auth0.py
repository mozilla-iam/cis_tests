from selenium.webdriver.common.by import By

from pages.page import Page


class Auth0(Page):
    _email_locator = (By.ID, 'field-email')
    _enter_locator = (By.ID, 'enter-initial')
    _send_email_locator = (By.CSS_SELECTOR, 'button[data-handler=send-passwordless-link]')
    _login_with_github_button_locator = (By.CSS_SELECTOR, 'button[data-handler="authorise-github"]')
    _password_locator = (By.ID, 'field-password')
    _enter_button_locator = (By.ID, 'authorise-ldap-credentials')
    _enter_passcode_button_locator = (By.CSS_SELECTOR, '.passcode-label .positive.auth-button')
    _passcode_field_locator = (By.CSS_SELECTOR, '.passcode-label input[name="passcode"]')

    def login_with_ldap(self, email, password):
        self.wait_for_element_visible(*self._email_locator)
        self.selenium.find_element(*self._email_locator).send_keys(email)
        self.selenium.find_element(*self._enter_locator).click()
        self.wait_for_element_visible(*self._password_locator)
        self.selenium.find_element(*self._password_locator).send_keys(password)
        self.selenium.find_element(*self._enter_button_locator).click()

    def request_login_link(self, email):
        self.wait_for_element_visible(self._email_locator)
        self.selenium.find_element(*self._email_locator).send_keys(email)
        self.selenium.find_element(*self._enter_locator).click()
        self.selenium.find_element(self._send_email_locator).click()
