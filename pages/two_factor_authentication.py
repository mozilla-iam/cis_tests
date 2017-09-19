from selenium.common.exceptions import NoSuchFrameException
from selenium.webdriver.common.by import By

from pages.page import Page


class TwoFactorAuthentication(Page):
    _enter_passcode_button = (By.CSS_SELECTOR, '.passcode-label .positive.auth-button')
    _passcode_field_locator = (By.CSS_SELECTOR, '.passcode-label input[name="passcode"]')
    _error_message_locator = (By.CSS_SELECTOR, '.message.error')

    @property
    def is_error_message_displayed(self):
        try:
            self.selenium.switch_to_frame('duo_iframe')
        except NoSuchFrameException:
            return False
        else:
            is_message_shown = self.selenium.find_element(*self._error_message_locator).is_displayed()
            self.selenium.switch_to_default_content()
            return is_message_shown

    def enter_passcode(self, passcode):
        self.selenium.switch_to_frame('duo_iframe')
        self.selenium.find_element(*self._enter_passcode_button).click()
        self.selenium.find_element(*self._passcode_field_locator).clear()
        self.selenium.find_element(*self._passcode_field_locator).send_keys(passcode)
        self.selenium.find_element(*self._enter_passcode_button).click()
        self.selenium.switch_to_default_content()
