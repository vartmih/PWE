from datetime import datetime
from http.cookiejar import CookieJar

from httpx import AsyncClient


class TestTodo:
    """Класс тестирования API для операций с задачами"""
    todo_data = {
        "todo": "test",
    }

    todo_update_data = {
        "todo": "test_update",
    }

    report_valid_formats = ('csv', 'xlsx')
    invalid_report_formats = ('pdf', 'html')

    @staticmethod
    async def get_todo_id(client: AsyncClient, cookie: CookieJar) -> str:
        """
        Возвращает список всех задач

        Parameters:
            client: асинхронный клиент для работы с API
            cookie: куки для авторизации
        :return: список всех задач
        """
        response = await client.get(url="/todos", cookies=cookie)
        todo_id = response.json()[0]['id']
        return todo_id

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
            assert todo['status'] == status['status_name']

    async def test_get_todos_list(self, client: AsyncClient, cookie: CookieJar) -> None:
        response = await client.get(url="/todos", cookies=cookie)

        assert response.status_code == 200
        assert len(response.json()) == 5

    async def test_update_todo(self, client: AsyncClient, cookie: CookieJar) -> None:
        todo_id = await self.get_todo_id(client=client, cookie=cookie)

        response = await client.patch(url=f"/todos/{todo_id}", json=self.todo_update_data, cookies=cookie)
        todo = response.json()

        bad_request_response = await client.patch(url=f"/todos/{todo_id}", json={}, cookies=cookie)
        error = bad_request_response.json()

        assert response.status_code == 200
        assert todo['todo'] == self.todo_update_data['todo']

        assert bad_request_response.status_code == 400
        assert error['detail'] == 'Необходимо передать хотя бы один параметр для обновления задачи'

    async def test_get_report(self, client: AsyncClient, cookie: CookieJar) -> None:
        for report_format in self.report_valid_formats:
            response = await client.get(url=f"/todos/report?report_format={report_format}", cookies=cookie)
            file = response.content

            assert response.status_code == 200
            assert isinstance(file, bytes)

        for report_format in self.invalid_report_formats:
            response = await client.get(url=f"/todos/report?report_format={report_format}", cookies=cookie)
            error = response.json()

            assert response.status_code == 400
            assert error['detail'] == f'Возможные форматы отчета: csv или xlsx. Был запрошен формат - {report_format}'

    async def test_delete_todo(self, client: AsyncClient, cookie: CookieJar) -> None:
        todo_id = await self.get_todo_id(client=client, cookie=cookie)

        response = await client.delete(url=f"/todos/{todo_id}", cookies=cookie)
        data = response.json()

        bad_request_response = await client.delete(url=f"/todos/{todo_id}", cookies=cookie)
        error = bad_request_response.json()

        assert response.status_code == 200
        assert data['message'] == 'Задача успешно удалена'

        assert bad_request_response.status_code == 404
        assert error['detail'] == 'Задача не найдена'
