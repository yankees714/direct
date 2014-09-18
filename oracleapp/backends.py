# from django.conf import settings
from django.contrib.auth.models import User

import requests

class BowdoinAuthBackend(object):
    """
    docstring
    """

    def authenticate(self, username=None, password=None):
        login_valid = check_login(username, password)
        
        if login_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user (ignoring password field)
                user = User(username=username, password='N/A')
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def check_login(username, password):
    result = requests.post(
        "https://www.bowdoin.edu/apps/mobile/login.php",
        data={'username': username, 'password': password}
    )
    if result:
        return result.text != "0"
    else:
        return False
