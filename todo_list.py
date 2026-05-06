import json

try:
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
except:
    tasks = []

completed_tasks = []


def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f)


while True:
    print("\n1 - Показать задачи")
    print("2 - Добавить задачу")
    print("3 - Удалить задачу")
    print("4 - Отметить выполненной")
    print("5 - Вернуть выполненную")
    print("6 - Выход")

    choice = input("Выбери: ")

    # ПОКАЗАТЬ
    if choice == "1":
        if len(tasks) == 0:
            print("Список пуст")
        else:
            for i, task in enumerate(tasks):
                print(i + 1, "-", task["title"])

    # ДОБАВИТЬ
    elif choice == "2":
        title = input("Новая задача: ")

        task = {
            "title": title,
            "done": False
        }

        tasks.append(task)

        save_tasks()

        print("Добавлено")

    # УДАЛИТЬ
    elif choice == "3":
        if len(tasks) == 0:
            print("Список пуст")
        else:
            number = int(input("Номер задачи: "))
            tasks.pop(number - 1)

            save_tasks()

            print("Удалено")

    # ОТМЕТИТЬ ВЫПОЛНЕННОЙ
    elif choice == "4":
        number = int(input("Номер задачи: "))

        task = tasks.pop(number - 1)
        completed_tasks.append(task)

        save_tasks()

        print("Задача выполнена ✔")

    # ВЕРНУТЬ ЗАДАЧУ
    elif choice == "5":
        if len(completed_tasks) == 0:
            print("Нет выполненных задач")
        else:
            print("\nВыполненные задачи:")
            for i, task in enumerate(completed_tasks):
                print(i + 1, "-", task["title"])

            number = int(input("Какую вернуть: "))

            task = completed_tasks.pop(number - 1)
            tasks.append(task)

            save_tasks()

            print("Задача возвращена ↩")

    # ВЫХОД
    elif choice == "6":
        print("Выход")
        break

    else:
        print("Неверная команда")
