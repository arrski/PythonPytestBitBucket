import uuid, allure
import pytest, os
from dotenv import load_dotenv
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.repository_page import RepositoryPage
from pages.modify_page import ModifyPage

repo_name = 'repo_' + str(uuid.uuid4())[:8] #let's generate unique name for repo each time
branch_name = 'fix_for_issue_' + str(uuid.uuid4())[:8] #let's generate unique branch for repo each time
load_dotenv()
main_user = os.environ.get('admin')
main_user_password = os.environ.get('adminpass')

#a shared page between all test cases
@pytest.fixture(scope="module")
def shared_page(playwright):
    browser = playwright.chromium.launch(headless=False, slow_mo= 2000)
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    page = context.new_page()
    yield page
    browser.close()

@allure.epic("Test Creating A Repository in Bitbucket")
@allure.story("Admin Logs In")
@allure.title("Test admin logs in")
def test_user_can_log_in(shared_page: Page) -> None:
    login_page = LoginPage(shared_page, main_user, main_user_password)
    login_page.load_page()
    login_page.click_and_enter_user()
    login_page.click_login_button()
    login_page.click_and_enter_password()
    login_page.click_login_button()

@allure.epic("Test Creating A Repository in Bitbucket")
@allure.story("Admin Creates Repository")
@allure.title("Test if admin can create repository")
def test_user_can_manage_repositories(shared_page: Page) -> None:
    repositories_page = RepositoryPage(shared_page, repo_name)
    repositories_page.go_to_repositories()
    repositories_page.create_repository()

@allure.epic("Test Creating A Repository in Bitbucket")
@allure.story("Admin Makes A Commit")
@allure.title("Test if admin can create branch, commit and then merge")
def test_user_modify_file_and_make_pr(shared_page: Page) -> None:
    modify_page = ModifyPage(shared_page, repo_name, branch_name)
    modify_page.create_branch()
    modify_page.modify_and_commit()
    modify_page.approve_pr_and_validate()
    modify_page.check_last_commit(repo_name)
    modify_page.log_user_off()


