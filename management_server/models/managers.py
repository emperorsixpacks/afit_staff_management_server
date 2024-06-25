from tortoise.manager import Manager

class UserManager(Manager):
    def create(self, **kwargs):
        password = kwargs.pop("password", None)