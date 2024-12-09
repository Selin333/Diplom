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

# Настройки IMAP
IMAP_SERVER = 'imap.yandex.ru'
EMAIL_USER = 'mail4studying@yandex.ru'  # Ваш адрес
EMAIL_PASSWORD = 'udizppjkqpkpjlzk'

# Настройка логирования
logger = logging.getLogger("observer_notify")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("observer_log.txt")
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def log_action(message, level="INFO"):
    """
    Запись событий в лог.
    """
    if level == "INFO":
        logger.info(message)
    elif level == "ERROR":
        logger.error(message)
    elif level == "WARNING":
        logger.warning(message)

class FileSystemMonitor(FileSystemEventHandler):
    """
    Обработчик событий файловой системы.
    """
    def on_created(self, event):
        log_action(f"Файл создан: {event.src_path}")

    def on_deleted(self, event):
        log_action(f"Файл удалён: {event.src_path}")

    def on_modified(self, event):
        log_action(f"Файл изменён: {event.src_path}")

    def on_moved(self, event):
        log_action(f"Файл перемещён: {event.src_path} -> {event.dest_path}")

class EmailHandler:
    """
    Класс для обработки отправки писем.
    """
    def __init__(self):
        self.last_log_size = 0

    def send_email_to_inbox(self, subject, body, attachment_path=None):
        """
        Отправляет письмо в папку "Входящие".
        """
        try:
            msg = MIMEMultipart()
            msg["From"] = 'observer'
            msg["To"] = EMAIL_USER
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, "rb") as file:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={os.path.basename(attachment_path)}"
                    )
                    msg.attach(part)

            msg_bytes = BytesIO()
            BytesGenerator(msg_bytes).flatten(msg)
            raw_message = msg_bytes.getvalue()

            with imaplib.IMAP4_SSL(IMAP_SERVER) as mail:
                mail.login(EMAIL_USER, EMAIL_PASSWORD)
                mail.append("INBOX", None, None, raw_message)
                logger.info(f"Письмо успешно добавлено в INBOX: {subject}")
        except Exception as e:
            logger.error(f"Ошибка при отправке письма: {e}")

    def check_existing_emails(self):
        """
        Проверяет, есть ли письма от observer в папке INBOX.
        """
        try:
            with imaplib.IMAP4_SSL(IMAP_SERVER) as mail:
                mail.login(EMAIL_USER, EMAIL_PASSWORD)
                mail.select("INBOX")

                from email.header import Header
                subject_encoded = str(Header('Уведомление об НСД!', 'utf-8'))

                # Формируем запрос для поиска писем
                status, messages = mail.search(None, f'HEADER Subject "{subject_encoded}"')

                return len(messages[0].split()) > 0
        except Exception as e:
            logger.error(f"Ошибка при проверке писем: {e}")
            return False

    def send_log_if_updated(self):
        """
        Отправляет обновлённый лог, если лог изменился.
        """
        try:
            log_path = "observer_log.txt"
            current_size = os.path.getsize(log_path)
            is_first_email = not self.check_existing_emails()

            if is_first_email:
                self.send_email_to_inbox(
                    subject="Уведомление об НСД!",
                    body="Лог создан. См. вложение.",
                    attachment_path=log_path
                )
            elif current_size > self.last_log_size:
                self.send_email_to_inbox(
                    subject="Актуализация лога инцидента",
                    body="Лог был обновлён. См. вложение.",
                    attachment_path=log_path
                )
                self.last_log_size = current_size
        except Exception as e:
            logger.error(f"Ошибка при обновлении лога: {e}")

class SystemObserver:
    """
    Класс для мониторинга окон и процессов.
    """
    def __init__(self):
        self.opened_windows = []
        self.processes = []
        self.wmi_client = wmi.WMI()

    def monitor_windows(self):
        """
        Отслеживает новые окна.
        """
        recent_windows = pgw.getAllTitles()
        new_windows = [win for win in recent_windows if win not in self.opened_windows]

        if new_windows:
            log_action(f"Новые окна: {new_windows}")
            self.opened_windows.extend(new_windows)

    def monitor_processes(self):
        """
        Отслеживает новые процессы.
        """
        current_processes = [p.Name for p in self.wmi_client.Win32_Process()]
        new_processes = [proc for proc in current_processes if proc not in self.processes]

        if new_processes:
            log_action(f"Новые процессы: {new_processes}")
            self.processes.extend(new_processes)

def observer_run(action_name):
    """
    Запускает мониторинг системы и отправку логов.
    """
    try:
        monitor_path = "C:\\Users\\Godless\\Desktop\\test"
        email_handler = EmailHandler()
        observer = Observer()
        event_handler = FileSystemMonitor()
        system_observer = SystemObserver()

        observer.schedule(event_handler, monitor_path, recursive=True)
        observer.start()
        log_action(f"Мониторинг файловой системы запущен по пути: {monitor_path}")
        log_action(f"Выполняем действие: {action_name}")

        while True:
            system_observer.monitor_windows()
            system_observer.monitor_processes()
            email_handler.send_log_if_updated()
            time.sleep(60)
    except Exception as e:
        log_action(f"Ошибка в observer_run: {e}", level="ERROR")
    finally:
        observer.stop()
        observer.join()
