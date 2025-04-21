# Tự Động Sao Lưu Cơ Sở Dữ Liệu

Kho lưu trữ này chứa một script Python thực hiện sao lưu file cơ sở dữ liệu `.sql` hoặc `.sqlite3` hằng ngày vào lúc 00:00 và gửi email thông báo thành công hoặc thất bại.

## 1. Cấu hình

1. Tạo file `email.env` trong thư mục gốc (cùng cấp với `backup_database.py`).
2. Thêm các biến môi trường sau (thay thế bằng thông tin của bạn):

   ```env
   EMAIL_SENDER=youremail@gmail.com
   EMAIL_PASSWORD=your_app_password
   EMAIL_RECEIVER=recipient@example.com
   ```

> **Lưu ý:** Tuyệt đối không commit hoặc push `email.env` lên GitHub. File này đã được liệt kê trong `.gitignore`.

## 2. Cài đặt phụ thuộc

Dùng `pip` để cài các gói cần thiết:

```bash
pip install -r requirements.txt
```

## 3. Chạy script thủ công

Để kiểm thử việc sao lưu và gửi email:

```bash
python backup_database.py
```

- Nếu thành công, bạn sẽ nhận email chứa tên file backup.
- Nếu thất bại, bạn sẽ nhận email thông báo lỗi.

## 4. Tự động với Task Scheduler trên Windows

1. Mở **Task Scheduler**.
2. Chọn **Create Task**.
3. Tab **General**: đặt tên tác vụ (ví dụ: `Database Backup`).
4. Tab **Triggers**: nhấn **New...**, chọn **On a schedule**, **Daily**, thời gian **00:00:00 AM**.
5. Tab **Actions**: nhấn **New...**:
   - **Action**: **Start a program**
   - **Program/script**: đường dẫn đến file `python.exe`, ví dụ:
     ```
     C:\path\to\python.exe
     ```
   - **Add arguments**: đường dẫn đến script, ví dụ:
     ```
     D:\tudonghoaquytrinh\baitapvenhachuong3\backup_database.py
     ```
   - **Start in**: thư mục chứa script, ví dụ:
     ```
     D:\tudonghoaquytrinh\baitapvenhachuong3
     ```
6. Nhấn **OK** để lưu.

Sau khi hoàn thành, script sẽ tự động chạy mỗi đêm lúc nửa đêm và gửi báo cáo qua email.
