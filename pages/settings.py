from selenium.webdriver.common.by import By

from pages.auth0 import Auth0
from pages.base import Base
from pages.groups_page import GroupsPage
from pages.page import PageRegion
from pages.two_factor_authentication import TwoFactorAuthentication
from tests import conftest


class Settings(Base):
    _profile_tab_locator = (By.ID, 'profile')
    _profile_button_locator = (By.CSS_SELECTOR, '#profile-tab > a')

    _groups_tab_locator = (By.ID, 'mygroups')
    _groups_button_locator = (By.CSS_SELECTOR, '#mygroups-tab > a')

    _you_and_mozilla_tab_locator = (By.ID, 'youandmozilla')
    _you_and_mozilla_button_locator = (By.CSS_SELECTOR, '#youandmozilla-tab > a')

    @property
    def profile(self):
        self.wait_for_element_present(*self._profile_button_locator)
        self.selenium.find_element(*self._profile_button_locator).click()
        return self.ProfileTab(self.base_url, self.selenium,
                               self.selenium.find_element(*self._profile_tab_locator))

    @property
    def groups(self):
        self.selenium.find_element(*self._groups_button_locator).click()
        return self.Groups(self.base_url, self.selenium,
                           self.selenium.find_element(*self._groups_tab_locator))

    @property
    def you_and_mozilla(self):
        self.selenium.find_element(*self._you_and_mozilla_button_locator).click()
        return self.YouAndMozilla(self.base_url, self.selenium,
                                  self.selenium.find_element(*self._you_and_mozilla_tab_locator))

    class ProfileTab(PageRegion):
        _username_input_locator = (By.ID, 'id_username')
        _update_basic_information_locator = (By.ID, 'form-submit-basic')
        _full_name_input_locator = (By.ID, 'id_full_name')
        _primary_email_address = (By.CSS_SELECTOR, 'fieldset:nth-child(1) .email')
        _secondary_email_addresses = (By.CSS_SELECTOR, '#alternate-email .email')
        _add_identity_button_locator = (By.ID, 'nav-login')
        _update_emails_locator = (By.ID, 'form-submit-email')
        _delete_button_locator = (By.CSS_SELECTOR, '#alternate-email .delete')
        _contact_identities_locator = (By.CSS_SELECTOR, '.identity-profile')

        @property
        def primary_email(self):
            return self.selenium.find_element(*self._primary_email_address).text

        @property
        def secondary_email_address(self):
            return [item.text for item in self.selenium.find_elements(*self._secondary_email_addresses)]

        @property
        def username(self):
            return self.selenium.find_element(*self._username_input_locator).get_attribute('value')

        @property
        def full_name(self):
            return self.selenium.find_element(*self._full_name_input_locator).get_attribute('value')

        @property
        def contact_identities(self):
            return self.selenium.find_elements(*self._contact_identities_locator)

        def delete_secondary_email(self, email):
            delete_buttons = self.selenium.find_elements(*self._delete_button_locator)
            for item in self.secondary_email_address:
                if item == email:
                    email_index = self.secondary_email_address.index(item)
                    delete_buttons[email_index].click()

        def set_username(self, username):
            username_input = self.selenium.find_element(*self._username_input_locator)
            username_input.clear()
            username_input.send_keys(username)

        def sef_full_name(self, full_name):
            fullname_input = self.selenium.find_element(*self._full_name_input_locator)
            fullname_input.clear()
            fullname_input.send_keys(full_name)

        def click_update_basic_information(self):
            self.selenium.find_element(*self._update_basic_information_locator).click()

        def click_add_identity(self):
            element = self.selenium.find_element(*self._add_identity_button_locator)
            self.selenium.execute_script("arguments[0].scrollIntoView();", element)
            self.selenium.find_element(*self._add_identity_button_locator).click()
            return Auth0(self.base_url, self.selenium)

        def add_email_identity(self, email):
            auth0 = self.click_add_identity()
            auth0.request_login_link(email)
            login_link = conftest.login_link(email)
            self.selenium.get(login_link)
            return self

        def add_github_identity(self, username, password, passcode):
            auth0 = self.click_add_identity()
            auth0.login_with_github(username, password)
            two_fa = TwoFactorAuthentication(self.base_url, self.selenium)
            two_fa.enter_github_passcode(passcode)
            return self

        def click_update_emails(self):
            self.selenium.find_element(*self._update_emails_locator).click()

    class Groups(PageRegion):
        _find_group_page = (By.PARTIAL_LINK_TEXT, 'find the group')

        @property
        def is_find_group_link_visible(self):
            return self.is_element_visible(*self._find_group_page)

        def click_find_group_link(self):
            self.selenium.find_element(*self._find_group_page).click()
            return GroupsPage(self.base_url, self.selenium)

    class YouAndMozilla(PageRegion):
        _tshirt_sizes_locator = (By.CSS_SELECTOR, '.sizing div[class="tshirt-option"]')
        _update_tshirt_size_locator = (By.ID, 'form-submit-tshirt')

        @property
        def tshirt_sizes_list(self):
            return [item.text for item in self.selenium.find_elements(*self._tshirt_sizes_locator)]

        @property
        def selected_tshirt_size(self):
            for item in self.selenium.find_elements(*self._tshirt_sizes_locator):
                if item.find_element(By.CSS_SELECTOR, 'input').get_attribute('checked'):
                    return item.text

        def select_tshirt_size(self, size):
            for item in self.selenium.find_elements(*self._tshirt_sizes_locator):
                if item.text == size:
                    item.find_element(By.CSS_SELECTOR, 'input').click()

        def click_update_tshirt_size(self):
            self.selenium.find_element(*self._update_tshirt_size_locator).click()
