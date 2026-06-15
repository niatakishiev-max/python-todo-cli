from todo_list import (
    normalize_task,
    load_data,
    save_data,
    move_task_to_completed,
    restore_completed_task,
)


def test_normalize_task_from_string():
    task = normalize_task("Купить хлеб")

    assert task == {
        "title": "Купить хлеб",
        "done": False,
        "reminder": None,
        "reminded": False
    }


def test_normalize_task_from_dict():
    task = normalize_task({
        "title": "Позвонить клиенту",
        "done": True,
        "reminder": "2026-06-15 18:30",
        "reminded": False
    })

    assert task == {
        "title": "Позвонить клиенту",
        "done": True,
        "reminder": "2026-06-15 18:30",
        "reminded": False
    }


def test_normalize_task_with_missing_fields():
    task = normalize_task({
        "title": "Задача без всех полей"
    })

    assert task == {
        "title": "Задача без всех полей",
        "done": False,
        "reminder": None,
        "reminded": False
    }


def test_load_data_missing_file(tmp_path):
    file_path = tmp_path / "missing_tasks.json"

    tasks, completed_tasks = load_data(file_path)

    assert tasks == []
    assert completed_tasks == []


def test_save_and_load_data(tmp_path):
    file_path = tmp_path / "tasks.json"

    tasks = [
        {
            "title": "Купить хлеб",
            "done": False,
            "reminder": None,
            "reminded": False
        }
    ]

    completed_tasks = [
        {
            "title": "Позвонить клиенту",
            "done": True,
            "reminder": None,
            "reminded": False
        }
    ]

    save_data(file_path, tasks, completed_tasks)

    loaded_tasks, loaded_completed_tasks = load_data(file_path)

    assert loaded_tasks == tasks
    assert loaded_completed_tasks == completed_tasks


def test_move_task_to_completed():
    tasks = [
        {
            "title": "Купить хлеб",
            "done": False,
            "reminder": None,
            "reminded": False
        }
    ]

    completed_tasks = []

    move_task_to_completed(tasks, completed_tasks, 0)

    assert tasks == []
    assert completed_tasks == [
        {
            "title": "Купить хлеб",
            "done": True,
            "reminder": None,
            "reminded": False
        }
    ]


def test_restore_completed_task():
    tasks = []

    completed_tasks = [
        {
            "title": "Купить хлеб",
            "done": True,
            "reminder": None,
            "reminded": False
        }
    ]

    restore_completed_task(tasks, completed_tasks, 0)

    assert completed_tasks == []
    assert tasks == [
        {
            "title": "Купить хлеб",
            "done": False,
            "reminder": None,
            "reminded": False
        }
    ]
