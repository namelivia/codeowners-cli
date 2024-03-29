from click.testing import CliRunner
from cli import cli


class TestCli:
    def setup_method(self):
        self.runner = CliRunner()

    def test_getting_owner_of_a_file(self):
        path = "/some/file/path"
        owners_file_path = "/some/owners/file/path"
        result = self.runner.invoke(
            cli,
            ["owners", "get", "--path", path, "--owners_file_path", owners_file_path],
        )
        assert result.exit_code == 0

    def test_suggesting_owner_of_a_file(self):
        path = "/some/file/path"
        owners_file_path = "/some/owners/file/path"
        repo = "some-repo"
        result = self.runner.invoke(
            cli,
            [
                "owners",
                "suggest",
                "--path",
                path,
                "--repo",
                repo,
                "--owners_file_path",
                owners_file_path,
            ],
        )
        assert result.exit_code == 0
