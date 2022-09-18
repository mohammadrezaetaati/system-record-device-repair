from django.db import models
from django.core.validators import RegexValidator


class Place(models.Model):
    name = models.CharField(max_length=255)
    boss = models.CharField(max_length=255)

    class Meta:
        ordering=('name',)

    def __str__(self) -> str:
        return self.name


class Branch(models.Model):
    name=models.CharField(max_length=100)
    place = models.ForeignKey(Place,on_delete=models.PROTECT)
    boss=models.CharField(max_length=100)
    phone=models.CharField(max_length=20 ,validators=[RegexValidator(regex='^[0-9-۰-۹]+$')])

    class Meta:
        ordering=('place',)

    def __str__(self) -> str: 
        return f'{self.name}-{self.place.name}'