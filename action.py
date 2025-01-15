import os
import subprocess
from observer_notify import log_action
import pyautogui
import time

# Путь к SDelete (если не в PATH, укажите полный путь к исполняемому файлу)
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

def secure_delete_with_sdelete(file_path, passes=3):
    """
    Надежно удаляет файл с использованием SDelete.

    :param file_path: Путь к файлу
    :param passes: Количество перезаписей (по умолчанию 3)
    """
    if os.path.exists(file_path):
        try:
            # Запускаем SDelete с указанным количеством перезаписей
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
    Выполняет сброс ОС до заводских настроек.
    """
    try:
        subprocess.run(["systemreset", "-factoryreset"], check=True)
        log_action("Сброс ОС до заводских настроек")
        time.sleep(4)
        pyautogui.moveTo(739, 446)  # Замените на координаты кнопки
        pyautogui.click()

        # Если требуется, добавьте последующие шаги для подтверждения
        time.sleep(2)
        pyautogui.moveTo(832, 431)  # Замените на координаты следующей кнопки
        pyautogui.click()
    except subprocess.CalledProcessError as e:
        log_action(f"Ошибка при выполнении сброса ОС: {e}", level="ERROR")
    except FileNotFoundError:
        log_action("Команда systemreset не найдена. Убедитесь, что вы используете Windows 10 или выше.", level="ERROR")

def cover_file(file_path):
    """
    Создаёт ложный файл с заранее определённым содержимым.

    :param file_path: Путь к файлу для создания ложного содержимого
    """
    try:
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
    Удаляет временные файлы Windows.
    """
    try:
        temp_dir = os.getenv('TEMP')
        subprocess.run([SDELETE_PATH, "-p", "3", temp_dir], check=True)
        log_action(f"Временные файлы в {temp_dir} успешно удалены.")
    except Exception as e:
        log_action(f"Ошибка при удалении временных файлов: {e}", level="ERROR")

def delete_user_certificates():
    """
    Удаляет пользовательские сертификаты.
    """
    try:
        subprocess.run(["certutil", "-delstore", "my"], check=True)
        log_action("Пользовательские сертификаты успешно удалены.")
    except Exception as e:
        log_action(f"Ошибка при удалении пользовательских сертификатов: {e}", level="ERROR")

def clear_memory():
    """
    Очищает оперативную память с использованием RAMMap.
    """
    try:
        rammap_path = "path\\to\\rammap.exe"  # Укажите путь к RAMMap
        subprocess.run([rammap_path, "-E"], check=True)
        log_action("Оперативная память успешно очищена с помощью RAMMap.")
    except Exception as e:
        log_action(f"Ошибка при очистке оперативной памяти: {e}", level="ERROR")

def empty_recycle_bin():
    """
    Надежно очищает корзину Windows.
    """
    try:
        recycle_bin_path = "C:\\$Recycle.Bin"
        subprocess.run([SDELETE_PATH, "-p", "3", recycle_bin_path], check=True)
        log_action("Корзина успешно очищена.")
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
            cover_file(file_path)  # Создаём ложный файл на месте удалённого

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
