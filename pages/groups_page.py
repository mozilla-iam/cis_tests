from selenium.webdriver.common.by import By

from pages.base import Base


class GroupsPage(Base):
    _create_group_main_button = (By.CLASS_NAME, 'large')
    _create_group_name = (By.NAME, 'name')
    _create_group_form = (By.CSS_SELECTOR, 'form.add-group')
    _create_group_submit_button = (By.CSS_SELECTOR, 'form.add-group .btn-primary')
    _delete_acknowledgement_locator = (By.ID, 'delete-checkbox')
    _delete_group_button_locator = (By.ID, 'delete-group')

    def create_group(self, group_name):
        self.selenium.find_element(*self._create_group_main_button).click()
        self.wait_for_element_visible(*self._create_group_name)
        element = self.selenium.find_element(*self._create_group_name)
        element.send_keys(group_name)
        self.selenium.find_element(*self._create_group_submit_button).click()

    def check_delete_aknowledgement(self):
        self.selenium.find_element(*self._delete_acknowledgement_locator).click()

    def click_delete_group(self):
        self.selenium.find_element(*self._delete_group_button_locator).click()
