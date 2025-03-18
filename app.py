from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Хранилище (в памяти)
tasks = []

# Для простоты используем простейшие HTML-шаблоны через render_template_string.
# Но при желании можно подключить Jinja2-шаблоны из /templates.

HTML_INDEX = """
<!DOCTYPE html>
<html>
    <head><title>To-Do List</title></head>
    <body>
        <h1>Список задач</h1>
        <form method="POST" action="{{ url_for('create_task') }}">
            <input type="text" name="title" placeholder="Новая задача"/>
            <button type="submit">Добавить</button>
        </form>
        <ul>
            {% for idx, task in enumerate(tasks) %}
                <li>
                    {{task}}
                    <a href="{{ url_for('edit_task', task_id=idx) }}">(Редактировать)</a>
                    <a href="{{ url_for('delete_task', task_id=idx) }}">(Удалить)</a>
                </li>
            {% endfor %}
        </ul>
    </body>
</html>
"""

HTML_EDIT = """
<!DOCTYPE html>
<html>
    <head><title>Редактировать задачу</title></head>
    <body>
        <h1>Редактировать задачу</h1>
        <form method="POST" action="{{ url_for('edit_task', task_id=task_id) }}">
            <input type="text" name="title" value="{{ task }}" />
            <button type="submit">Сохранить</button>
        </form>
        <a href="{{ url_for('index') }}">Назад</a>
    </body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_INDEX, tasks=tasks)

@app.route("/create", methods=["POST"])
def create_task():
    title = request.form.get("title", "").strip()
    if title:
        tasks.append(title)
    return redirect(url_for("index"))

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    # Проверка на выход за границы массива
    if task_id < 0 or task_id >= len(tasks):
        return "Task not found", 404

    if request.method == "GET":
        return render_template_string(HTML_EDIT, task=tasks[task_id], task_id=task_id)
    
    # POST-запрос — сохранить изменения
    title = request.form.get("title", "").strip()
    if title:
        tasks[task_id] = title
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    if task_id < 0 or task_id >= len(tasks):
        return "Task not found", 404
    
    tasks.pop(task_id)
    return redirect(url_for("index"))

# Запуск приложения (локально)
if __name__ == "__main__":
    app.run(debug=True)
