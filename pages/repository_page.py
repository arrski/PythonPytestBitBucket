from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from helpers import get_screenshot
import allure

class RepositoryPage:


    def __init__(self, page: Page, repo_name: str):
        self.page = page
        self.repo_name = repo_name
        self.repositories_link = page.locator('a[href="/personal_assignments/workspace/repositories/"]')
        self.create_repository_link = page.locator('[data-testid="create-repository-button"]')
        self.select_project = page.locator('//span[@id="select2-chosen-5"]')
        self.pick_project = page.locator('(//span[@class="project-dropdown--label"])[1]')
        self.enter_repo_name = page.locator('#id_name')
        self.create_repo_button = page.locator('button[type="submit"]')

    def go_to_repositories(self) -> bool:
        with allure.step("Going to repositories"):
            try:
                self.repositories_link.click()
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error going to repositories: {error}")
                get_screenshot("Screenshot_error_going_to_repositories", self.page)
                return False


    def create_repository(self) -> bool:
        with allure.step("Creating repository"):
            try:
                self.create_repository_link.click()
                self.select_project.click()
                self.pick_project.click()
                self.enter_repo_name.click()
                self.enter_repo_name.fill(str(self.repo_name))
                self.create_repo_button.click()
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error creating repository: {error}")
                get_screenshot("Screenshot_error_creating_repository", self.page)
                return False

