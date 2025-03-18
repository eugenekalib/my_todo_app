import pytest
from app import app, tasks

@pytest.fixture
def client():
    # Создаём тестовый клиент Flask
    with app.test_client() as client:
        yield client

def test_create_task(client):
    # Перед началом очищаем список
    tasks.clear()

    # Отправляем POST-запрос на /create
    response = client.post("/create", data={"title": "Test Task"}, follow_redirects=True)
    
    # Проверяем, что перенаправило на главную страницу
    assert response.status_code == 200
    # Проверяем, что новая задача добавилась
    assert b"Test Task" in response.data
    assert len(tasks) == 1

def test_edit_task(client):
    tasks.clear()
    tasks.append("Old Task")

    # Редактируем
    response = client.post("/edit/0", data={"title": "New Task"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"New Task" in response.data
    assert tasks[0] == "New Task"

def test_delete_task(client):
    tasks.clear()
    tasks.extend(["Task A", "Task B"])

    response = client.get("/delete/0", follow_redirects=True)
    assert response.status_code == 200
    # На странице уже должна быть только Task B
    assert b"Task A" not in response.data
    assert b"Task B" in response.data
    assert len(tasks) == 1