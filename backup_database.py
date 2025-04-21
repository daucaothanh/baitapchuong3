import os
import smtplib
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pytz

# Tải biến môi trường từ file .env
load_dotenv("email.env")

# Cấu hình email
EMAIL_GUI = os.getenv("SENDER_EMAIL")
MAT_KHAU = os.getenv("SENDER_PASSWORD")
EMAIL_NHAN = os.getenv("RECEIVER_EMAIL")

# Thiết lập múi giờ cho lịch trình
local_timezone = pytz.timezone('Asia/Ho_Chi_Minh')  # Sử dụng múi giờ của Việt Nam

# Hàm sao lưu cơ sở dữ liệu
def sao_luu_co_so_du_lieu():
    try:
        # Tạo thư mục lưu backup nếu chưa tồn tại
        thu_muc_backup = "backup"
        if not os.path.exists(thu_muc_backup):
            os.makedirs(thu_muc_backup)

        # Tạo tên file backup kèm dấu thời gian
        thoi_gian = datetime.now(local_timezone).strftime("%Y%m%d_%H%M%S")  # Chú ý thời gian dùng múi giờ đúng
        ten_file_backup = os.path.join(thu_muc_backup, f"database_backup_{thoi_gian}.sql")

        # Mô phỏng sao lưu (thay bằng lệnh thực khi cần)
        with open(ten_file_backup, "w", encoding="utf-8") as f:
            f.write("-- Nội dung sao lưu cơ sở dữ liệu mẫu --")

        # Gửi email thông báo thành công
        gui_email("Sao lưu thành công", f"Backup hoàn tất: {ten_file_backup}")
        print(f"Sao lưu thành công: {ten_file_backup}")

    except Exception as loi:
        # Gửi email thông báo thất bại
        gui_email("Sao lưu thất bại", f"Lỗi khi sao lưu: {loi}")
        print(f"Sao lưu thất bại: {loi}")

# Hàm gửi email
def gui_email(tieu_de, noi_dung):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_GUI
        msg["To"] = EMAIL_NHAN
        msg["Subject"] = tieu_de
        msg.attach(MIMEText(noi_dung, "plain"))

        # Kết nối và gửi qua Gmail SMTP
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_GUI, MAT_KHAU)
            server.send_message(msg)

        print("Gửi email thành công.")
    except Exception as loi:
        print(f"Gửi email thất bại: {loi}")

# Lên lịch chạy hằng ngày lúc 00:00 theo múi giờ
def job():
    now = datetime.now(local_timezone)
    print(f"Thời gian hiện tại: {now}")
    sao_luu_co_so_du_lieu()

schedule.every().day.at("00:00").do(job)  # Lên lịch thực hiện sao lưu lúc 00:00

print("Script sao lưu đang chạy... Nhấn Ctrl+C để dừng.")
while True:
    schedule.run_pending()
    time.sleep(60)  # Kiểm tra mỗi phút một lần
