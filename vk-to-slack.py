#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slacker import Slacker
import vk_api
import time

#setting
DEBUG = True

slack = Slacker('Your token API Slack')
login_vk = 'your login VK'
pass_vk = 'your pass VK'
group_id = '-1234567890'

def main():
    login, password = login_vk, pass_vk
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    while True: #запускаем цикл
        man_id = str(group_id) #id группы с которой будем брать посты и комментарии
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
            if DEBUG:
                print('новых комментариев нет ' + ts + bts) #Если новых комментариев нет выводим сообщение и время
            time.sleep(5) #если время у комментариев разное цикл прекращается
        response = vk.wall.getComments(owner_id=man_id, post_id=a, count=1, sort='desc', offset=0)  # получаем комментарий со стены
        b = response['items'][0]['text'] #вытаскиваем из него только текст
        if DEBUG:
            print(b)
        slack.chat.post_message('#vk', 'Новый комментарий: ' + b) #отправляем сообщение с текстом в Slack и повторяем цикл

if __name__ == '__main__':
    main()

