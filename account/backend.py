from account.models import UserModel
from django.shortcuts import get_object_or_404


class UserAuthentication():
    def authenticate(self, username=None, password=None):
        user = get_object_or_404(username=username)
        if user:
            if user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        user = get_object_or_404(pk=userid)
        if user and user.is_active:
            return user
        return None
