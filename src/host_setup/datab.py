import sqlite3
from sqlite3 import Error
import os
from datetime import datetime
from host_setup.env import Env

DATAB_DEF = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    path text NOT NULL,
                                    priority integer,
                                    status integer NOT NULL,
                                    processing int NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL
                                );"""


def check_db(var):
    if var is not None:
        return var
    else:
        try:
            return os.environ["PLEXDB"]
        except:
            raise EnvironmentError("the db var isn't set")


class DataB:
    def __init__(self, db_path=None):
        self.path = check_db(db_path)
        self.conn = self.create_connection(self.path)
        self.create_new_table()

    def __repr__(self):
        return f"\n{self.__class__.__name__} \n path: {self.path} \n conn: {self.conn} \n tasks: {self.select_all_tasks()}"

    def __str__(self):
        return f"path: {self.path} \n conn: {self.conn} \n tasks: {self.select_all_tasks()}"

    @staticmethod
    def create_connection(db_file):
        """ create a database connection to the SQLite database
         specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn

    @property
    def get_start_time(self):
        # datetime object containing current date and time
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    @property
    def cur(self):
        return self.conn.cursor()

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def create_new_table(self):
        """ create a table from the create_table_sql statement
        :return:
        """
        try:
            self.cur.execute(DATAB_DEF)
        except Error as e:
            print(e)

    def create_new_task(self, name, path, priority=0, status=0, processing=0):
        """
        Create a new task for tracking. this is a helper around _create_task
        :param name : str
        :param priority : int
        :param status : int
        :return: id : int
        """
        task = (name, path, priority, status, processing, self.get_start_time, "-")
        self.create_task(task)

    def create_task(self, task):
        """
        Create a new task
        :param task:
        :return:
        """

        sql = """ INSERT INTO tasks(name,path,priority,status,processing,begin_date,end_date)
                VALUES(?,?,?,?,?,?,?) """
        self.cur.execute(sql, task)
        self.commit()
        return self.cur.lastrowid

    def update_task(self, task):
        """
        update priority, begin_date, and end date of a task
        :param task:
        """
        sql = """ UPDATE tasks
                SET name = ? ,
                    path = ? ,
                    priority = ? ,
                    status = ? ,
                    processing = ? ,
                    begin_date = ? ,
                    end_date = ?
                WHERE id = ?"""
        self.cur.execute(sql, task)
        self.conn.commit()

    def update_task_by_name(self, param, val, name):
        """
        update priority, begin_date, and end date of a task
        :param task:
        """
        sql = f""" UPDATE tasks
                SET {param} = ?
                WHERE name = ?"""
        self.cur.execute(sql, (val, name))
        self.conn.commit()

    def update_task_param(self, param, val, task_id):
        """
        update priority, begin_date, and end date of a task
        :param task:
        """
        sql = f""" UPDATE tasks
                SET {param} = ?
                WHERE id = ?"""
        self.cur.execute(sql, (val, task_id))
        self.conn.commit()

    def select_all_tasks(self):
        """
        Query all rows in the tasks table
        :return:
        """

        return self.cur.execute("SELECT * FROM tasks").fetchall()

    def select_task_by_param(self, param, term):
        """
        Query tasks by priority
        :param priority:
        :return:
        """
        return self.cur.execute(
            f"SELECT * FROM tasks WHERE {param}=?", (term,)
        ).fetchall()

    def get_task_param(self, param, name):
        try:
            result = self.cur.execute(
                f"SELECT {param} FROM tasks WHERE name=?", (name,)
            ).fetchall()
            if len(result) == 0:
                if param == "status" or param == "processing":
                    return 0
                else:
                    return None
            else:
                return result[0][0]
        except:
            return None

    def get_task_status(self, name):
        task = self.select_task_by_param("name", name)
        if len(task) == 0:
            return 0
        elif len(task) == 1:
            return task[0][4]
        else:
            # TODO find something smart to do
            print(task)
            print("there's a problem we should kill one")
            return task[0][4]

    def select_task_status(self, param, term):
        """
        Query tasks 
        :param priority:
        :return:
        """
        return self.cur.execute(
            f"SELECT * FROM tasks WHERE {param}=?", (term,)
        ).fetchall()

    def delete_task(self, id):
        """
        Delete a task by task id
        :param id: id of the task
        :return:
        """
        sql = "DELETE FROM tasks WHERE id=?"
        self.cur.execute(sql, (id,))
        self.conn.commit()

    def delete_all_tasks(self):
        """
        Delete all rows in the tasks table
        :return:
        """
        sql = "DELETE FROM tasks"
        self.cur.execute(sql)
        self.conn.commit()

    def delete_database(self):
        """
        Delete the base .db file
        :return:
        """
        self.close()
        os.remove(self.path)
