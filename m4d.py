import os
import pythoncom
from threading import Thread
import time
import wmi
import watchdog
import smtplib
import pygetwindow as pgw
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


Canary_name = 'secret_prog.exe'
Default_action = 'delete'
# YEEEESSS


def start():
    def listener():
        print('start')
        pythoncom.CoInitialize()
        c = wmi.WMI()
        if c.Win32_Process(name=Canary_name):
            
            
            print(c.Win32_Process(name=Canary_name))
            print("Процесс", Canary_name, "найден. Закрытие приложения.....")
            os.system('taskkill /f /im ' + Canary_name + ' > NUL 2>&1')
            print('Закрыто')
            return True
        else:
            return False

                    




    t = Thread(target=listener)
    t.daemon = True
    t.start()

    time.sleep(5)

def action():
    local_app_data = os.getenv('LOCALAPPDATA')

    # Chromium_path = '\\Chromium\\User Data\\Default\\'
    Chromium_path = 'C:\\Users\\aselin\\Desktop\\test\\'
    # Chromium_files = ['Network\\Cookies','Network\\Cookies-journal','History','History-journal','Login Data','Login Data For Account','Login Data For Account-journal','Login Data-journal']
    Chromium_files = ['123.txt','321.txt','abc.txt','3333333333333.txt']

    Yandex_path = '%LOCALAPPDATA%\\Yandex\\YandexBrowser\\User Data\\Default\\Network\\Cookies'
    # тут все нужно добавлять

    Firefox = '%UserProfile%\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\*\\cookies.sqlite'

    
    def cover():
        
        for i in Chromium_files:
            path = Chromium_path + i
            #pat = local_app_data + Chromium_path + i       
            print(f"Путь: {path}")
            
            if os.path.exists(path):
                
                try:
                    print(os.stat(path))
                    
                except Exception as e:
                    print(f"Ошибка: {e}")
            else:
                print("Файл или папка не существует.")

    

    def delete():
        for i in Chromium_files:
            path = Chromium_path + i
            #path = local_app_data + Chromium_path + i       
            
            
            if os.path.exists(path):
                
                try:
                    os.remove(path)
                    print(f"Файл: {path} - удален")
                    
                except Exception as e:
                    print(f"Ошибка: {e}")
            else:
                print(f"{path} - Файл или папка не существует.")
            
    def system_reset():

        a = input("введите 1 для сбросв: ")
        # Команда для сброса Windows
        if a ==1:
            os.system("powershell.exe systemreset -factoryreset")

        # Запуск команд




    def notify():
    # server = 'yandex.ru'
    # user = 'notify@yandex.ru'
    # password = 'password_mail'
    
    # recipients = ['mail4studying@yandex.ru']
    # sender = 'notify@mail.ru'
    # subject = 'Кто то получил доступ к вашему комптьютеру'
    # text = 'Дата, время что произошло с файлами, лог отслеживателя'
    # html = '<html><head></head><body><p>'+text+'</p></body></html>'
    
    # filepath = "/var/log/maillog"
    # basename = os.path.basename(filepath)
    # filesize = os.path.getsize(filepath)
    
    # msg = MIMEMultipart('alternative')
    # msg['Subject'] = subject
    # msg['From'] = 'Python script <' + sender + '>'
    # msg['To'] = ', '.join(recipients)
    # msg['Reply-To'] = sender
    # msg['Return-Path'] = sender
    # msg['X-Mailer'] = 'Python/'+(python_version())
    
    # part_text = MIMEText(text, 'plain')
    # part_html = MIMEText(html, 'html')
    # part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(basename))
    # part_file.set_payload(open(filepath,"rb").read() )
    # part_file.add_header('Content-Description', basename)
    # part_file.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename, filesize))
    # encoders.encode_base64(part_file)
    
    # msg.attach(part_text)
    # msg.attach(part_html)
    # msg.attach(part_file)
    
    # mail = smtplib.SMTP_SSL(server)
    # mail.login(user, password)
    # mail.sendmail(sender, recipients, msg.as_string())
    # mail.quit()
        pass
    


    if Default_action == 'cover':
        print('cover')
        cover()
        notify()


    elif Default_action == 'delete':
        print('delete')
        delete()
        notify()
        
    else:
        print('Enter default action')


 
def observer():
    opened_Windows = []
    recent_Windows = pgw.getAllTitles()
    for i in recent_Windows:
        if i not in opened_Windows:
            opened_Windows.append(i)

    print(opened_Windows)


status = start()
print(status)





if status != True:
    
    print(Default_action)
    action()
else:
    exit()














