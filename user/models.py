from email.policy import default
from django.db import models

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self,username,password=None,**extra_fields):
        if not username:   
            raise ValueError('The username must be set')
        user=self.model(username=username,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,username,password=None,**extra_fields):
        if not username:
            raise ValueError('The username must be set')
        superuser=self.model(username=username,**extra_fields)
        superuser.role='administrator'
        superuser.set_password(password)
        superuser.is_staff=True
        superuser.is_superuser=True
        superuser.add=True
        superuser.delete=True
        superuser.edit=True
        superuser.change_status=True
        superuser.save()
        return superuser

class User(AbstractBaseUser,PermissionsMixin):

    ROLE_CHOES=(
        ('administrator','Administrator'),
        ('storekeeper','Storekeeper'),
        ('registrar','Registrar'),
        ('reporter','Reporter'),
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_first_login = models.BooleanField(default=True)
    username=models.CharField(max_length=8,unique=True)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    role=models.CharField(max_length=13,choices=ROLE_CHOES)
    add=models.BooleanField(default=False)
    edit=models.BooleanField(default=False)
    delete=models.BooleanField(default=False)
    change_status=models.BooleanField(default=False)
    USERNAME_FIELD='username'
    object=UserManager()

    def __str__(self) -> str:
        return self.username
        
    class Meta:
        ordering=('first_name','last_name',)


