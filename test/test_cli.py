import unittest

from typer.testing import CliRunner

from trellocli import __app_name__, __app_version__, cli

runner = CliRunner()


class TestCLI(unittest.TestCase):
    def test_version(self) -> None:
        result = runner.invoke(cli.app, ['-v'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(f'{__app_name__} v{__app_version__}\n', result.stdout)
