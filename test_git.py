import os, uuid
import shutil
import pytest
from git import Repo
from dotenv import load_dotenv


load_dotenv()
user_alias = os.environ.get('user_alias')
user_alias_password = os.environ.get('user_alias_password')
repository_token = os.environ.get('repository_token')
repository_email = os.environ.get('repository_email')
content_to_add = "Modified content " + str(uuid.uuid4())[:4]
commit_message = "file changed locally"


@pytest.fixture
def prepare_directory():
    local_dir = "./repo_clone_" + str(uuid.uuid4())[:4]
    if os.path.exists(local_dir):
        shutil.rmtree(local_dir)
    os.makedirs(local_dir, exist_ok=True)
    return local_dir


@pytest.fixture()
def clone_repository(prepare_directory):
    directory = prepare_directory
    try:
        repository = Repo.clone_from(repository_token, directory)
        return repository
    except Exception as e:
        pytest.fail(f"Failed to clone repository: {str(e)}")


@pytest.fixture()
def modify_file_in_local_repo(prepare_directory):
    file_path = prepare_directory + "/README.md"
    try:
        with open(file_path, 'w') as file:
            file.write(content_to_add)
        return file_path
    except Exception as e:
        pytest.fail(f"Failed to modify file: {str(e)}")


def test_commit_and_push(clone_repository, modify_file_in_local_repo):
    repository = clone_repository
    with repository.config_writer() as config:
        config.set_value("user", "email", repository_email)
        config.set_value("user", "name", "admin_approved_user")

    repository.git.add('--all')
    repository.git.commit('-m', commit_message)
    repository.git.push()


