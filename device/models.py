from datetime import datetime
from email.policy import default
from unicodedata import category


from django.db import models
from django.conf import settings


import device.functions
from place.models import Branch,Place








class Category(models.Model):
    name=models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name

class BrandCategory(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    

    def __str__(self) -> str:
        return f'{self.name}-{self.category.name}'

class Part(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    brand=models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f'{self.name}-{self.brand}'
        
class NumberPart(models.Model):
    number=models.SmallIntegerField(default=1)
    part=models.ForeignKey(Part,on_delete=models.PROTECT,null=True,blank=True)

    # def __str__(self) -> str:
        # return 


class Input(models.Model):

    STATUS_CHOICES = [
        ("unrepairable", "غیرقابل تعمیر"),
        ('finished','تحویل داده شده'),
        ("provide", "آماده به تحویل"),
        ("repair_city", "تعمیردرشهر"),
        ("ngoing", "دردست اقدام"), 
    ]

    work_order_number = models.CharField(max_length=30)
    serial = models.CharField(max_length=50)
    category=models.ForeignKey(Category,on_delete=models.PROTECT)
    brand_category=models.ForeignKey(BrandCategory,on_delete=models.PROTECT)
    place = models.ForeignKey(Place,on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch,on_delete=models.PROTECT)
    entry_date = models.CharField(max_length=20, editable=False)
    exit_date = models.CharField(max_length=20, editable=False,default='-')
    provide_date = models.CharField(max_length=20, editable=False)
    delivery = models.CharField(max_length=30)
    delivery_operator=models.CharField(max_length=100,null=True,blank=True,default='-')
    transferee=models.CharField(max_length=30,null=True,blank=True,default='-')
    transferee_operator = models.CharField(max_length=100)
    parts=models.ManyToManyField(NumberPart,null=True,blank=True,default='-')
    problem = models.CharField(max_length=255)
    description = models.CharField(
        max_length=255, null=True, blank=True, default="-"
    )
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES
    )

    def save(self, *args, **kwargs):
        self.entry_date = device.functions.save_date_time()
        super(Input, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.work_order_number

    class Meta:
        ordering=('-id',)



