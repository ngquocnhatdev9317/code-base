from conftest import BaseAuthTestCase, BaseTestCase
from tests.mockup import mock_user


class TestAuthenticationLogin(BaseTestCase):
    async def test_login_api_return_correct_when_send_correct_parameters(self):
        await mock_user(1, email="emailTest1@email.com", password="abc")

        response = await self.client_post(
            "/auth/login",
            data={"email": "emailTest1@email.com", "password": "abc"},
        )
        response_json = await response.json()

        self.assertEqual(response.status, 200)
        self.assertEqual(response_json["status"], True)
        self.assertEqual(response_json["status_code"], 200)
        self.assertIn("access_token", response_json["result"])
        self.assertIn("refresh_token", response_json["result"])

    async def test_login_api_return_error_when_send_miss_parameters(self):
        await mock_user(1, email="emailTest2@email.com", password="abc")

        response = await self.client_post(
            "/auth/login",
            data={"email": "emailTest2@email.com"},
        )
        response_json = await response.json()

        self.assertEqual(response.status, 422)
        self.assertEqual(response_json["status"], False)
        self.assertEqual(response_json["status_code"], 422)


class TestAuthenticationLogout(BaseAuthTestCase):
    async def test_logout_api_return_correct_when_send_correct_token(self):
        await self.login_test()
        response = await self.client_delete("/auth/logout", headers={"Authorization": self.authentication_header})

        self.assertEqual(response.status, 204)

    async def test_authentication_failure_when_send_miss_header(self):
        response = await self.client_delete("/auth/logout")
        response_json = await response.json()

        self.assertEqual(response.status, 401)
        self.assertEqual(response_json["status"], False)
        self.assertEqual(response_json["status_code"], 401)
        self.assertEqual(response_json["error_detail"]["message"], "Missing authorization header")

    async def test_authentication_failure_when_send_wrong_token(self):
        response = await self.client_delete("/auth/logout", headers={"Authorization": "Bearer wrong.token"})
        response_json = await response.json()

        self.assertEqual(response.status, 401)
        self.assertEqual(response_json["status"], False)
        self.assertEqual(response_json["status_code"], 401)
        self.assertEqual(response_json["error_detail"]["message"], "Invalid access token")

    async def test_authentication_failure_when_send_wrong_authentication_method(self):
        response = await self.client_delete("/auth/logout", headers={"Authorization": "APIKey this.is.token"})
        response_json = await response.json()

        self.assertEqual(response.status, 401)
        self.assertEqual(response_json["status"], False)
        self.assertEqual(response_json["status_code"], 401)
        self.assertEqual(response_json["error_detail"]["message"], "Invalid token scheme")
