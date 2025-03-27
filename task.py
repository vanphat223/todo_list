# task.py
from datetime import datetime

class Task:
    def __init__(self, description, category="Cá nhân", priority="Thấp", completed=False, created_at=None, due_date=None):
        self.id = None  # Thêm thuộc tính id
        self.description = description
        self.category = category
        self.priority = priority
        self.completed = completed
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.due_date = due_date if due_date else None

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "completed": int(self.completed),
            "created_at": self.created_at,
            "due_date": self.due_date
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            data["description"],
            data["category"],
            data["priority"],
            bool(data["completed"]),
            data["created_at"],
            data["due_date"]
        )
        task.id = data.get("id")  # Gán ID từ dữ liệu
        return task