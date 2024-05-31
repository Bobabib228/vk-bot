import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import pymysql
from config import host, user_bd, password_bd, db_name
from text_hello import hello, message_start_info,message_zadanie1

token = "vk1.a.uXfI_gAQDJjZ-FQOVafRXX7fxv4l8wmPK87hNp3YyiGy83j5300j62q773LpCv3SlJUx5Jab9RzSYf9FNKvcsVyXLtL4zc7KOQ99x0PZO6ef9CiHfEcYM6v89sOVTCAlvdQJwqh_BPXIgrU4g5w0CFH1ldq6yzEz9KfI1ZXCfv0Q-eZNh4fjHth_Ql55P58C_jdXTyxLPssgevHQB1FiJw"
session = vk_api.VkApi(token=token)

#connect с БД
try:
    connetion = pymysql.connect(
        host=host,
        user=user_bd,
        password=password_bd,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Connect true")
except Exception as ex:
    print(ex)


class User():
    def __init__(self, sender, mode, point, rank, place,check_quest):
        self.id = sender
        self.mode = mode
        self.point = point
        self.rank = rank
        self.place = place
        self.check_quest = check_quest


class Admin():
    def __init__(self, sender, password, mode):
        self.id = sender
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

# Функции вывода клавиатур
def write_start_meny(sender, message, keyboard):
    keyboard.add_button("Старт", VkKeyboardColor.POSITIVE)
    write_message(sender, message, keyboard)


def write_back(sender, message, keyboard):

    keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
    write_message(sender, message, keyboard)


def write_prod_meny(sender, message, keyboard):
    keyboard.add_button("Продолжить", VkKeyboardColor.POSITIVE)
    write_message(sender, message, keyboard)


def write_start_infobtn(sender, message,keyboard):
    keyboard.add_button("Получить задание", VkKeyboardColor.POSITIVE)
    write_message(sender,message,keyboard)


def write_donne(sender,message,keyboard):
    keyboard.add_button("Готов", VkKeyboardColor.POSITIVE)
    write_message(sender,message,keyboard)


def write_admin(sender, message, keyboard):
    keyboard.add_button("Просмотр статистики", VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("Выполнение задания", VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("Изменить статистику юзера", VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("Создать задание", VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
    write_message(sender,message,keyboard)

def write_change_keyboard(sender,message,keyboard):
    keyboard.add_button("Изменить уровень", VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("Изменить количество баллов", VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
    write_message(sender,message,keyboard)


def write_user_meny(sender, message, keyboard):
    keyboard.add_button("Получить задание", VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Моя статистика", VkKeyboardColor.NEGATIVE)
    write_message(sender,message,keyboard)



# Функция получения данных пользователя из БД
def select_user():
    try:
        with connetion.cursor() as cursor:
            insert_query = f"select * from user where id = {sender}"
            cursor.execute(insert_query)
            select = cursor.fetchall()
            user_point = select[0]["point"]
            user_rank = select[0]["rank"]
            user_place = select[0]["place"]
            user_mode = select[0]['user_mode']
            check_quest = select[0]['check_quest']
    except Exception as ex:
        print(ex)
    return user_point, user_rank, user_place, user_mode, check_quest


def creating_record(tabl, column, meaning): #функция добавления данных в столбец бд
    try:
        with connetion.cursor() as cursor:
            cursor.execute(f"insert into {tabl} ({column}) values ({meaning})")     
    except Exception as ex:
        print(ex)


def creating_quest(name, text, level, scores, result, priority): #функция создания записи о квесте в бд
    try:
        with connetion.cursor() as cursor:
            cursor.execute(f"insert into quest (name, text, result, level, priority, scores) values ('{name}','{text}','{result}','{level}','{priority}','{scores}')")
    except Exception as ex:
        print(ex)

#вариативное получение данных пользователя из БД
def select_user_variable(id):
    try:
        with connetion.cursor() as cursor:
            insert_query = f"select * from user where id = {id}"
            cursor.execute(insert_query)
            select = cursor.fetchall()
            user_point = select[0]["point"]
            user_rank = select[0]["rank"]
            user_place = select[0]["place"]
            user_mode = select[0]['user_mode']
            check_quest = select[0]['check_quest']
    except Exception as ex:
        print(ex)
    return user_point, user_rank, user_place, user_mode, check_quest


def select_admin():
    try:
        with connetion.cursor() as cursor:
            insert_query = f"select * from admins where id = {sender}"
            cursor.execute(insert_query)
            select = cursor.fetchall()
            admin_nom = select[0]["Nom"]
            admin_password = select[0]["password"]
    except Exception as ex:
        print(ex)
    return admin_nom, admin_password


def update_mode(mode):
    try:
        with connetion.cursor() as cursor:
            cursor.execute((f"update user set user_mode = '{mode}' where id = {sender}"))
            connetion.commit()
    except Exception as ex:
        print(ex)


def convert(user_point, user_rank, user_place, user_mode,check_quest):
    user.point = user_point
    user.mode = user_mode
    user.rank = user_rank
    user.place = user_place
    user.check_quest = check_quest


# просмотр статистики пользователя по id
def browse_user(id):
    select = select_user_variable(id)
    user_name = session.method("users.get", {"user_ids": id}) 
    fullname = user_name[0]['first_name'] +  ' ' + user_name[0]['last_name'] # Полное имя пользователя
    write_message(sender,f"Данные пользователя:\n\
                            Фио: {fullname}\n\
                            Баллы:{select[0]}\n\
                            Уровень:{select[1]}")
    

def update_point(point):
    try:
        insert_query = f"update user set point = '{point}' where id = {sender}"
        with connetion.cursor() as cursor:
            cursor.execute(insert_query)
            connetion.commit()
    except Exception as ex:
        print(ex)


def update_check_quest(check):
    try:
        with connetion.cursor() as cursor:
            cursor.execute(f"update user set check_quest = '{check}' where id = {sender}")
    except Exception as ex:
        print(ex)


def quest_search():
    try:
        with connetion.cursor() as cursor:
            cursor.execute(f"select * from quest where level = '{user.rank}'")
            select = cursor.fetchall()
            id_quest = select[0]["id"]
            level_quest = select[0]["level"]
            priority_quest = select[0]["priority"]
    except Exception as ex:
        print(ex)
    return id_quest, level_quest, priority_quest


users = []
admins = []

for event in VkLongPoll(session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text_message = str(event.text).lower()
        keyboard = VkKeyboard()
        sender = event.user_id

        
        if text_message == 'начать':
            try:
                with connetion.cursor() as cursor:
                    fetch_id = cursor.execute(f"SELECT id from user where id = {sender} ")
                    print(fetch_id)
            except Exception as ex:
                print(ex)

            if fetch_id == 1:
                write_start_meny(sender,hello, keyboard)
                select = select_user()
                print(users)
                if len(users) == 0: #проверка на случай если в БД есть запись о пользователе но в массиве его нет
                    users.append(User(sender,select[3],select[0],select[1],select[2],select[4]))
                else:#проверка, существует ли запись если массив не пустой
                    for user in users:
                        if user.id == sender:
                            break
                        else:
                            users.append(User(sender,select[3],select[0],select[1],select[2],select[4]))

                            break
                update_mode('start')

            elif fetch_id == 0:
                write_start_meny(sender, hello, keyboard)
                users.append(User(sender, "start", 0, 0, 0, 0))
                try:
                    with connetion.cursor() as cursor:
                        insert_query = f"INSERT INTO `user` (id,point,rank,place,user_mode, check_quest) VALUES ({ sender},'0','0','0','start','0');"
                        cursor.execute(insert_query)
                        connetion.commit()
                except Exception as ex:
                    print(ex)

        else:
            select = select_user()
            print(users)
            if len(users) == 0: #проверка на случай если в БД есть запись о пользователе но в массиве его нет
                users.append(User(sender,select[3],select[0],select[1],select[2],select[4]))
            else:#проверка, существует ли запись если массив не пустой
                for user in users:
                    if user.id == sender:
                        break
                    else:
                        users.append(User(sender,select[3],select[0],select[1],select[2],select[4]))
                        break

            for user in users:
                select = select_user()
                convert(select[0],select[1],select[2],select[3],select[4])

                match user.mode:
                    case "start":
                        if text_message == "старт":
                            write_prod_meny(sender,message_start_info,keyboard)


                        elif text_message == "продолжить":
                            write_start_infobtn(sender, f"Твой текущий уровень: {user.rank}\n\
                                                Баллы {user.point} ", keyboard)
                        
                        elif text_message == "получить задание":
                            write_donne(sender, message_zadanie1,keyboard)
                            update_check_quest(1)
                            

                        elif text_message == "готов":
                            write_message(sender,"Молодец! пройди тест по ссылке и пришли сюда скрин результата")#тут добавить парсинг картинки
                            user.point =int(user.point)+50
                            update_point(user.point)

                        elif text_message == "отправить":
                            user.point =int(user.point)+50
                            update_point(user.point)
                            write_user_meny(sender,"Молодец! Держи 50 баллов! Выбери действие:",keyboard)
                            update_mode("user_meny")

                        elif text_message == "/admin":
                                write_message(sender, "Введите пароль:")
                                update_mode('admin_reg')

                    case "user_meny":
                        if text_message == "получить задание":
                            print("a")
                            update_mode("start_quest")
                        elif text_message == "моя статистика":
                            update_mode("stat_chek")

                    case "start_quest":
                        select = select_user()
                        convert(select[0],select[1],select[2],select[3],select[4])
                        quest_search()
                        print("d")
                        # if user.check_quest == 0:


                    case "admin_reg":
                        select = select_admin()
                        password = select[1]
                        write_admin(sender, "Hello", keyboard)
                        if text_message == password:
                            try:
                                insert_query = (f"update user set user_mode = 'admins' where id = {sender}")
                                with connetion.cursor() as cursor:
                                    cursor.execute(insert_query)
                                    connetion.commit()
                            except Exception as ex:
                                print(ex)

                    case "admins":
                        if text_message == "просмотр статистики":
                            write_message(sender, "Введите id")
                            update_mode('admin_browse')

                        elif text_message == "изменить статистику юзера":
                            write_message(sender, "Введите id")
                            update_mode('admin_change')
                        
                        elif text_message == "создать задание":
                            print("1")
                            write_message(sender,"Введите название задания")
                            update_mode('creating_name')

                    case "creating_name":
                        name = text_message
                        print(name)
                        write_message(sender, "Введите текст задания")
                        update_mode("creating_text")

                    case "creating_text":
                        text = text_message
                        print(text)
                        write_message(sender, "Введите, для какого уровня это задание")
                        update_mode("creating_rank")

                    case "creating_rank":
                        level = text_message
                        write_message(sender,"Введите приоритет задания от 0 до 10")
                        update_mode("creating_priority")

                    case "creating_priority":
                        priority = int(text_message)
                        write_message(sender, "Введите сколько баллов получит пользователь за выполнение задания")
                        update_mode("creating_scores")

                    case "creating_scores":
                        scores = int(text_message)
                        write_message(sender, "Введите, какой ответ даст пользователь на задание (картинка или текст)")
                        update_mode("end_creating")

                    case "end_creating":
                        result = text_message
                        creating_quest(name, text, level, scores, result, priority)
                        write_message(sender,"Задание добавлено")
                        update_mode("admins")

                    case "admin_change":
                        browse_user(text_message)
                        change_id = text_message
                        update_mode('change_keyboard')
                        write_change_keyboard(sender,"Выберите что хотите изменить:", keyboard)
                        update_mode('change')

                    case "change":
                        if text_message == "изменить уровень":
                            write_message(sender,"Введите название уровня на который хотите заменить:")
                            update_mode("change_rank")
                        elif text_message == "назад":
                            update_mode('admins')
                        elif text_message == 'изменить количество баллов':
                            write_message(sender,"Введите количество баллов:")
                            update_mode('change_point')

                    case "change_rank":
                        try:
                            insert_query = f"update user set rank = '{text_message}' where id = {change_id}"
                            with connetion.cursor() as cursor:
                                cursor.execute(insert_query)
                                connetion.commit()
                        except Exception as ex:
                            print(ex)
                        write_message(sender,"Уровень успешно изменён")
                        write_admin(sender, "Hello", keyboard)
                        update_mode('admins')
                        
                    case "change_point":
                        try:
                            insert_query = f"update user set point = '{text_message}' where id = {change_id}"
                            with connetion.cursor() as cursor:
                                cursor.execute(insert_query)
                                connetion.commit()
                        except Exception as ex:
                            print(ex)
                        write_message(sender,"Количество баллов изменено")
                        write_admin(sender, "Hello", keyboard)
                        update_mode('admins')

                    case "admin_browse":
                        browse_user(text_message)
                        update_mode('admins')

                    # case "prod":
                    #     write_admin(sender, "Hello", keyboard)
