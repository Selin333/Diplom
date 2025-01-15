import os
import time
import wmi
import pygetwindow as pgw
import logging
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.generator import BytesGenerator
from email import encoders
from email.mime.base import MIMEBase
from io import BytesIO
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
IMAP_SERVER = 'imap.yandex.ru'
EMAIL_USER = 'mail4studying@yandex.ru'  # Ваш адрес
EMAIL_PASSWORD = 'udizppjkqpkpjlzk'
def check_existing_emails():
    """
    Проверяет, есть ли письма от observer в папке INBOX.
    """
    try:
        with imaplib.IMAP4_SSL(IMAP_SERVER) as mail:
            mail.login(EMAIL_USER, EMAIL_PASSWORD)
            mail.select("INBOX")
            subject = 'Уведомление об НСД!'
            subject_utf7 = subject.encode('utf-7').decode('ascii')
            search_criteria = f'(HEADER Subject "{subject_utf7}")'
            status, messages = mail.search(None, search_criteria)
            return len(messages[0].split()) > 0
    except Exception as e:
        print(f"Ошибка при проверке писем: {e}")
        return False


print(check_existing_emails())
