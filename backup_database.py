import os
import smtplib
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env file
load_dotenv()

# Email configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# Backup function
def backup_database():
    try:
        # Create backup directory if it doesn't exist
        backup_dir = "backup"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Generate backup file name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"database_backup_{timestamp}.sql")

        # Simulate database backup (Replace with actual backup command if needed)
        with open(backup_file, "w") as file:
            file.write("-- Simulated database backup content --")

        send_email("Backup Successful", f"Backup completed successfully. File: {backup_file}")
        print(f"Backup successful: {backup_file}")

    except Exception as e:
        send_email("Backup Failed", f"Backup failed with error: {e}")
        print(f"Backup failed: {e}")

# Email sending function
def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = subject

        # Email body
        msg.attach(MIMEText(body, "plain"))

        # Send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Schedule the backup at 00:00 daily
schedule.every().day.at("00:00").do(backup_database)

print("Backup script is running... Press Ctrl+C to exit.")
while True:
    schedule.run_pending()
    time.sleep(1)
