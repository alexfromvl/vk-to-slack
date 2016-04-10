from slacker import Slacker #импорт модуля для работы с API Slack

import vk_api #импорт модуля для работы с API Вконтакте

slack = Slacker('<API TOKEN>') #записываем токен от Slack bot

def main():
    
    login, password = 'email@email.ru', 'pass' #авторизуемся в ВК
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    
    response = vk.wall.getComments(owner_id=-1, post_id=1, count=1, extended=1)  # Используем метод wall.getComments для получения комментариев
    print(response ['items'][0]['text']) #Получаем текст комментария со стены

    slack.chat.post_message('#vk', 'Комментарий: ' + response ['items'][0]['text']) # Отправляем полученый комментарий в чат

if __name__ == '__main__':
    main()
