import pytest

# Можно напрямую импортировать список tasks или вынести логику в отдельный модуль utils.
from app import tasks

@pytest.fixture
def setup_tasks():
    # Перед каждым тестом очищаем список или создаём новый
    tasks.clear()
    yield
    # После теста тоже очищаем (на всякий случай)
    tasks.clear()

def test_add_task(setup_tasks):
    tasks.append("Task 1")
    assert len(tasks) == 1
    assert tasks[0] == "Task 1"

def test_delete_task(setup_tasks):
    tasks.append("Task 1")
    tasks.append("Task 2")
    tasks.pop(0)  # Удаляем первую
    assert len(tasks) == 1
    assert tasks[0] == "Task 2"
