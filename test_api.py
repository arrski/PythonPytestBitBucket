import json, uuid, os
from dotenv import load_dotenv
from helpers import *

load_dotenv()
key = os.environ.get('key')
secret = os.environ.get('secret')


# Make tests independent with unique repository names test_repo + ID
@pytest.fixture(scope="module")
def repository_name():
    unique_id = str(uuid.uuid4())[:8]
    return f"test_repo_{unique_id}"


@pytest.fixture(scope="module")
def api_urls(repository_name):
    return {
        "repository_url": f"{workspace_url}{repository_name}",
        "commit_url": f"{workspace_url}{repository_name}/src",
        "branches_url": f"{workspace_url}{repository_name}/refs/branches"
    }


# Provide headers for test cases
@pytest.fixture(scope="module")
def provide_headers():
    try:
        headers = generate_access_token(key, secret, access_token_url)
        return headers
    except Exception as e:
        pytest.fail(f"Failed to generate access token: {str(e)}")


#provide simple headers just with access token
@pytest.fixture(scope="module")
def provide_token():
    try:
        token = generate_only_token(key, secret, access_token_url)
        return token
    except Exception as e:
        pytest.fail(f"Failed to generate token: {str(e)}")

@allure.epic("Test Interactions With Bitbucket via API")
@allure.story("Repository Creation In Bitbucket")
@allure.title("Test repository creation via API in Bitbucket")
def test_create_repository(provide_headers, api_urls, repository_name):

    with allure.step("Creating repository " + str(repository_name)):
        url = api_urls["repository_url"]
        payload = repository_payload.copy()

        # Set repo properties with unique name
        payload["name"] = repository_name

        try:
            response = requests.post(
                url,
                data=json.dumps(payload),
                headers=provide_headers
            )

            # Assert status code
            assert response.status_code == 200, f"Failed to create repository: {response.text}"

            # Assert response content
            with allure.step("Verify response"):
                repo_data = response.json()
                assert repo_data["scm"] == "git"
                assert repo_data["is_private"] == True
                assert repository_name in repo_data["name"]

                print(f"Created repository: {repository_name}")

        except requests.RequestException as e:
            pytest.fail(f"API request failed: {str(e)}")


@allure.epic("Test Interactions With Bitbucket via API")
@allure.story("Repository Validation In Bitbucket")
@allure.title("Test repository validation via API in Bitbucket")
def test_validate_repository(provide_headers, api_urls, repository_name):

    with allure.step("Validating repository " + str(repository_name)):
        try:
            response = requests.get(
                api_urls["repository_url"],
                headers=provide_headers
            )

            # Assert status code
            assert response.status_code == 200, f"Repository validation failed: {response.text}"

            # Assert response content
            with allure.step("Verify response"):
                repo_data = response.json()
                assert repo_data["name"] == repository_name
                print(f"Validated repository: {repository_name}")

        except requests.RequestException as e:
            pytest.fail(f"API request failed: {str(e)}")

@allure.epic("Test Interactions With Bitbucket via API")
@allure.story("Commit Into Bitbucket Repository")
@allure.title("Test commit into Bitbucket via API")
def test_make_commit(provide_token, api_urls):

    headers = {"Authorization": f"Bearer {provide_token}"}

    with allure.step("Commiting a file to  " + str(api_urls["commit_url"])):
        try:
            # Add a file with content
            test_content = f"Test content added at {uuid.uuid4()}"
            files = {"README.md": test_content}

            response = requests.post(
                api_urls["commit_url"],
                data=commit_message,
                files=files,
                headers=headers
            )

            # Assert status code and validate response data
            with allure.step("Verify response"):
                assert response.status_code == 201, f"Failed to create commit: {response.text}"
                print("Commiting a file to  " + str(api_urls["commit_url"]))

        except requests.RequestException as e:
            pytest.fail(f"API request failed: {str(e)}")


@allure.epic("Test Interactions With Bitbucket via API")
@allure.story("Repository Branch Creation In Bitbucket")
@allure.title("Test branch creation in Bitbucket via API")
def test_create_branch(provide_token, api_urls):

    headers = {"Authorization": f"Bearer {provide_token}"}
    branch_name = f"feature-{uuid.uuid4().hex[:6]}"

    with allure.step("Creating a branch: " + str(branch_name)):
        # Passing unique branch name
        branch_payload = {
            "name": branch_name,
            "target": {
                "hash": "main"
            }
        }

        try:
            response = requests.post(
            api_urls["branches_url"],
            json=branch_payload,
            headers=headers)

            # Assert status code and validate response data
            with allure.step("Verify response"):
                assert response.status_code == 201, f"Failed to create branch: {response.text}"
                branch_info = response.json()
                assert branch_info["name"] == branch_name, "Branch name doesn't match"
                assert branch_info["target"]["hash"] is not None, "Branch target hash not found"
                print("Creating a branch: " + str(branch_name))

        except requests.RequestException as e:
            pytest.fail(f"API request failed: {str(e)}")


@allure.epic("Test Interactions With Bitbucket via API")
@allure.story("Repository Branch Deletion In Bitbucket")
@allure.title("Test branch deletion in Bitbucket via API")
#@pytest.mark.skip
def test_delete_repository(provide_headers, repository_name):

    url = f"{workspace_url}{repository_name}"

    with allure.step("Deleting repository: " + str(url)):
        try:
            delete_response = requests.delete(url, headers=provide_headers)
            print("Deleting repository: " + url)
            print(f"Repository cleanup status: {delete_response.status_code}")
        except Exception as e:
            print(f"Warning: Failed to clean up repository: {str(e)}")