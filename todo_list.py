import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "tasks.json"
DATE_FORMAT = "%Y-%m-%d %H:%M"


def normalize_task(task):
    if isinstance(task, str):
        return {
            "title": task,
            "done": False,
            "reminder": None,
            "reminded": False
        }

    return {
        "title": task.get("title", ""),
        "done": task.get("done", False),
        "reminder": task.get("reminder"),
        "reminded": task.get("reminded", False)
    }


def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return [], []
    except json.JSONDecodeError:
        return [], []

    if isinstance(data, list):
        return [normalize_task(task) for task in data], []

    tasks = data.get("tasks", [])
    completed_tasks = data.get("completed_tasks", [])

    return (
        [normalize_task(task) for task in tasks],
        [normalize_task(task) for task in completed_tasks]
    )


def save_data():
    data = {
        "tasks": tasks,
        "completed_tasks": completed_tasks
    }

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


tasks, completed_tasks = load_data()


def get_task_index(tasks_list, message):
    try:
        number = int(input(message))
    except ValueError:
        print("Нужно ввести число")
        return None

    if number < 1 or number > len(tasks_list):
        print("Неверный номер задачи")
        return None

    return number - 1


def get_reminder():
    reminder = input(
        "Напоминание (ГГ-ММ-ДД ЧЧ:ММ) или Enter без напоминания: "
    ).strip()

    if reminder == "":
        return None

    try:
        datetime.strptime(reminder, DATE_FORMAT)
    except ValueError:
        print("Неверный формат даты. Напоминание не добавлено")
        return None

    return reminder


def show_tasks():
    if len(tasks) == 0:
        print("Список пуст")
        return

    for i, task in enumerate(tasks):
        reminder = task.get("reminder")

        if reminder:
            print(i + 1, "-", task["title"], "| напоминание:", reminder)
        else:
            print(i + 1, "-", task["title"])


def show_completed_tasks():
    if len(completed_tasks) == 0:
        print("Нет выполненных задач")
        return

    print("\nВыполненные задачи:")
    for i, task in enumerate(completed_tasks):
        print(i + 1, "-", task["title"])


def add_task():
    title = input("Новая задача: ").strip()

    if title == "":
        print("Название задачи не может быть пустым")
        return

    reminder = get_reminder()

    task = {
        "title": title,
        "done": False,
        "reminder": reminder,
        "reminded": False
    }

    tasks.append(task)
    save_data()

    print("Добавлено")


def delete_task():
    if len(tasks) == 0:
        print("Список пуст")
        return

    index = get_task_index(tasks, "Номер задачи: ")

    if index is None:
        return

    tasks.pop(index)
    save_data()

    print("Удалено")


def complete_task():
    if len(tasks) == 0:
        print("Список пуст")
        return

    index = get_task_index(tasks, "Номер задачи: ")

    if index is None:
        return

    task = tasks.pop(index)
    task["done"] = True
    completed_tasks.append(task)

    save_data()

    print("Задача выполнена")


def restore_task():
    if len(completed_tasks) == 0:
        print("Нет выполненных задач")
        return

    print("\nВыполненные задачи:")
    for i, task in enumerate(completed_tasks):
        print(i + 1, "-", task["title"])

    index = get_task_index(completed_tasks, "Какую вернуть: ")

    if index is None:
        return

    task = completed_tasks.pop(index)
    task["done"] = False
    tasks.append(task)

    save_data()

    print("Задача возвращена")


def check_reminders():
    now = datetime.now()
    has_changes = False

    for task in tasks:
        reminder = task.get("reminder")

        if not reminder:
            continue

        try:
            reminder_time = datetime.strptime(reminder, DATE_FORMAT)
        except ValueError:
            task["reminder"] = None
            task["reminded"] = False
            has_changes = True
            continue

        if reminder_time <= now:
            print("Напоминание:", task["title"])
            task["reminder"] = None
            task["reminded"] = True
            has_changes = True

    if has_changes:
        save_data()


def show_menu():
    print("\n1 - Показать задачи")
    print("2 - Добавить задачу")
    print("3 - Удалить задачу")
    print("4 - Отметить выполненной")
    print("5 - Показать выполненные задачи")
    print("6 - Вернуть выполненную")
    print("7 - Выход")


def main():
    check_reminders()

    while True:
        show_menu()

        choice = input("Выбери: ")

        if choice == "1":
            show_tasks()
        elif choice == "2":
            add_task()
        elif choice == "3":
            delete_task()
        elif choice == "4":
            complete_task()
        elif choice == "5":
            show_completed_tasks()
        elif choice == "6":
            restore_task()
        elif choice == "7":
            print("Выход")
            break
        else:
            print("Неверная команда")



if __name__ == "__main__":
    main()
