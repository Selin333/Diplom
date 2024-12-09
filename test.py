import imaplib

IMAP_SERVER = 'imap.yandex.ru'
EMAIL_USER = 'mail4studying@yandex.ru'  # Ваш адрес
EMAIL_PASSWORD = 'udizppjkqpkpjlzk'  # Пароль приложения

try:
    with imaplib.IMAP4_SSL(IMAP_SERVER) as mail:
        mail.login(EMAIL_USER, EMAIL_PASSWORD)
        print("Успешный вход!")
except Exception as e:
    print(f"Ошибка: {e}")
