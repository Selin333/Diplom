# import requests
# import plyer
# import time
# import datetime


# while True:

    
#     now = datetime.datetime.now()
#     # print(40*"-")
#     print(now.time())
#     # print(40*"-")
  
#     response = requests.get('https://m4d.nalog.gov.ru/emchd')
#     cookies = response.cookies
    
#     response.encoding = 'utf-8'
#     if response.ok:
#         response = response.text
#         print(response)
#         print(len(response))
#         if len(response) != 2405:
#                 plyer.notification.notify( message='МЧД ЗАРАБОТАЛ!!!!МЧД ЗАРАБОТАЛ!!!!МЧД ЗАРАБОТАЛ!!!!МЧД ЗАРАБОТАЛ!!!!МЧД ЗАРАБОТАЛ!!!!', app_name='ЕЕЕЕ', title='Ура')
                
#                 break
#     print(cookies)
#     break
  



# import csv
# with open("C:\\Users\\aselin\\Downloads\\admin.csv", encoding='utf-8') as r_file:
#     # Создаем объект reader, указываем символ-разделитель ","
#     file_reader = csv.reader(r_file, delimiter = ",")
#     # Счетчик для подсчета количества строк и вывода заголовков столбцов
#     count = 0
#     # Считывание данных из CSV файла
#     for row in file_reader:
#         if count == 0:
#             # Вывод строки, содержащей заголовки для столбцов
#             print(f'Файл содержит столбцы: {", ".join(row)}')
#     #     else:
#     #         # Вывод строк
#     #         print(f'    {row[0]} - {row[1]} и он родился в {row[2]} году.')
#     #     count += 1
#     # print(f'Всего в файле {count} строк.')



import os
import pythoncom
from threading import Thread
import time
import wmi

Canary_name = 'KeePassXC.exe'
Default_action = 'cover'


local_app_data = os.getenv('LOCALAPPDATA')


if local_app_data is None:
    print("Ошибка: Переменная окружения LOCALAPPDATA не найдена.")
else:
    spisok = ['123.txt','321.txt','abc.txt','3333333333333.txt']
    for i in spisok:
        test_path = os.path.join(local_app_data, 'Chromium', 'User Data', 'Default', 'Network', i)

   
        print(f"Путь: {test_path}")

    
        if os.path.exists(test_path):
        
            try:
                print(os.stat(test_path))
            except Exception as e:
                print(f"Ошибка: {e}")
        else:
            print("Файл или папка не существует.")
def start():
    def listener():
        print('start')
        pythoncom.CoInitialize()
        c = wmi.WMI()
        if c.Win32_Process(name=Canary_name):
            
            print(c.Win32_Process(name=Canary_name))
            print("Process", Canary_name, "is running")
            return True
        else:

            process_watcher = c.Win32_Process.watch_for("creation")
            
            while True:
                new_process = process_watcher()
                
                if new_process.Caption == Canary_name:
                    print('Запущен!')
                    time.sleep(5)
                    os.system('taskkill /im '+Canary_name)
                    print('Закрыт')
                    return True




    t = Thread(target=listener)
    t.daemon = True
    t.start()

    time.sleep(5)

def action():


    def cover():
        
        try:
            # os.remove("C:\\Users\\aselin\\Desktop\\testpython.txt")
            # for i in Chromium_files:
            #     os.stat(Chromium_path+i)
            pass
        except FileNotFoundError as e:
            
            print('Не все файлы найденны')
            print(e)

    

    def delete():

        pass


    #Файлы cookie и история браузеров


    Chromium_path = '%LOCALAPPDATA%\\Chromium\\User Data\\Default\\'
    Chromium_files = ['Network\\Cookies','Network\\Cookies-journal','History','History-journal','Login Data','Login Data For Account','Login Data For Account-journal','Login Data-journal']


    
    Yandex = '%LOCALAPPDATA%\\Yandex\\YandexBrowser\\User Data\\Default\\Network\\Cookies'
    # тут все нужно добавлять

    Firefox = '%UserProfile%\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\*\\cookies.sqlite'

    if Default_action == 'cover':
        print('cover')
        cover()


    elif Default_action == 'delete':
        print('delete')
        delete()
        
    else:
        print('Enter default action')

action()
status = start()





if status != True:

    print('cover')
    action()

while True:
    print('1')

    time.sleep(2);

#test123











