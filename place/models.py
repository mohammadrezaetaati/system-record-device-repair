from email.policy import default
from random import choices
from django.db import models
from django.core.validators import RegexValidator


class Place(models.Model):
    UPDATE_CHOICE=[
        ('update','Update'),
        ('no_update','No_update'),
    ]
    name = models.CharField(max_length=50)
    boss = models.CharField(max_length=30)
    storekeeper=models.CharField(max_length=30)
    update=models.CharField(max_length=9,choices=UPDATE_CHOICE,default='no_update')

    class Meta:
        ordering=('name',)

    def __str__(self) -> str:
        return f'{self.name}-{self.update}'


class Branch(models.Model):
    UPDATE_CHOICE=[
        ('update','Update'),
        ('no_update','No_update'),
    ]
    name = models.CharField(max_length=50)
    boss = models.CharField(max_length=30)
    place = models.ForeignKey(Place,on_delete=models.PROTECT)
    phone=models.CharField(max_length=20 ,validators=[RegexValidator(regex='^[0-9-۰-۹]+$')])
    update=models.CharField(max_length=9,choices=UPDATE_CHOICE,default='no_update')


    class Meta:
        ordering=('place',)

    def __str__(self) -> str: 
        return f'{self.name}-{self.place.name}-{self.update}'