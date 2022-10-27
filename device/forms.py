

from dataclasses import fields
from distutils.command.install_egg_info import to_filename
from pyexpat import model
from django import forms
import place

from place.models import Branch, Place

from .models import Input,Category,BrandCategory,Part

class OperationForm(forms.Form):
    serial = forms.CharField(max_length=255)
    


class AddDeviceForm(forms.ModelForm):
    category=forms.ModelChoiceField(queryset=Category.objects.all(),to_field_name='name')
    brand_category=forms.ModelChoiceField(queryset=BrandCategory.objects.all(),to_field_name='id')
    place=forms.ModelChoiceField(queryset=Place.objects.all(),to_field_name='id')
    branch=forms.ModelChoiceField(queryset=Branch.objects.all(),to_field_name='id')

    class Meta:
        model=Input
        # exclude=('parts','work_order_number','serial','status','transferee',)
        fields=['category','brand_category','place','branch','problem','delivery','serial']



class CategoryForm(forms.Form):

    create_name=forms.CharField(max_length=100,required=False)
    update_name=forms.CharField(max_length=100,required=False)
    hidden=forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)
    category=forms.ModelMultipleChoiceField(queryset=Category.objects.all(),to_field_name='id',required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.data) == 1 :
            self.fields['create_name'].required=True
        if 'create_name' in  self.data and self.data['create_name'] == '':
            self.fields['create_name'].required=True
        if 'update_name' in  self.data and self.data['update_name'] == '':
            self.fields['update_name'].required=True
    

class EditBrandCategoryForm(CategoryForm):
    brandcategory=forms.ModelMultipleChoiceField(queryset=BrandCategory.objects.all(),to_field_name='id',required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'brandcategory' in  self.data and self.data['brandcategory'] == '':
            self.fields['category'].required=True
    

        
            # print(self.data['create_name'],'llllllllllllllllll')
     
class DeviceUnrepairableForm(forms.Form):
    transferee=forms.CharField(max_length=30)
    description=forms.CharField(max_length=255)
    
class EditPartsForm(forms.ModelForm):
    
     class Meta:
        model=Part
        exclude=['number']

class EditStatusForm(forms.Form):
    number=forms.IntegerField(required=False)
    delivery=forms.CharField(max_length=100,required=False)
    seal_number=forms.CharField(max_length=20,required=False)
    description=forms.CharField(max_length=255,required=False)

class EditDeviceNgoingForm(forms.ModelForm):
    category=forms.ModelChoiceField(queryset=Category.objects.all(),to_field_name='name')
    place=forms.ModelChoiceField(queryset=Place.objects.all(),to_field_name='id')
    
    class Meta:
        model=Input
        exclude=('work_order_number','entry_date','exit_date','delivery_operator','transferee','transferee_operator','parts','description','status')
    
class DeviceProvidestatus(forms.Form):
    delivery=forms.CharField(max_length=100)
 


class EditStatusLaptopForm(forms.Form):

    ram = forms.BooleanField()
    brand_ram = forms.CharField(max_length=25)
    amount_ram=forms.IntegerField(required=False)
    number_ram = forms.IntegerField(required=False)
    # cpu = forms.BooleanField()
    # number_cpu = forms.IntegerField()
    # brand_cpu = forms.CharField(max_length=255)
    # gpu = forms.BooleanField()
    # number_gpu = forms.IntegerField()
    # brand_gpu = forms.CharField(max_length=255)
    # mainboard = forms.BooleanField()
    # hdd = forms.BooleanField()
    # number_hdd = forms.IntegerField()
    # brand_hdd = forms.CharField(max_length=255)
    # ssd = forms.BooleanField()
    # number_ssd = forms.IntegerField()
    # brand_ssd = forms.CharField(max_length=255)
