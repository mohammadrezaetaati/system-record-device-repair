
from enum import unique
from django.db import models

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin


# User=get_user_model()



# class Person(User):
#     ROLE_CHOES=(
#         ('administrator','Administrator'),
#         ('registrar','Registrar'),
#         ('reporter','Reporter'),
#     )
#     role=models.CharField(max_length=13,choices=ROLE_CHOES)
#     add=models.BooleanField(default=False)
#     edit=models.BooleanField(default=False)
#     delete=models.BooleanField(default=False)

#     class Meta:   
#         permissions=[
#             ('can_all_access','Can access everything'),
#             ('can_delete','Can delete anything'),
#             ('can_edit','Can edit anything'),
#             ('can_add','Can add anything'),
#             ('can_report','Can report'),
#         ]

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
        superuser.save()
        return superuser

class User(AbstractBaseUser,PermissionsMixin):
    ROLE_CHOES=(
        ('administrator','Administrator'),
        ('registrar','Registrar'),
        ('reporter','Reporter'),
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
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


