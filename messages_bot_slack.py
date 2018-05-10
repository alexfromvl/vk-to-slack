# -*- coding: utf-8 -*-

import requests

# https://github.com/python273/vk_api
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType

# https://github.com/os/slacker
from slacker import Slacker
import time

#setting
DEBUG = True
slack = Slacker('Your token API Slack')
login = 'your login VK'
password = 'your pass VK'
vk_token = 'Your token API VK group'

def main():

    if DEBUG:
        print("Start work!")

    session = requests.Session()

    # Авторизация пользователя:
    """
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    """

    # Авторизация группы:
    # при передаче token вызывать vk_session.auth не нужно
    """
    vk_session = vk_api.VkApi(token='токен с доступом к сообщениям и фото')
    """
    vk_session = vk_api.VkApi(token=vk_token)

    vk = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            # Отправка в Slack чат (#vk) - должен быть заранее создан у вас в Slack
            slack.chat.post_message('#vk', 'Новое сообщение: id{}: "{}"'.format(event.user_id, event.text))
            if DEBUG:
                print('id{}: "{}"'.format(event.user_id, event.text), end=' ')

            # Ответ пользователю на сообщение в ВК.
            vk.messages.send(
                user_id=event.user_id,
                message="Мы получили ваше сообщение. В ближайшее время мы ответим вам."
            )
            if DEBUG:
                print('ok')


if __name__ == '__main__':
    main()
