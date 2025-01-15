import os
import subprocess
from observer_notify import log_action
import pyautogui
import time
import ctypes
import threading


SDELETE_PATH = "sdelete64.exe"

# Папки и файлы для защиты по браузерам
BROWSERS_DATA = {
    "Chromium": {
        "path": "%LOCALAPPDATA%\\Chromium\\User Data\\Default\\",
        "files": [
            "Network\\Cookies",
            "Network\\Cookies-journal",
            "History",
            "History-journal",
            "Login Data",
            "Login Data For Account",
            "Login Data For Account-journal",
            "Login Data-journal"
        ]
    },
    "Chrome": {
        "path": "%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\",
        "files": [
            "Network\\Cookies",
            "Network\\Cookies-journal",
            "History",
            "History-journal",
            "Login Data",
            "Login Data For Account",
            "Login Data For Account-journal",
            "Login Data-journal"
        ]
    },
    "Edge": {
        "path": "%LOCALAPPDATA%\\Microsoft\\Edge\\User Data\\Default\\",
        "files": [
            "Network\\Cookies",
            "Network\\Cookies-journal",
            "History",
            "History-journal",
            "Login Data",
            "Login Data For Account",
            "Login Data For Account-journal",
            "Login Data-journal"
        ]
    },
    "Firefox": {
        "path": "%APPDATA%\\Mozilla\\Firefox\\Profiles\\",
        "files": [
            "cookies.sqlite",
            "cookies.sqlite-wal",
            "cookies.sqlite-shm",
            "places.sqlite",
            "places.sqlite-wal",
            "places.sqlite-shm",
            "logins.json",
            "key4.db"
        ]
    },
    "Opera": {
        "path": "%APPDATA%\\Opera Software\\Opera Stable\\",
        "files": [
            "Cookies",
            "Cookies-journal",
            "History",
            "History-journal",
            "Login Data",
            "Login Data-journal"
        ]
    },
    "Yandex": {
        "path": "%LOCALAPPDATA%\\Yandex\\YandexBrowser\\User Data\\Default\\",
        "files": [
            "Network\\Cookies",
            "Network\\Cookies-journal",
            "History",
            "History-journal",
            "Login Data",
            "Login Data For Account",
            "Login Data For Account-journal",
            "Login Data-journal"
        ]
    }
}


def block_input(duration):
    """
    Полностью блокирует ввод с клавиатуры и мыши на указанное время.

    :param duration: Время блокировки в секундах
    """
    try:
        ctypes.windll.user32.BlockInput(True)  # Блокирует ввод
        time.sleep(duration)  # Ожидает завершения времени
    finally:
        ctypes.windll.user32.BlockInput(False)  # Гарантированно разблокирует ввод


def secure_delete_with_sdelete(file_path, passes=3):
    """
    Надежно удаляет файл с использованием SDelete.

    :param file_path: Путь к файлу
    :param passes: Количество перезаписей (по умолчанию 3)
    """
    if os.path.exists(file_path):
        try:

            subprocess.run([SDELETE_PATH, "-p", str(passes), file_path], check=True)
            log_action(f"Файл {file_path} успешно удалён с помощью SDelete.")
        except subprocess.CalledProcessError as e:
            log_action(f"Ошибка при выполнении SDelete: {e}", level="ERROR")
        except FileNotFoundError:
            log_action("SDelete не найден. Убедитесь, что он доступен по указанному пути.", level="ERROR")
    else:
        log_action(f"Файл {file_path} не найден.", level="WARNING")


def reset_system():
    """
    Выполняет сброс ОС до заводских настроек с полной блокировкой ввода.
    """
    try:
        log_action("Сброс ОС до заводских настроек начат")

        # Блокируем ввод
        block_input_duration = 20
        block_thread = threading.Thread(target=block_input, args=(block_input_duration,))
        block_thread.start()

        # Запускаем команду сброса
        os.system("powershell.exe systemreset -factoryreset")
        time.sleep(4)

        # Эмуляция нажатия кнопок
        pyautogui.moveTo(739, 446)  # Замените на координаты кнопки "Далее"
        # pyautogui.click()
        time.sleep(2)
        pyautogui.moveTo(832, 431)  # Замените на координаты кнопки подтверждения
        # pyautogui.click()

        log_action("Сброс ОС подтверждён")
    except Exception as e:
        log_action(f"Ошибка при выполнении сброса ОС: {e}", level="ERROR")
    finally:
        ctypes.windll.user32.BlockInput(False)  # Разблокируем ввод


def cover_file(file_path):
    """
    Создаёт ложный файл с заранее определённым содержимым.

    :param file_path: Путь к файлу для создания ложного содержимого
    """
    try:
        secure_delete_with_sdelete(file_path)
        file_extension = os.path.splitext(file_path)[1].lower()
        fake_content = ""

        if file_extension == ".txt":
            fake_content = "Я помню чудное мгновенье:\nПередо мной явилась ты,\nКак мимолётное виденье,\nКак гений чистой красоты."
        elif file_extension == ".docx":
            fake_content = "Документ создан для тестирования."
        elif file_extension == ".db":
            fake_content = "Фальшивая база данных."
        else:
            fake_content = "Этот файл создан для защиты данных."

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(fake_content)

        log_action(f"Ложный файл создан: {file_path}")
    except Exception as e:
        log_action(f"Ошибка при создании ложного файла {file_path}: {e}", level="ERROR")


