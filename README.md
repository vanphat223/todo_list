# Ứng dụng Quản lý Công việc (To-Do List)

Đây là một ứng dụng quản lý công việc chuyên nghiệp được viết bằng Python, sử dụng Tkinter để tạo giao diện đồ họa. Ứng dụng hỗ trợ quản lý công việc với các tính năng nâng cao như sắp xếp, phân loại, và thông báo.

## Tính năng
- Thêm, chỉnh sửa, xóa công việc với xác nhận trước khi xóa.
- Phân loại công việc theo danh mục (Học tập, Công việc, Cá nhân).
- Đặt mức độ ưu tiên (Cao, Trung bình, Thấp).
- Đánh dấu công việc hoàn thành/chưa hoàn thành.
- Đặt ngày hết hạn (YYYY-MM-DD) và thông báo trước 1 ngày.
- Sắp xếp công việc theo ngày hết hạn, trạng thái, hoặc ưu tiên.
- Tìm kiếm công việc theo từ khóa.
- Lưu trữ dữ liệu trong SQLite.
- Giao diện hiện đại với màu sắc (công việc chưa hoàn thành hiển thị đỏ, coogn việc hoàn thành hiển thị màu xanh).

## Công nghệ sử dụng
- Ngôn ngữ lập trình: Python
- Thư viện: `tkinter`, `ttk` (giao diện), `sqlite3` (cơ sở dữ liệu), `datetime` (thời gian)

## Hướng dẫn chạy
1. Cài đặt Python 3.x: https://www.python.org/
2. Clone repository về máy:
   ```bash
   git clone https://github.com/phanvanphat/todo_list_pro.git
   cd todo_list