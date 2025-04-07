from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from helpers import overview_url
import allure


class LoginPage:

    URL = overview_url

    def __init__(self, page: Page, user: str, password: str):
        self.page = page
        self.field_username = page.locator("[id=username]")
        self.field_password = page.locator("[id=password]")
        self.login_button = page.locator("#login-submit")
        self.user = user
        self.password = password

    def load_page(self) -> bool:
        with allure.step("Going to login page"):
            try:
                self.page.goto(self.URL)
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error going to page: {error}")
                return False

    def click_and_enter_user(self) -> bool:
        with allure.step("Entering username"):
            try:
                self.field_username.click()
                self.field_username.fill(self.user)
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error entering user name {error}")
                return False

    def click_and_enter_password(self) -> bool:
        with allure.step("Entering password"):
            try:
                self.field_password.click()
                self.field_password.fill(self.password)
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error entering password: {error}")
                return False

    def click_login_button(self) -> bool:
        with allure.step("Clicking login button"):
            try:
                self.login_button.click()
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error clicking login button: {error}")
                return False

    def fast_login_user(self):
        with allure.step("Performing fast login"):
            try:
                self.page.goto(self.URL)
                self.field_username.click()
                self.field_username.fill(self.user)
                self.login_button.click()
                self.field_password.click()
                self.field_password.fill(self.password)
                self.login_button.click()
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error going to repositories: {error}")
                return False