# native imports
import unittest
import os

# custom imports
from main import check_for_repos, copy_files_from_folder


class TestMain(unittest.TestCase):

    # Test copying files from folder
    def test_copy_files_from_folder(self):
        self.assertEqual(200, copy_files_from_folder())

    # Test to see if the service repo does not exist
    def test_check_for_repos_wrong_service_name(self):
        service_name = "hello"
        repositories = [service_name, "infra-terrafrom", "infra-charts", "infra-gitops"]
        path = os.path.expanduser("~/Documents/code")
        ssh_prefix = "git@github.com:amun"
        self.assertEqual(False, check_for_repos(path, repositories, ssh_prefix))

    # Test to see if the service repo does exist
    def test_check_for_repos_right_service_name(self):
        service_name = "hello-world-service-script"
        repositories = [service_name, "infra-terrafrom", "infra-charts", "infra-gitops"]
        path = os.path.expanduser("~/Documents/code")
        ssh_prefix = "git@github.com:amun"
        self.assertEqual(repositories, check_for_repos(path, repositories, ssh_prefix))
