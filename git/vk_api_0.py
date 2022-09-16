import vk_api


def auth_handler():
    "Функция для обработки двухфакторной авторизации"
    key = input('Введите код:')
    remember_device = True
    return key, remember_device


def captcha_handler(captcha):
    "Функция для обработки каптчи"
    key = input(f'Введите каптчу {captcha.get_url().strip()}')
    return captcha.try_again(key)


vk_session = vk_api.VkApi('+7xxxxxxxx', 'password', auth_handler=auth_handler, captcha_handler=captcha_handler)
vk_session.auth()
vk = vk_session.get_api()
print(vk_session.json())
print(vk_session.token['user_id'])
print(vk_session.token['access_token'])
response = vk.account.getAppPermissions(4096)
print(response)
