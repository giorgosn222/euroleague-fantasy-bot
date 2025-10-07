import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = 'giorgosn222@gmail.com'
EMAIL_PASSWORD = 'fmbjhvhhzfdxpfki'
RECIPIENT_EMAIL = 'maskereid1@hotmail.com'

msg = EmailMessage()
msg['Subject'] = 'Test Email from Python script'
msg['From'] = EMAIL_ADDRESS
msg['To'] = RECIPIENT_EMAIL
msg.set_content('This is a test email sent from a Python script using Gmail.')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
  smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
  smtp.send_message(msg)

print("Email sent!")