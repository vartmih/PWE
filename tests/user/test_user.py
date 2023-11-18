from httpx import AsyncClient


class TestUser:
    """Класс тестирования API для операций с пользователями"""
    user_data_for_cookie = {
        "email": "user@example.com",
        "password": "00000000",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "first_name": "Im",
        "last_name": "User",
        "birth_date": "1990-11-18"
    }

    user_data = {
        "email": "user1@example.com",
        "password": "00000000",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "first_name": "Im",
        "last_name": "User",
        "birth_date": "1990-11-18"
    }

    update_user_data = {
        "first_name": "User",
        "last_name": "Im",
    }

    async def test_register_user(self, client: AsyncClient):
        response = await client.post(url="/users/register", json=self.user_data)
        response_data = response.json()
        assert response_data['email'] == self.user_data['email']
        assert response_data['first_name'] == self.user_data['first_name']
        assert response_data['last_name'] == self.user_data['last_name']
        assert response_data['birth_date'] == self.user_data['birth_date']
        assert response_data.get('id')
        assert response.status_code == 201

    async def test_login_user(self, client: AsyncClient):
        credentials = {
            "username": self.user_data['email'],
            "password": self.user_data['password']
        }
        response = await client.post(url="/users/login", data=credentials)
        assert response.status_code == 204

    async def test_get_user(self, client: AsyncClient):
        response = await client.get(url="/users/me")
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['email'] == self.user_data['email']
        assert response_data['first_name'] == self.user_data['first_name']
        assert response_data['last_name'] == self.user_data['last_name']
        assert response_data['birth_date'] == self.user_data['birth_date']

    async def test_update_user(self, client: AsyncClient):
        response = await client.patch(url="/users/me", json=self.update_user_data)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['first_name'] == self.update_user_data['first_name']
        assert response_data['last_name'] == self.update_user_data['last_name']

    async def test_logout_user(self, client: AsyncClient):
        response = await client.post(url="/users/logout")
        assert response.status_code == 204
