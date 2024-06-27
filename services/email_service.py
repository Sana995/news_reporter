import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import logging

load_dotenv()

#subject = "Testing"
#body = '''This is the body of the text message'''

def send_email(subject, body):
    sender = os.environ["EMAIL_SENDER"]
    recipients = os.environ["EMAIL_RECIPIENTS"]
    password = os.environ["EMAIL_APP_PASSWORD"]
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    logging.info("Message sent!")

