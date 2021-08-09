import datetime

import requests
from django.conf import settings
from social_core.exceptions import AuthForbidden

from users.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    response = requests.get(f'https://api.vk.com/method/users.get/',
                            params={'fields': 'bdate, sex, about, photo_max_orig',
                                    'access_token': response['access_token'], 'v': '5.92'})

    if response.status_code != 200:
        return

    data = response.json()['response'][0]

    if data.get('sex'):
        if data['sex']:
            user.userprofile.gender = UserProfile.MALE if data['sex'] == 2 else UserProfile.FEMALE

    if data.get('about'):
        user.userprofile.about = data['about']

    if data.get('bdate'):
        bdate = datetime.datetime.strptime(data['bdate'], '%d.%m.%Y')
        if datetime.datetime.now().year - bdate.year < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOauth2')

    if data.get('photo_max_orig'):
        with open(f'{settings.MEDIA_ROOT}/users_image/{user.pk}.jpg', 'wb') as avatar:
            avatar.write(requests.get(data['photo_max_orig']).content)
        user.avatar = f'users_image/{user.pk}.jpg'

    user.save()


