from conftest import BaseTestCase


class TestCommon(BaseTestCase):
    async def test_heathcheck_api_return_correct(self):
        request = self.client.get("/")
        response = await request
        text = await response.text()

        self.assertEqual(response.status, 200)
        self.assertEqual(text, "Welcome to home page")
