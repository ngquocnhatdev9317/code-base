from subprocess import PIPE, Popen, run
from unittest import TestCase


class TestManageAiohttpFile(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        run(
            ["python", "src/manage_aiohttp.py", "init", "dummy_unittest_1"], check=False
        )
        run(
            ["python", "src/manage_aiohttp.py", "init", "dummy_unittest_exist"],
            check=False,
        )

    def test_init_command_should_success_when_database_is_exist(self):
        with Popen(
            ["python", "src/manage_aiohttp.py", "init", "dummy_unittest_1"], stderr=PIPE
        ) as p:
            _, stderr = p.communicate()

        assert 'Database "dummy_unittest_1" already exists' in str(stderr)
        assert 'Init database "dummy_unittest_1" done' in str(stderr)

    def test_init_command_should_success_when_database_is_exist_with_force(self):
        with Popen(
            ["python", "src/manage_aiohttp.py", "-f", "init", "dummy_unittest_1"],
            stderr=PIPE,
        ) as p:
            _, stderr = p.communicate()

        assert 'Create force to exists database "dummy_unittest_1"' in str(stderr)
        assert 'Init database "dummy_unittest_1" done' in str(stderr)

    def test_init_command_should_success_when_database_is_unexist(self):
        with Popen(
            ["python", "src/manage_aiohttp.py", "init", "dummy_unittest_2"],
            stderr=PIPE,
        ) as p:
            _, stderr = p.communicate()

        assert 'Database "dummy_unittest_2" already exists' not in str(stderr)
        assert 'Init database "dummy_unittest_2" done' in str(stderr)

    def test_remove_command_should_success_when_database_is_unexist(self):
        with Popen(
            ["python", "src/manage_aiohttp.py", "remove", "dummy_unittest_unexist"],
            stderr=PIPE,
        ) as p:
            _, stderr = p.communicate()

        assert '"dummy_unittest_unexist" is unexist' in str(stderr)

    def test_remove_command_should_success_when_database_is_exist(self):
        with Popen(
            ["python", "src/manage_aiohttp.py", "remove", "dummy_unittest_exist"],
            stderr=PIPE,
        ) as p:
            _, stderr = p.communicate()

        assert 'Dropped the exists database "dummy_unittest_exist"' in str(stderr)

    @classmethod
    def tearDownClass(cls) -> None:
        run(
            ["python", "src/manage_aiohttp.py", "remove", "dummy_unittest_1"],
            check=False,
        )
        run(
            ["python", "src/manage_aiohttp.py", "remove", "dummy_unittest_2"],
            check=False,
        )
        run(
            ["python", "src/manage_aiohttp.py", "remove", "dummy_unittest_unexist"],
            check=False,
        )
        run(
            ["python", "src/manage_aiohttp.py", "remove", "dummy_unittest_exist"],
            check=False,
        )
