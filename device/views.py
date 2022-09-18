

import json
from persian import convert_en_numbers
from typing import Union,List

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, CreateView,UpdateView
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,JsonResponse
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from .forms import EditBrandCategoryForm, OperationForm, AddDeviceForm, EditStatusLaptopForm,CategoryForm
from .models import Input,Category,BrandCategory
from place.models import Branch, Place

from .functions import create_work_order_number


user = get_user_model()


class SeeAllDevice(ListView):
    model = Input
    template_name = "device/view_all_device.html"
    context_object_name = "devices"
    # paginate_by: int = 10

    def get_ordering(self):
        return "-id"
    

class Operation(View):
    """check operation for save or change status device"""
    def get(self, request):

        form = OperationForm()
        context = {"form": form}
        return render(request, "device/form_operation.html", context=context)
        
    def device_exists(self,serial:str) -> bool:
        device: Input = Input.objects.filter(
                serial=serial
            ).exists()
        return device

    def status(self,serial) -> str:
        """return status device"""
        if self.device_exists(serial):
            status=Input.objects.filter(serial=serial).values('status').last()
            return status.get('status')
    # def show_next_page(self,operation,serial):
    #     if operation == 'Save' and  self.status(serial) == "دردست اقدام" :
    #         return render(self.request, "form_operation.html", context={'status':True})
    #     elif operation == 'Change_status' and self.status(serial="آماده به تحویل"):
    #         return rend
    def post(self, request):
        form = OperationForm(request.POST)
        if form.is_valid():
            serial = form.cleaned_data.get("serial")
            operation = form.cleaned_data.get("operation")
            serial =convert_en_numbers(serial)
            if operation == 'Save' and  self.status(serial) == "دردست اقدام" :
                return render(request, "device/form_operation.html", context={'status':True})
            request.session["serial"] = serial
            return redirect("/device/add/")
        return render(request, "device/form_operation.html")


class EditStatus(View):

    def get(self,request):
        return render(request,'device/form_editstatus.html')
    
    def post(self,request):
        form=EditStatusLaptopForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print(form.cleaned_data)


class Storing(View):

    def get(self, request):
        devices=Category.objects.all()
        places=Place.objects.all()
        context = {
            'devices':devices,
            'places':places,
        }
        return render(request, "device/form_add_device.html", context=context)

    def check_create_work_order_number(self) -> str:
        """check filed work_order_number not null for create work_order_number"""
        try:
            last_object: Input = Input.objects.last()
            last_work_orde_number = last_object.work_order_number
        except AttributeError:
            last_work_orde_number = None
        work_order_number = create_work_order_number(last_work_orde_number)
        return work_order_number

    def post(self, request):
        form = AddDeviceForm(request.POST)
        print(request.POST)
        devices=Category.objects.all()
        places=Place.objects.all()  
        context = {"form": form,'devices':devices,'places':places}
        if form.is_valid():
            admin = user.objects.get(username="admin")
            Input.objects.create(
               **form.cleaned_data,
                work_order_number=self.check_create_work_order_number(),
                serial=request.session.get("serial"),
                transferee=admin,
            )
            
            return redirect("/device/operation/")
        return render(request,"device/form_add_device.html", context=context)


class EditCategory(View):
    
    def get(self,request):
        context={'category':Category.objects.all()}
        return render(request,'device/form_add_category.html',context=context)

    def obj_exists(self,name:str,queryset:QuerySet) -> bool:
        return queryset.objects.filter(name=name).exists()

    def response(self,message:str) -> json:
        if message == 'success':
            return JsonResponse({'msg':'success'})
        elif message == 'exists':
            return JsonResponse({'msg':'exists'})
        else:
            return JsonResponse({'msg':'error'})

    def create(self,name:str,queryset:QuerySet) -> json:
        if self.obj_exists(name,queryset):
            return self.response('exists')
        queryset.objects.create(name=name)    
        return self.response('success')
        
    def update(self,queryset:Union[QuerySet,list[Category,BrandCategory]],name_new:str):
        return queryset.update(name=name_new)
        
    def delete(self,queryset:Union[QuerySet,list[Category,BrandCategory]]):
        return queryset.delete()
    
    def post(self,request):
        form=CategoryForm(request.POST)
        if form.is_valid():
            if 'create_name' in request.POST:
                return self.create(name=form.cleaned_data.get('create_name'),queryset=Category)
            if 'update_name' in request.POST:
                self.update(queryset= form.cleaned_data.get('category'),name_new= form.cleaned_data.get('update_name'))
            if 'category' in request.POST:
                self.delete(form.cleaned_data.get('category'))
            return self.response('success')
        else:
            return self.response('error')

       


class EditBrandCategory(EditCategory):

    def get(self,request):
        context={'category':Category.objects.all()}
        return render(request,'device/form_edit_brandcategory.html',context=context)

    def obj_exists(self,category:object,name:str) -> bool:
        return BrandCategory.objects.filter(category=category,name=name).exists()

    def create(self,category,name):
        category=get_object_or_404(Category,name=category)
        if self.obj_exists(category,name):
            return self.response('exists')
        BrandCategory.objects.create(category=category,name=name)
        return self.response('success')
    
    def post(self,request):
            form=EditBrandCategoryForm(request.POST)
            print(form.errors)
            if form.is_valid():
                if 'create_name' in form.data:
                    print('create_name',form.cleaned_data)
                    return self.create(form.cleaned_data.get('hidden'),form.cleaned_data.get('create_name'))
                elif 'update_name' in form.data:
                    print('update_name',form.cleaned_data)
                    self.update(queryset=form.cleaned_data.get('brandcategory'),name_new=form.cleaned_data.get("update_name"))
                else: 
                    self.delete(form.cleaned_data.get('brandcategory'))
                return self.response('success')
            else:
                return self.response('error')


class Ajax:
    """
    It refreshes the input page without 
    reloading to load branch, brand_category
    """
        
    def load_Branchs(request):
        place_name = request.GET.get('place_name')
        print(place_name)
        branchs = Branch.objects.filter(place__name=place_name)
        return JsonResponse(list(branchs.values('id', 'name')), safe=False)

    def load_brand_category(request):
        
        category_name=request.GET.get('category_name')
        brands=BrandCategory.objects.filter(category__name=category_name)
        return JsonResponse(list(brands.values('id','name')),safe=False)



    