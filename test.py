import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import pymysql
from config import host, user_bd, password_bd,db_name

token = "vk1.a.uXfI_gAQDJjZ-FQOVafRXX7fxv4l8wmPK87hNp3YyiGy83j5300j62q773LpCv3SlJUx5Jab9RzSYf9FNKvcsVyXLtL4zc7KOQ99x0PZO6ef9CiHfEcYM6v89sOVTCAlvdQJwqh_BPXIgrU4g5w0CFH1ldq6yzEz9KfI1ZXCfv0Q-eZNh4fjHth_Ql55P58C_jdXTyxLPssgevHQB1FiJw"
session = vk_api.VkApi(token=token)

try:
    connetion = pymysql.connect(
        host=host,
        user = user_bd,
        password=password_bd,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Connect true")
except Exception as ex:
    print(ex)



class User():
    def __init__(self, sender, mode, point, rank, place):
        self.id = sender
        self.mode = mode
        self.point = point
        self.rank = rank
        self.place = place


class Admin():
    def __init__(self, sender, password,mode):
        self.id = sender
        #self.mode = mode
        self.password = password
        self.mode = mode
        

# функция вывода сообщений


def write_message(sender, message, keyboard=None):
    post = {'user_id': sender,
            'message': message,
            'random_id': get_random_id()}
    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()
    else:
        post = post
    session.method('messages.send', post)

# функция вывода стартового меню


def write_start_meny(sender, message, keyboard):

    keyboard.add_button("Задания", VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Мои отчивки", VkKeyboardColor.PRIMARY)
    keyboard.add_button("Моё звание", VkKeyboardColor.PRIMARY)
    keyboard.add_button("Рейтинг", VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Баллы", VkKeyboardColor.NEGATIVE)

    write_message(sender, message, keyboard)


def write_back(sender, message, keyboard):

    keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
    write_message(sender, message, keyboard)


def write_admin_meny(sender,message,keyboard):
    keyboard.add_button("выйти", VkKeyboardColor.NEGATIVE)
    write_message(sender,message,keyboard)


users = []
admins = []

for event in VkLongPoll(session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text_message = str(event.text).lower()
        keyboard = VkKeyboard()
        # text_message = text_message.lower()
        sender = event.user_id

        if text_message == "начать":
            try:
                with connetion.cursor() as cursor:
                    fetch_id = cursor.execute(f"SELECT id from user where id = {sender} ")
            except Exception as ex:
                print(ex)
            if fetch_id == 1:
                    try:
                        write_start_meny(sender, "Здорова папаня", keyboard)
                        insert_query = (f"update user set user_mode = 'start' where id = {sender}")
                        with connetion.cursor() as cursor:
                            user_mode = cursor.execute(insert_query)
                            connetion.commit()
                            for user in users:
                                users.append(User(sender,user_mode,0,0,0))
                    except Exception as ex:
                        print(ex)
            elif fetch_id == 0:
                write_start_meny(sender, "Выберите действиее:", keyboard)
                for user in users:
                    try:
                            with connetion.cursor() as cursor:
                                insert_query = f"INSERT INTO `user` (id,point,rank,place,user_mode) VALUES ({sender},'0','0','0','start');"
                                cursor.execute(insert_query)
                                connetion.commit()
                    except Exception as ex:
                        print(ex)
                    users.append(User(sender,"start",0,0,0))


        # if text_message == "/admin":
        #     try:
        #         with connetion.cursor() as cursor:
        #             fetch_id2 = cursor.execute(f"SELECT id from admins where id = {sender} ")
        #             print(fetch_id)
        #     except Exception as ex:
        #         print("EROR 1")
        #         print(ex)
        #     if fetch_id2 == 1:
        #             try:
        #                 write_start_meny(sender, "Вы пытаетесь войти как админ, введите пароль:", keyboard)
        #                 user_mode = (f"update user set user_mode = 'admin_start' where id = {sender}")
        #                 with connetion.cursor() as cursor:
        #                     cursor.execute(user_mode)
        #                     connetion.commit()
        #             except Exception as ex:
        #                 print(ex)
        #     elif fetch_id == 0:
        #         write_message(sender,"Вы не являетесь админом!")
                

        #for user in users:
            if user.id == sender: #если юзер уже был зарегестрирован
                # try:
                #     with connetion.cursor as cursor:
                #         user_mode = (f"select user_mode from user where id = {sender}")
                #     print(user_mode)
                # except Exception as ex:
                #     print(ex)
                if user.mode == "start":
                    if text_message == "баллы":
                        # try:
                        #     with connetion.cursor as cursor:
                        #         point = (f"select point from user where id = {sender}")
                        #         print(user_mode)
                        # except Exception as ex:
                        #     print(ex)
                        write_start_meny(sender, f"Ваши баллы:{user.point}", keyboard)
                    if text_message == "задания":
                        #write_message(sender, "Тут гуляет ветер...")
                        write_back(sender,"Выберите задания",keyboard)
                        user_mode = "zadania"
                    if text_message == "мои отчивки":
                        write_back(sender, "Ваши отчивки",keyboard)
                        user_mode = "achievement"
                    if text_message == "моё звание":
                        write_back(sender, f"Ваше звание:{user.rank}",keyboard)
                        user_mode = "rank"
                    if text_message == "рейтинг":
                        write_back(sender, f"Ваше место:{user.place}",keyboard)
                        user_mode = "rating"
                    if text_message =="/admin":
                        write_message(sender,"тут будет вход под админа")
                    if text_message =="/adminadd":
                        write_message(sender, "Тут будет добавление админа")


                    if user_mode == "zadania":
                        if text_message == "назад":
                            write_start_meny(sender, "Выберите действие", keyboard)
                            user.mode = "start"
                        
                    if user_mode == "achievement":
                        if text_message == "назад":
                            write_start_meny(sender, "Выберите действие", keyboard)
                            user.mode = "start"

                    if user_mode == "rank":
                        if text_message == "назад":
                            write_start_meny(sender, "Выберите действие", keyboard)
                            user.mode = "start"
                    
                    if user_mode == "rating":
                        if text_message == "назад":
                            write_start_meny(sender, "Выберите действие", keyboard)
                            user.mode = "start"

                    
                            
                    
                    

                
            