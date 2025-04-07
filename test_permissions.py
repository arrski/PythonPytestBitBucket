import allure
import pytest, os
from dotenv import load_dotenv
from playwright.sync_api import Page
from pages.user_page import UserPage

load_dotenv()
main_user = os.environ.get('admin')
main_user_password = os.environ.get('adminpass')
second_user = os.environ.get('user')
second_user_pass = os.environ.get('userpass')
permissions_repository = os.environ.get('permissions_repository')

#each test start with a fresh page
@pytest.fixture(scope="function")
def shared_page(playwright):
    browser = playwright.chromium.launch(headless=False, slow_mo= 2000)
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    page = context.new_page()
    yield page
    browser.close()


@allure.epic("Test Managing Permissions In Bitbucket")
@allure.story("Admin Adds User With Read Permissions")
@allure.title("Test admin logs in and create user with read permissions")
def test_admin_sets_new_user(shared_page: Page):
    user_page = UserPage(shared_page, main_user, main_user_password)
    user_page.login_user()
    user_page.go_to_repositories()
    user_page.pick_repository(permissions_repository)
    user_page.add_user_to_repo()
    user_page.log_user_off()


@allure.epic("Test Managing Permissions In Bitbucket")
@allure.story("Second Read Only User Logs In")
@allure.title("Test if second user cannot create branch and commit and repo visibility")
def test_second_user_only_read(shared_page: Page):
    user_page = UserPage(shared_page, second_user, second_user_pass)
    user_page.login_user()
    user_page.go_to_repository(permissions_repository)
    user_page.try_to_create_branch()
    user_page.try_to_modify_file()
    user_page.check_visibility()
    user_page.log_user_off()


@allure.epic("Test Managing Permissions In Bitbucket")
@allure.story("Admin Adds User Write Access")
@allure.title("Test admin changes rights from read to write")
def test_admin_sets_write_right(shared_page: Page):
    user_page = UserPage(shared_page, main_user, main_user_password)
    user_page.login_user()
    shared_page.wait_for_load_state(state="load")
    user_page.go_to_repositories()
    user_page.pick_repository(permissions_repository)
    user_page.change_user_rights()
    user_page.log_user_off()


@allure.epic("Test Managing Permissions In Bitbucket")
@allure.story("Second Write/Read User Logs In")
@allure.title("Test second user to create branch and commit")
def test_second_user_write_rights(shared_page: Page):
    user_page = UserPage(shared_page, second_user, second_user_pass)
    user_page.login_user()
    shared_page.wait_for_load_state(state="load")
    user_page.go_to_repository(permissions_repository)
    user_page.perform_commit()
    user_page.try_to_modify_file()
    user_page.approve_and_validate()
    user_page.log_user_off()


@allure.epic("Test Managing Permissions In Bitbucket")
@allure.story("Admin Removes Access For Second User")
@allure.title("Test admin removes access")
def test_admin_removes_second_user(shared_page: Page):
    user_page = UserPage(shared_page, main_user, main_user_password)
    user_page.login_user()
    shared_page.wait_for_load_state(state="networkidle")
    user_page.go_to_repositories()
    user_page.pick_repository(permissions_repository)
    user_page.remove_user(second_user)
    user_page.log_user_off()


@allure.epic("Test Managing Permissions In Bitbucket")
@allure.story("Second Write/Read User Logs In")
@allure.title("Test second user can access repository")
def test_second_user_access_denied(shared_page: Page):
    user_page = UserPage(shared_page, second_user, second_user_pass)
    user_page.login_user()
    shared_page.wait_for_load_state(state="load")
    user_page.check_access_to_repository(permissions_repository)
    user_page.log_user_off()
