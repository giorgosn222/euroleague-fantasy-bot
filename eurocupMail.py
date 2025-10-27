import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

msg = EmailMessage()
msg['Subject'] = 'Automated Email for Fantasy'
msg['From'] = EMAIL_ADDRESS
msg['To'] = EMAIL_ADDRESS
msg.set_content('Reminder to make changes on Fantasy.')

# Path to file
file_path = Path("Eurocup Fantasy 2025-2026.csv")

with open(file_path, 'rb') as f:
  file_data = f.read()
  file_name = file_path.name

msg.add_attachment(
  file_data,
  maintype='application',
  subtype='octet-stream',
  filename=file_name
)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
  smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
  smtp.send_message(msg)

print("Email sent!")