def delete_temp_files():
    """
    Удаляет все файлы и папки внутри %TEMP% с использованием SDelete, оставляя саму папку.
    """
    temp_dir = os.getenv('TEMP')
    if not temp_dir:
        log_action("Не удалось получить путь к TEMP.", level="ERROR")
        return

    try:

        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    subprocess.run([SDELETE_PATH, "-p", "3", file_path], check=True)
                    log_action(f"Файл {file_path} успешно удалён.")
                except Exception as e:
                    log_action(f"Ошибка при удалении файла {file_path}: {e}", level="ERROR")

            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    subprocess.run([SDELETE_PATH, "-p", "3", dir_path], check=True)
                    log_action(f"Папка {dir_path} успешно очищена.")
                except Exception as e:
                    log_action(f"Ошибка при очистке папки {dir_path}: {e}", level="ERROR")

    except Exception as e:
        log_action(f"Ошибка при удалении временных файлов: {e}", level="ERROR")


def delete_user_certificates():
    """
    Удаляет все сертификаты из хранилища "Личное" текущего пользователя.
    """
    try:
        # Получаем список сертификатов из хранилища "Личное" текущего пользователя
        result = subprocess.run(
            ["certutil", "-store", "-user", "My"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout

        # Ищем строки с серийными номерами сертификатов
        serial_numbers = []
        for line in output.splitlines():
            if "Серийный номер:" in line:
                serial_number = line.split(":")[1].strip()
                serial_numbers.append(serial_number)

        # Удаляем каждый сертификат по серийному номеру
        if serial_numbers:
            for serial in serial_numbers:
                try:
                    subprocess.run(
                        ["certutil", "-user", "-delstore", "My", serial],
                        check=True
                    )
                    log_action(f"Сертификат с серийным номером {serial} успешно удалён.")
                except subprocess.CalledProcessError as e:
                    log_action(f"Ошибка при удалении сертификата с серийным номером {serial}: {e}", level="ERROR")
        else:
            log_action("В хранилище 'Личное' текущего пользователя нет сертификатов для удаления.")
    except Exception as e:
        log_action(f"Ошибка при работе с хранилищем 'Личное': {e}", level="ERROR")


def clear_memory():
    """
    Очищает оперативную память с использованием RAMMap.
    """
    try:
        rammap_path = "RAMMap64.exe"  # Укажите путь к RAMMap
        subprocess.run([rammap_path, "-Et"], check=True)
        log_action("Оперативная память успешно очищена с помощью RAMMap.")
    except Exception as e:
        log_action(f"Ошибка при очистке оперативной памяти: {e}", level="ERROR")


def empty_recycle_bin():
    """
    Надёжно очищает корзину Windows с использованием SDelete.
    """
    recycle_bin_path = "C:\\$Recycle.Bin"
    if not os.path.exists(recycle_bin_path):
        log_action("Папка корзины не найдена.", level="ERROR")
        return

    try:

        for root, dirs, files in os.walk(recycle_bin_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    subprocess.run([SDELETE_PATH, "-p", "3", file_path], check=True)
                    log_action(f"Файл {file_path} успешно удалён из корзины.")
                except Exception as e:
                    log_action(f"Ошибка при удалении файла {file_path}: {e}", level="ERROR")

            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    subprocess.run([SDELETE_PATH, "-p", "3", dir_path], check=True)
                    log_action(f"Папка {dir_path} успешно очищена из корзины.")
                except Exception as e:
                    log_action(f"Ошибка при очистке папки {dir_path}: {e}", level="ERROR")

        log_action("Корзина успешно очищена с использованием SDelete.")
    except Exception as e:
        log_action(f"Ошибка при очистке корзины: {e}", level="ERROR")


def delete():
    """
    Удаляет заданные файлы с использованием SDelete для всех браузеров.
    """
    for browser, data in BROWSERS_DATA.items():
        browser_path = os.path.expandvars(data["path"])
        for file in data["files"]:
            file_path = os.path.join(browser_path, file)
            secure_delete_with_sdelete(file_path)



def action(Default_action):
    """
    Выполняет действие в зависимости от настройки Default_action:
    - delete: Удаление файлов
    - reset: Сброс ОС до заводских настроек
    - clear_temp: Удаление временных файлов
    - clear_certs: Удаление пользовательских сертификатов
    - clear_memory: Очистка оперативной памяти
    - empty_bin: Очистка корзины Windows
    """
    if Default_action == "delete":
        log_action("Запущено удаление файлов.")
        delete()
        log_action("Удаление файлов завершено.")
    elif Default_action == "reset":
        log_action("Запущен сброс ОС до заводских настроек.")
        reset_system()
    elif Default_action == "clear_temp":
        log_action("Запущено удаление временных файлов.")
        delete_temp_files()
    elif Default_action == "clear_certs":
        log_action("Запущено удаление пользовательских сертификатов.")
        delete_user_certificates()
    elif Default_action == "clear_memory":
        log_action("Запущена очистка оперативной памяти.")
        clear_memory()
    elif Default_action == "empty_bin":
        log_action("Запущена очистка корзины Windows.")
        empty_recycle_bin()
    else:
        log_action(f"Действие {Default_action} не поддерживается.", level="WARNING")


# cover_file('C:\\Users\\Diplom\\Documents\\test.txt')
# delete_user_certificates()
# clear_memory()
#empty_recycle_bin()