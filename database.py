# database.py
import sqlite3
from task import Task

class Database:
    def __init__(self, db_name="tasks.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    category TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    completed INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    due_date TEXT
                )
            """)

    def add_task(self, task):
        with self.conn:
            cursor = self.conn.execute("""
                INSERT INTO tasks (description, category, priority, completed, created_at, due_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (task.description, task.category, task.priority, task.completed, task.created_at, task.due_date))
            return cursor.lastrowid

    def get_all_tasks(self):
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM tasks")
            tasks = []
            for row in cursor.fetchall():
                task_data = dict(zip(["id", "description", "category", "priority", "completed", "created_at", "due_date"], row))
                task = Task.from_dict(task_data)
                task.id = task_data["id"]  # Gán ID cho đối tượng Task
                tasks.append(task)
            return tasks

    def update_task(self, task_id, task):
        with self.conn:
            self.conn.execute("""
                UPDATE tasks SET description=?, category=?, priority=?, completed=?, created_at=?, due_date=?
                WHERE id=?
            """, (task.description, task.category, task.priority, task.completed, task.created_at, task.due_date, task_id))

    def delete_task(self, task_id):
        with self.conn:
            self.conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))