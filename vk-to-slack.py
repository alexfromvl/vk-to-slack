from slacker import Slacker

import vk_api

import time

slack = Slacker('Your token API Slack')

def main():
    login, password = 'login', 'pass'
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return


    vk = vk_session.get_api()

    while True: #запускаем цикл
        man_id = str(-29534144) #id группы с котороый будем брать посты и комментарии
        postidlist = vk.wall.get(owner_id=man_id, count=1, offset=0) #получаем последний пост
        a = str(postidlist['items'][0]['id']) #получаем id поста в виде цифры и записываем
        time.sleep(5) #засыпаем на 5 секунд
        ts = 10
        bts = 10
        while ts == bts: #сравниваем два числа времени комментариев, цикл выполняется до тех пор, пока цифры равны.
            response = vk.wall.getComments(owner_id=man_id, post_id=a, count=1, sort='desc', offset=0) #Получаем последний комментарий
            ts = str(response['items'][0]['date']) #запрашиваем время комментария
            time.sleep(5) #ожидание 5 секунд
            response = vk.wall.getComments(owner_id=man_id, post_id=a, count=1, sort='desc', offset=0)
            bts = str(response['items'][0]['date'])
            print('новых комментов нет ' + ts + bts) #Если новых комментариев нет выводим сообщение и время
            time.sleep(5) #если время у комментариев разное цикл прекращается
        response = vk.wall.getComments(owner_id=man_id, post_id=a, count=1, sort='desc', offset=0)  # получаем комментарий со стены
        b = response['items'][0]['text'] #вытаскиваем из него только текст
        print(b)
        slack.chat.post_message('#vk', 'Новый комментарий: ' + b) #отправляем сообщение с текстом в Slack и повторяем цикл

if __name__ == '__main__':
    main()

