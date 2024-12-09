import os
from observer_notify import log_action

def action(Default_action):
    """
    Выполняет действие в зависимости от настройки Default_action:
    - delete: Удаление файлов
    """
    Chromium_path = "C:\\Users\\Godless\\Desktop\\test\\"
    Chromium_files = ["123.txt", "321.txt", "abc.txt", "3333333333333.txt"]

    def delete():
        """
        Удаляет заданные файлы.
        """
        for file in Chromium_files:
            path = os.path.join(Chromium_path, file)
            if os.path.exists(path):
                try:
                    os.remove(path)
                    log_action(f"Файл {path} успешно удалён.")
                except Exception as e:
                    log_action(f"Ошибка при удалении файла {path}: {e}", level="ERROR")
            else:
                log_action(f"Файл {path} не найден.", level="WARNING")

    if Default_action == "delete":
        log_action("Запущено удаление файлов.")
        delete()
        log_action("Удаление файлов завершено.")
    else:
        log_action(f"Действие {Default_action} не поддерживается.", level="WARNING")
