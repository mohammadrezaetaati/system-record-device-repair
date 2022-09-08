from django.contrib import admin

from .models import Part, Category,Input,BrandCategory


admin.site.register(Part)
admin.site.register(BrandCategory)
admin.site.register(Category)
admin.site.register(Input)









