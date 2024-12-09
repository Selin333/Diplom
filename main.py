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

def check_canary():
    """
    Проверяет наличие канарейского процесса.
    Если процесс найден, программа завершает работу.
    """
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

if __name__ == "__main__":
    try:
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
