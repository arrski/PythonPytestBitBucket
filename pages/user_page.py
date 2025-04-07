from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from helpers import find_desired_element_to_click, get_screenshot
from pages.login_page import LoginPage
from pages.modify_page import ModifyPage
import allure

class UserPage(LoginPage, ModifyPage):

    repo_url = "https://bitbucket.org/personal_assignments/workspace/repositories/"

    def __init__(self, page: Page, user: str, password: str):
        LoginPage.__init__(self, page, user, password)
        ModifyPage.__init__(self, page, repo_name = 'repo_permission_test', branch_name = 'permission_test_branch')
        self.page = page
        self.popup = ''


    def perform_commit(self):
        self.modify_and_commit()

    def approve_and_validate(self):
        self.approve_pr_and_validate()

    def login_user(self):
        self.fast_login_user()

    def enter_credentials(self):
        self.click_and_enter_user()

    def enter_password(self):
        self.click_and_enter_password()

    def click_login(self):
        self.login_button.click()

    def go_to_repositories(self) -> None:
        self.page.goto(self.repo_url)

    def pick_repository(self, repository: str) -> bool:
        with allure.step("Picking repository"):
            try:
                self.elements = self.page.locator('//span[@class="css-uokyes"]')
                self.page.locator(f'//a[normalize-space()="{repository}"]').click()
                find_desired_element_to_click(self.elements, "Repository settings", self.page)
                find_desired_element_to_click(self.elements, "Repository permissions", self.page)
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error picking repository: {error}")
                get_screenshot("Screenshot_error_pinking_repository", self.page)
                return False


    def add_user_to_repo(self) -> bool:
        with allure.step("Adding user"):
            try:
                self.page.locator('[data-testid="addPrivilegeButton"]').click()
                self.page.get_by_role("button", name="Confirm").click()
                get_screenshot("Screenshot_add_user", self.page)
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error adding user: {error}")
                get_screenshot("Screenshot_error_adding_user", self.page)
                return False


    def try_to_create_branch(self) -> bool:
        with allure.step("Creating branch"):
            try:
                self.elements = self.page.locator('//span[@class="css-uokyes"]')
                find_desired_element_to_click(self.elements, "Branches", self.page)
                if self.page.locator('#open-create-branch-modal').is_disabled():
                        get_screenshot("Screenshot_cant_create_branch", self.page)
                else:
                    print("Branch created successfully")
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error creating branch: {error}")
                get_screenshot("Screenshot_error_creating_branch", self.page)
                return False


    def try_to_modify_file(self) -> bool:
        with allure.step("Editing file"):
            try:
                self.elements = self.page.locator('//span[@class="css-uokyes"]')
                find_desired_element_to_click(self.elements, "Source", self.page)
                if not self.page.locator('button:has-text("Edit")').is_visible():
                    get_screenshot("Screenshot_cant_modify_file", self.page)
                else:
                    print("File modified successfully")
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error editing file: {error}")
                get_screenshot("Screenshot_error_editing_file", self.page)
                return False


    def check_visibility(self) -> bool:
        with allure.step("Checking visibility"):
            try:
                self.elements = self.page.locator('//span[@class="css-uokyes"]')
                find_desired_element_to_click(self.elements, "Source", self.page)
                if self.page.locator('//h1[normalize-space()="repo_permission_test"]').is_visible():
                    get_screenshot("Screenshot_can_view_repository", self.page)
                else:
                    print("Can't see repository")
                find_desired_element_to_click(self.elements, "Pull requests", self.page)
                if self.page.locator('div[data-qa="create-pull-request-button"]').is_visible():
                    get_screenshot("Screenshot_can_pull_requests", self.page)
                else:
                    print("Can't see pull requests")
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error checking_visibility: {error}")
                get_screenshot("Screenshot_error_checking_visibility", self.page)
                return False


    def change_user_rights(self) -> bool:
        with allure.step("Changing user rights"):
            try:
                self.page.locator('button[data-testid="privilegesDropdown--trigger"]').click()
                self.page.locator('(// button[@role="menuitem"])[2]').click()
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error changing user right: {error}")
                get_screenshot("Screenshot_error_changing_right", self.page)
                return False


    def go_to_repository(self, repository: str) -> bool:
        with allure.step("Going to repository"):
            try:
                self.page.goto(self.repo_url)
                self.page.locator(f'//a[normalize-space()="{repository}"]').click()
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error going to repository: {error}")
                get_screenshot("Screenshot_error_going_to_repository", self.page)
                return False


    def remove_user(self, user: str) -> bool:
        with allure.step("Removing user"):
            try:
                self.page.locator('//span[normalize-space()="Remove"]').click()
                get_screenshot("Removing_user", self.page)
                self.page.locator('[data-testid="remove-access-modal--remove-btn"]').click()
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error removing user: {error}")
                get_screenshot("Screenshot_error_removing_user", self.page)
                return False


    def log_user_off(self) -> bool:
        with allure.step("Logging user off"):
            try:
                self.page.locator('button[aria-label="Your profile"]').click()
                self.page.locator('//span[contains(text(),"Log out")]').click()
                self.page.locator('//a[normalize-space()="Log in to another account"]').click()
                get_screenshot("User_logged_off", self.page)
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error logging off: {error}")
                get_screenshot("Screenshot_error_logging_off", self.page)
                return False


    def check_access_to_repository(self, repo: str) -> bool:
        with allure.step("Checking access to repository"):
            try:
                self.page.goto(f"https://bitbucket.org/personal_assignments/{repo}/src/main/")
                if self.page.locator('.icon.icon-404').is_visible():
                    get_screenshot("Repository_not_found", self.page)
                self.page.goto(self.repo_url)
                get_screenshot("No_repositories_visible", self.page)
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error in accessing repo: {error}")
                get_screenshot("Screenshot_error_in_accessing_repo", self.page)
                return False




