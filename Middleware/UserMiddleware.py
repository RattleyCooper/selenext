from Middleware import Middleware


class UserMiddleware(Middleware):

    def set_created_at(self, value):
        return value

    def get_created_at(self, value):
        return value

    def set_email(self, value):
        return value

    def get_email(self, value):
        return value

    def set_password(self, value):
        return value

    def get_password(self, value):
        return value

    def set_username(self, value):
        return value + '_testies'

    def get_username(self, value):
        return value.replace('_testies', '')

