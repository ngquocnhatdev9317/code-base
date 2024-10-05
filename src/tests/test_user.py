from typing import Any, Coroutine

from conftest import BaseTestCase
from tests.mockup import mock_user


class TestUser(BaseTestCase):
    async def set_up_user(self, number=1) -> Coroutine[Any, Any, None]:
        await mock_user(number)

    async def test_user_api_get_should_return_correct_when_database_have_data(self):
        await self.set_up_user(1)
        response = await self.client_get("/users")
        response_json = await response.json()

        self.assertEqual(response.status, 200)
        self.assertEqual(response_json["status"], True)
        self.assertEqual(response_json["status_code"], 200)
        self.assertEqual(len(response_json["result"]), 1)

        await self.set_up_user(10)
        response = await self.client_get("/users")
        response_json = await response.json()

        self.assertEqual(response.status, 200)
        self.assertEqual(response_json["status"], True)
        self.assertEqual(response_json["status_code"], 200)
        self.assertEqual(len(response_json["result"]), 11)

    async def test_user_api_post_should_success_when_send_correct_parameters(self):
        response = await self.client_post(
            "/users",
            data={
                "name": "usernameTest",
                "email": "emailTest@email.com",
                "password": "abc",
            },
        )
        response_json = await response.json()

        self.assertEqual(response.status, 201)
        self.assertEqual(response_json["status"], True)
        self.assertEqual(response_json["status_code"], 200)

    async def test_user_api_post_should_fail_when_send_wrong_parameters(self):
        response = await self.client_post(
            "/users",
            data={
                "name": "usernameTest",
                "wrongfield": "emailTest@email.com",
                "password": "abc",
            },
        )
        response_json = await response.json()
        print(response_json)

        self.assertEqual(response.status, 422)
        self.assertEqual(response_json["status"], False)
        self.assertEqual(response_json["status_code"], 422)
        self.assertEqual(len(response_json["errors_detail"]), 1)

    async def test_user_api_post_should_fail_when_send_miss_parameters(self):
        response = await self.client_post(
            "/users",
            data={
                "name": "usernameTest",
                "password": "abc",
            },
        )
        response_json = await response.json()
        print(response_json)

        self.assertEqual(response.status, 422)
        self.assertEqual(response_json["status"], False)
        self.assertEqual(response_json["status_code"], 422)
        self.assertEqual(len(response_json["errors_detail"]), 1)
