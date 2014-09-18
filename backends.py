# from django.conf import settings
from django.contrib.auth.models import User

import requests

class BowdoinAuthBackend(object):
    """
    A Django auth backend for authenticating Bowdoin users.
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
    login_url = "https://www.bowdoin.edu/apps/mobile/login.php"
    creds = {'username': username, 'password': password}
    result = requests.post(url, data=creds)

    if result:
        return result.text != "0"
    else:
        return False
