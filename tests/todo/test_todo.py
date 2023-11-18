from http.cookiejar import CookieJar

from httpx import AsyncClient


class TestTodo:
    """Класс тестирования API для операций с задачами"""
    todo_data = {
        "todo": "test",
    }

    async def test_get_status(self, client: AsyncClient) -> None:
        response = await client.get(url="/todos/statuses")
        assert response.status_code == 200
        assert len(response.json()) == 5

    async def test_create_todo(self, client: AsyncClient, cookie: CookieJar) -> None:
        statuses_response = await client.get(url="/todos/statuses")
        statuses = statuses_response.json()
        for status in statuses:
            self.todo_data['status_id'] = status['id']
            response = await client.post(url="/todos", json=self.todo_data, cookies=cookie)
            todo = response.json()
            assert response.status_code == 200
            assert todo['todo'] == self.todo_data['todo']
            assert todo['status_id'] == self.todo_data['status_id']

    async def test_get_todos_list(self, client: AsyncClient, cookie: CookieJar) -> None:
        response = await client.get(url="/todos", cookies=cookie)
        assert response.status_code == 200
        assert len(response.json()) == 5
