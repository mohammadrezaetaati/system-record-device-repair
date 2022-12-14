from django.contrib import admin

from .models import Part, Category,BrandCategory,NumberPart,DeviceInput


admin.site.register(Part)
admin.site.register(BrandCategory)
admin.site.register(Category)

admin.site.register(NumberPart)

@admin.register(DeviceInput)
class DeviceInputAdmin(admin.ModelAdmin):

    def brand_category_name(self,obj):
        return obj.brand_category.name

    def category_name(self,obj):
        return obj.category.name

    def place_name(self,obj):
        return obj.place.name

    def branch_name(self,obj):
        return obj.branch.name
    
    # def part_name(self,obj):
    #     print(obj.parts)
    #     return obj.parts

    list_display = ('work_order_number','category','brand_category_name','place_name','branch_name',)










