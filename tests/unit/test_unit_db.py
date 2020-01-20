import os
from host_setup.datab import DataB
import pytest


def test_create_connection(test_data_dir):
    path = os.path.join(test_data_dir, "output/db.db")
    db = DataB(path)
    print(db.conn)
    assert os.path.exists(path)


def test_create_new_table(test_data_dir):
    path = os.path.join(test_data_dir, "output/db.db")
    db = DataB(path)
    db.create_new_table()


def test_create_task(test_data_dir):
    path = os.path.join(test_data_dir, "output/db.db")
    task_1 = ("Analyze the requirements of the app", 1, 1, "2015-01-01", "2015-01-02")
    task_2 = ("sdf", 0, 0, "2015-01-01", "2015-01-02")
    task_3 = ("aaa", 0, 1, "2015-01-01", "2015-01-02")
    task_4 = ("bbb", 0, 2, "2015-01-01", "2015-01-02")

    db = DataB(path)
    db.create_task(task_1)
    db.create_task(task_2)
    db.create_task(task_3)
    db.create_task(task_4)

    db.commit_changes()

    tasks = db.select_all_tasks()
    print(tasks)


def test_select_all_tasks(test_data_dir):
    path = os.path.join(test_data_dir, "output/db.db")
    db = DataB(path)
    tasks = db.select_all_tasks()
    print(f"all tasks : {tasks}")


def test_select_task_by_param(test_data_dir):
    path = os.path.join(test_data_dir, "output/db.db")
    db = DataB(path)
    tasks = db.select_task_by_param("priority", 0)
    print(f"tasks by priority {tasks}")


def test_update_task(test_data_dir):
    path = os.path.join(test_data_dir, "output/db.db")
    db = DataB(path)
    task_data = ("bbb", 0, 2, "2015-01-01", "2015-01-02", 0)
    db.update_task(task_data)


def test_update_param(test_data_dir):
    path = os.path.join(test_data_dir, "output/db.db")
    db = DataB(path)
    db.update_task_param("status_id", 2, 0)


def test_delete_task(test_data_dir):
    path = os.path.join(test_data_dir, "output/db.db")
    db = DataB(path)
    db.delete_task(0)


def test_delete_all_task(test_data_dir):
    path = os.path.join(test_data_dir, "output/db.db")
    db = DataB(path)
    db.delete_all_tasks()
    assert len(db.select_all_tasks()) == 0


def test_delete_db(test_data_dir):
    path = os.path.join(test_data_dir, "output/db.db")
    db = DataB(path)
    db.delete_database()
    assert not os.path.exists(path)
