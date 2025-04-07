from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError
from helpers import find_desired_element_to_click, get_screenshot
import allure

class ModifyPage:

    def __init__(self, page: Page, repo_name: str, branch_name: str):
        self.page = page
        self.repo_name = repo_name
        self.branch_name = branch_name
        self.elements = page.locator('//span[@class="css-uokyes"]') #side menu items

        #branch related locators
        self.create_branch_button = page.locator("[id=open-create-branch-modal]")
        self.enter_branch_name = page.locator('input[name="branchName"]')
        self.confirm_branch_button = page.locator('//button[@id="create-branch-button"]')

        #modify and commit locators
        self.change_branch = page.locator('//button[@data-testid="ref-selector-trigger"]')
        self.pick_branch = page.locator(f'//a[normalize-space()="{self.branch_name}"]')
        self.pick_file = page.locator('a[href="README.md"]')
        self.edit_file = page.locator('button:has-text("Edit")')
        self.confirm_changes = page.locator('//button[@class="button-panel-button commit-button aui-button"]')
        self.click_inside_file = page.locator("div:nth-child(10) > .CodeMirror-line")
        self.enter_text_into_file = page.locator("#editor-container").get_by_role("textbox")
        self.save_changes_in_file = page.locator('.save-button.aui-button.aui-button-primary')

        #approve and merge locators
        self.create_pr = page.locator('div[data-qa="create-pull-request-button"]')
        self.create_pr_button = page.locator('button[name="create"]')
        self.overview_tab = self.page.locator('//span[normalize-space()="Files changed"]')
        self.confirm_viewing_check = self.page.locator('input[value="Controlled Checkbox"]')
        self.approve_pr = self.page.locator('//span[contains(text(),"Approve")]')
        self.unapprove_pr = self.page.locator('//span[contains(text(),"Unapprove")]')
        self.merge_button = self.page.locator('//span[contains(text(),"Merge")]')


    def create_branch(self) -> bool:
        with allure.step("Creating branch"):
            try:
                find_desired_element_to_click(self.elements, "Branches", self.page)
                self.create_branch_button.click()
                self.enter_branch_name.fill(self.branch_name)
                self.confirm_branch_button.click()
                get_screenshot("Screenshot_confirm_branch_button", self.page)
                self.page.locator(f'a[href="/personal_assignments/{self.repo_name}/src"]').click()
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error creating branch: {error}")
                get_screenshot("Screenshot_error_creating_branch", self.page)
                return False


    def modify_and_commit(self) -> bool:
        with allure.step("Editing and commiting file"):
            try:
                find_desired_element_to_click(self.elements, "Source", self.page)
                self.change_branch.click()
                self.pick_branch.click()
                self.pick_file.click()
                self.edit_file.click()
                self.click_inside_file.click()
                self.enter_text_into_file.fill("*****THIS IS A CHANGE INTRODUCED DURING EDITION*****")
                get_screenshot("Screenshot_enter_text_into_file", self.page)
                self.save_changes_in_file.click()
                self.confirm_changes.wait_for(state="visible")
                expect(self.confirm_changes).to_be_visible()
                get_screenshot("Screenshot_confirm_change", self.page)
                self.confirm_changes.click()
                self.page.wait_for_load_state("networkidle")
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error while editing file: {error}")
                get_screenshot("Screenshot_error_editing_file", self.page)
                return False


    def approve_pr_and_validate(self) -> bool:
        with allure.step("Approving and validating"):
            try:
                self.page.wait_for_selector('//span[@class="css-uokyes"]', state="attached")
                find_desired_element_to_click(self.elements, "Pull requests", self.page)
                self.create_pr.click()
                self.create_pr_button.scroll_into_view_if_needed(timeout=4000)
                self.create_pr_button.click()
                get_screenshot("Screenshot_create_pr_button", self.page)
                self.overview_tab.scroll_into_view_if_needed(timeout=4000)
                self.overview_tab.click()
                get_screenshot("Screenshot_overview_tab", self.page)
                self.confirm_viewing_check.click()
                self.approve_pr.click()
                self.unapprove_pr.wait_for(state="visible")
                self.merge_button.click()
                get_screenshot("Screenshot_merge_button", self.page)
                self.page.get_by_label("Merge pull request").get_by_role("button", name="Merge").click()
                self.page.wait_for_load_state(state="networkidle")
                get_screenshot("Screenshot_branch_merged", self.page)
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error during validation: {error}")
                get_screenshot("Screenshot_during_validation", self.page)
                return False

    def check_last_commit(self, repo_name: str):
        with allure.step("Logging user off"):
            try:
                self.page.goto(f"https://bitbucket.org/personal_assignments/{repo_name}/commits/branch/main")
                get_screenshot("Changes merged", self.page)
                return True
            except PlaywrightTimeoutError as error:
                print(f"Error logging off: {error}")
                get_screenshot("Screenshot_error_logging_off", self.page)
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
