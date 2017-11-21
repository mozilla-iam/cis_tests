import time

from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.support.wait import WebDriverWait


class Page(object):

    def __init__(self, base_url, selenium):
        self.base_url = base_url
        self.selenium = selenium
        self.timeout = 60

    def is_element_visible(self, *locator):
        try:
            return self.selenium.find_element(*locator).is_displayed()
        except (NoSuchElementException, ElementNotVisibleException):
            return False

    def is_element_present(self, *locator):
        self.selenium.implicitly_wait(0)
        try:
            self.selenium.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(10)

    def wait_for_element_visible(self, *locator):
        count = 0
        while not self.is_element_visible(*locator):
            time.sleep(1)
            count += 1
            if count == self.timeout:
                raise Exception(':'.join(locator) + " is not visible")

    def wait_for_element_present(self, *locator):
        """Wait for an element to become present."""
        self.selenium.implicitly_wait(0)
        try:
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: s.find_element(*locator))
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(10)

    def go_to_url(self, url):
        self.selenium.get(url)

    @property
    def current_url(self):
        return self.selenium.current_url()


class PageRegion(Page):

    def __init__(self, base_url, selenium, root_element):
        Page.__init__(self, base_url, selenium)
        self._root_element = root_element
