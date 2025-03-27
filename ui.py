# ui.py
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from datetime import datetime, timedelta
from task import Task
from database import Database

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Công việc Pro")
        self.root.geometry("800x700")
        self.root.configure(bg="#f0f0f0")

        self.db = Database()
        self.tasks = self.db.get_all_tasks()
        self.check_due_dates()

        self.create_widgets()

    def create_widgets(self):
        # Tiêu đề
        tk.Label(self.root, text="Quản lý Công việc", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333").pack(pady=10)

        # Khung nhập liệu
        entry_frame = tk.Frame(self.root, bg="#f0f0f0")
        entry_frame.pack(pady=5)
        tk.Label(entry_frame, text="Công việc:", bg="#f0f0f0", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.task_entry = tk.Entry(entry_frame, width=40, font=("Arial", 10))
        self.task_entry.pack(side=tk.LEFT)
        self.category_var = tk.StringVar(value="Cá nhân")
        tk.OptionMenu(entry_frame, self.category_var, "Học tập", "Công việc", "Cá nhân").pack(side=tk.LEFT, padx=5)
        self.priority_var = tk.StringVar(value="Thấp")
        tk.OptionMenu(entry_frame, self.priority_var, "Cao", "Trung bình", "Thấp").pack(side=tk.LEFT, padx=5)
        tk.Button(entry_frame, text="Thêm", command=self.add_task).pack(side=tk.LEFT, padx=5)

        # Khung tìm kiếm
        search_frame = tk.Frame(self.root, bg="#f0f0f0")
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Tìm kiếm:", bg="#f0f0f0", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=40, font=("Arial", 10))
        self.search_entry.pack(side=tk.LEFT)
        self.search_entry.bind("<KeyRelease>", self.search_tasks)

        # Danh sách công việc
        self.task_tree = ttk.Treeview(self.root, columns=("ID", "Description", "Category", "Priority", "Status", "Created", "Due"), show="headings", height=20)
        self.task_tree.heading("ID", text="ID")
        self.task_tree.heading("Description", text="Công việc")
        self.task_tree.heading("Category", text="Danh mục")
        self.task_tree.heading("Priority", text="Ưu tiên")
        self.task_tree.heading("Status", text="Trạng thái")
        self.task_tree.heading("Created", text="Ngày tạo")
        self.task_tree.heading("Due", text="Hết hạn")
        self.task_tree.column("ID", width=30)
        self.task_tree.column("Description", width=250)
        self.task_tree.column("Category", width=100)
        self.task_tree.column("Priority", width=80)
        self.task_tree.column("Status", width=100)
        self.task_tree.column("Created", width=150)
        self.task_tree.column("Due", width=120)
        self.task_tree.pack(pady=10)
        self.task_tree.bind("<<TreeviewSelect>>", self.on_task_select)  # Thêm sự kiện chọn dòng
        self.update_task_tree()

        # Thanh cuộn
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.task_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.task_tree.configure(yscrollcommand=scrollbar.set)

        # Nút chức năng
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Chỉnh sửa", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Xóa", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Hoàn thành", command=self.toggle_complete).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Lưu", command=self.save_and_exit).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Sắp xếp theo Hết hạn", command=lambda: self.sort_tasks("due_date")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Sắp xếp theo Trạng thái", command=lambda: self.sort_tasks("completed")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Sắp xếp theo Ưu tiên", command=lambda: self.sort_tasks("priority")).pack(side=tk.LEFT, padx=5)

    def on_task_select(self, event):
        """Sự kiện khi chọn một dòng trong bảng: điền thông tin công việc vào các ô nhập liệu"""
        try:
            selected_item = self.task_tree.selection()[0]
            task_id = self.task_tree.item(selected_item, "tags")[0]
            task_index = next(i for i, t in enumerate(self.tasks) if str(t.id) == task_id)
            task = self.tasks[task_index]
            # Điền thông tin công việc vào các ô nhập liệu
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, task.description)
            self.category_var.set(task.category)
            self.priority_var.set(task.priority)
        except IndexError:
            pass

    def add_task(self):
        description = self.task_entry.get().strip()
        if description:
            due_date = simpledialog.askstring("Ngày hết hạn", "Nhập ngày hết hạn (YYYY-MM-DD):", parent=self.root)
            if due_date and not self.validate_date(due_date):
                messagebox.showwarning("Cảnh báo", "Định dạng ngày không hợp lệ! Vui lòng nhập theo YYYY-MM-DD.")
                return
            task = Task(description, self.category_var.get(), self.priority_var.get(), due_date=due_date)
            task_id = self.db.add_task(task)
            self.tasks = self.db.get_all_tasks()
            self.update_task_tree()
            self.check_due_dates()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập công việc!")

    def edit_task(self):
        try:
            selected_item = self.task_tree.selection()[0]
            task_id = self.task_tree.item(selected_item, "tags")[0]
            task_index = next(i for i, t in enumerate(self.tasks) if str(t.id) == task_id)
            new_description = self.task_entry.get().strip()
            if new_description:
                due_date = simpledialog.askstring("Ngày hết hạn", "Nhập ngày hết hạn mới (YYYY-MM-DD):", parent=self.root)
                if due_date and not self.validate_date(due_date):
                    messagebox.showwarning("Cảnh báo", "Định dạng ngày không hợp lệ! Vui lòng nhập theo YYYY-MM-DD.")
                    return
                self.tasks[task_index].description = new_description
                self.tasks[task_index].category = self.category_var.get()
                self.tasks[task_index].priority = self.priority_var.get()
                if due_date:
                    self.tasks[task_index].due_date = due_date
                self.db.update_task(int(task_id), self.tasks[task_index])
                self.tasks = self.db.get_all_tasks()
                self.update_task_tree()
                self.check_due_dates()
                self.task_entry.delete(0, tk.END)
                self.category_var.set("Cá nhân")
                self.priority_var.set("Thấp")
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập nội dung mới!")
        except IndexError:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn công việc để chỉnh sửa!")

    def delete_task(self):
        try:
            selected_item = self.task_tree.selection()[0]
            task_id = self.task_tree.item(selected_item, "tags")[0]
            if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa công việc này?"):
                self.db.delete_task(int(task_id))
                self.tasks = self.db.get_all_tasks()
                self.update_task_tree()
                self.check_due_dates()
        except IndexError:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn công việc để xóa!")

    def toggle_complete(self):
        try:
            selected_item = self.task_tree.selection()[0]
            task_id = self.task_tree.item(selected_item, "tags")[0]
            task_index = next(i for i, t in enumerate(self.tasks) if str(t.id) == task_id)
            self.tasks[task_index].completed = not self.tasks[task_index].completed
            self.db.update_task(int(task_id), self.tasks[task_index])
            self.tasks = self.db.get_all_tasks()
            self.update_task_tree()
            self.check_due_dates()
        except IndexError:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn công việc để thay đổi trạng thái!")

    def search_tasks(self, event=None):
        query = self.search_entry.get().lower()
        self.update_task_tree(query=query)

    def sort_tasks(self, key):
        if key == "due_date":
            self.tasks.sort(key=lambda x: x.due_date or "9999-12-31")
        elif key == "completed":
            self.tasks.sort(key=lambda x: x.completed)
        elif key == "priority":
            priority_order = {"Cao": 0, "Trung bình": 1, "Thấp": 2}
            self.tasks.sort(key=lambda x: priority_order[x.priority])
        self.update_task_tree()

    def update_task_tree(self, query=None):
        self.task_tree.delete(*self.task_tree.get_children())
        today = datetime.now().date()
        one_day_before = today + timedelta(days=1)
        for i, task in enumerate(self.tasks):
            if not query or query in task.description.lower():
                status = "Hoàn thành" if task.completed else "Chưa hoàn thành"
                due_date = task.due_date if task.due_date else "Chưa đặt"
                values = (i + 1, task.description, task.category, task.priority, status, task.created_at, due_date)
                # Gán tag cho trạng thái và công việc sắp hết hạn
                tags = []
                if status == "Chưa hoàn thành":
                    tags.append("not_completed")
                else:
                    tags.append("completed")
                if task.due_date and datetime.strptime(task.due_date, "%Y-%m-%d").date() <= one_day_before and not task.completed:
                    tags.append("due_soon")
                self.task_tree.insert("", "end", values=values, tags=(str(task.id), *tags))
        # Cấu hình màu cho các tag
        self.task_tree.tag_configure("not_completed", foreground="red")
        self.task_tree.tag_configure("completed", foreground="green")
        self.task_tree.tag_configure("due_soon", foreground="red")

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def check_due_dates(self):
        today = datetime.now().date()
        one_day_before = today + timedelta(days=1)
        for task in self.tasks:
            if task.due_date and not task.completed:
                due_date = datetime.strptime(task.due_date, "%Y-%m-%d").date()
                if due_date == one_day_before:
                    messagebox.showinfo("Thông báo", f"Công việc '{task.description}' sẽ hết hạn vào ngày mai ({task.due_date})!")

    def save_and_exit(self):
        self.root.quit()