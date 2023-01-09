from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

from .tasks import send_activation_code
# Create your models here

class UserManager(BaseUserManager):
    use_in_migrations = True


    def create_user(self, email, password, **kwargs):
        assert email, 'Email is required'
        
        email = self.normalize_email(email)
        user:User = self.model(email=email, **kwargs)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        send_activation_code.delay(user.email, user.activation_code)

        return user
    

    def create_superuser(self, email, password, **kwargs):
        assert email, 'Email is required'

        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        email = self.normalize_email(email)
        user:User = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = None
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=8, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def create_activation_code(self):
        from django.utils.crypto import get_random_string


        code = get_random_string(length=8, allowed_chars='qwertyuiopasdfghjklzxcvbnmQWERTYUIOASDFGHJKLZXCVBNM234567890')
        self.activation_code = code
        self.save()
