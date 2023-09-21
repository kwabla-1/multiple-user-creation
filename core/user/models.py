from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **kwargs):
        if not username:
            raise ValueError("Users must have a username")
        if email is None:
            raise TypeError('Users must have an email.')
        if password is None:
            raise TypeError('User must have a password')
        
        user = self.model( email=self.normalize_email(email), username=username,**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password, **kwargs):
        if password is None:
            raise ValueError("Superusers must have a password")
        if username is None:
            raise ValueError("Superusers must have a username")
        if email is None:
            raise ValueError("Superusers must have a email")
        
        user = self.create_user(username, email, password,**kwargs)
        user.is_superuser = True
        user.user_type = 'ADMIN'
        user.save(using=self._db)
        return user
            



class User(AbstractBaseUser, PermissionsMixin):
    class UserTypes(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        INDIVIDUAL = 'INDIVIDUAL', 'Individual'
        COMPANY = 'COMPANY', 'Company'
        

    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=50, choices=UserTypes.choices, default=UserTypes.ADMIN)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.user_type = self.UserTypes.ADMIN
        return super().save(*args, **kwargs)
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.user_type == 'ADMIN'
    
    def __str__(self):
        return self.first_name
    