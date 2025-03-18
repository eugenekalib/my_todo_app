import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import threading
import time

from app import app, tasks

@pytest.fixture(scope="module")
def selenium_driver():
    driver = webdriver.Chrome()  # Или firefox и т.д.
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def test_server():
    # Запустим Flask в отдельном потоке
    server = threading.Thread(target=app.run, kwargs={'debug': False, 'use_reloader': False})
    server.start()
    time.sleep(1)  # Дадим серверу время стартовать
    yield
    # Остановка: в реальном проекте может потребоваться дополнительный механизм
    # Здесь для простоты пусть поток "умирает" при завершении тестов

def test_full_flow(selenium_driver, test_server):
    # Очищаем список перед тестом
    tasks.clear()

    base_url = "http://127.0.0.1:5000"
    selenium_driver.get(base_url)

    # Находим поле ввода, вводим текст "Selenium Task", нажимаем "Добавить"
    input_box = selenium_driver.find_element(By.NAME, "title")
    input_box.send_keys("Selenium Task")
    input_box.send_keys(Keys.RETURN)  # Эквивалент нажатия на кнопку

    time.sleep(1)  # Дать время серверу обработать

    # Проверяем, появилась ли задача
    page_source = selenium_driver.page_source
    assert "Selenium Task" in page_source
    assert len(tasks) == 1
