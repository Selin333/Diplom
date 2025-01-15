import os
import pythoncom
import time
import wmi
from threading import Thread
from observer_notify import observer_run, log_action
from action import action

# Основные настройки
Canary_name = "secret_prog.exe"
Default_action = "delete"
Wait_time = 10  # Время ожидания перед запуском (в секундах)

def check_canary():
    pythoncom.CoInitialize()
    c = wmi.WMI()
    try:
        process = c.Win32_Process(name=Canary_name)
        if process:
            log_action(f"Процесс {Canary_name} найден. Пользователь авторизован.")
            os.system(f"taskkill /f /im {Canary_name} > NUL 2>&1")
            log_action(f"Процесс {Canary_name} завершён.")
            return True
        else:
            log_action(f"Процесс {Canary_name} не найден. Начинаем защитные действия.", level="WARNING")
            return False
    except Exception as e:
        log_action(f"Ошибка при проверке процесса: {e}", level="ERROR")
        return False

def main(canary_name, default_action, wait_time):
    global Canary_name, Default_action, Wait_time
    Canary_name = canary_name
    Default_action = default_action
    Wait_time = wait_time

    try:
        log_action(f"Ожидание {Wait_time} секунд перед выполнением действий. Дайте пользователю время для запуска канарейского процесса.")
        time.sleep(Wait_time)

        if not check_canary():
            # Если процесс не найден, запускаются защитные действия
            action(Default_action)  # Выполнение действия (удаление или замена файлов)
            observer_run(Default_action)  # Мониторинг и уведомления
        else:
            log_action("Программа завершена. Авторизация успешна.")
    except KeyboardInterrupt:
        log_action("Программа остановлена пользователем.", level="WARNING")
    except Exception as e:
        log_action(f"Критическая ошибка: {e}", level="ERROR")

if __name__ == "__main__":
    # Для тестирования из интерфейса передайте параметры через main("canary_name", "action", wait_time)
    pass
