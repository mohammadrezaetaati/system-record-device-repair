from email.policy import default
from random import choices
from django.db import models
from django.core.validators import RegexValidator

from user.models import User

class Place(models.Model):

    name = models.CharField(max_length=50)
    boss = models.CharField(max_length=30)
    storekeeper=models.ForeignKey(User,on_delete=models.PROTECT,related_name='place')


    class Meta:
        ordering=('name',)

    def __str__(self) -> str:
        return f'{self.name}'


class Branch(models.Model):

    name = models.CharField(max_length=50)
    boss = models.CharField(max_length=30)
    place = models.ForeignKey(Place,on_delete=models.PROTECT,related_name='branchs')
    phone=models.CharField(max_length=20 ,validators=[RegexValidator(regex='^[0-9-۰-۹]+$')])



    class Meta:
        ordering=('place__name',)

    def __str__(self) -> str: 
        return f'{self.name}-{self.place.name}'