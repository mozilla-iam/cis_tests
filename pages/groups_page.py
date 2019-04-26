from selenium.webdriver.common.by import By

from pages.base import Base


class GroupsPage(Base):
    _create_group_main_button = (By.CLASS_NAME, 'large')
    _create_group_name = (By.NAME, 'name')
    _create_group_form = (By.CSS_SELECTOR, 'form.add-group')
    _create_group_submit_button = (By.CSS_SELECTOR, 'form.add-group .btn-primary')
    _delete_acknowledgement_locator = (By.ID, 'delete-checkbox')
    _delete_group_button_locator = (By.ID, 'delete-group')
    _group_type_options_locator = (By.CSS_SELECTOR, '#group_type label')
    _access_type_options_locator = (By.CSS_SELECTOR, '#access_type label')

    def create_group(self, group_name, group_type='Open', access_type='Tag'):
        self.selenium.find_element(*self._create_group_main_button).click()
        self.wait_for_element_visible(*self._create_group_name)
        element = self.selenium.find_element(*self._create_group_name)
        element.send_keys(group_name)
        self.set_group_type(group_type)
        self.set_access_type(access_type)
        self.selenium.find_element(*self._create_group_submit_button).click()

    def check_delete_aknowledgement(self):
        self.selenium.find_element(*self._delete_acknowledgement_locator).click()

    def click_delete_group(self):
        self.selenium.find_element(*self._delete_group_button_locator).click()

    def set_group_type(self, group_type):
        group_type_options = self.selenium.find_elements(*self._group_type_options_locator)
        [item.click() for item in group_type_options if group_type == item.text]

    def set_access_type(self, access_type):
        access_type_options = self.selenium.find_elements(*self._access_type_options_locator)
        [item.click() for item in access_type_options if access_type == item.text]
