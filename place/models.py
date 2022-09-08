from django.db import models



class Place(models.Model):
    name = models.CharField(max_length=255)
    boss = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Branch(models.Model):
    name=models.CharField(max_length=100)
    place = models.ForeignKey(Place,on_delete=models.CASCADE)
    boos=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)

    def __str__(self) -> str: 
        return f'{self.name}-{self.place.name}'