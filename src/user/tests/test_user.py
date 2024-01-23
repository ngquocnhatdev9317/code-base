from conftest import BaseTestCase


class TestUser(BaseTestCase):
    async def test_user_api(self):
        request = self.client.get("/")
        response = await request

        self.assertEqual(response.status, 200)
