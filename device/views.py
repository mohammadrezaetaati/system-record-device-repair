

from ast import parse
import json
from multiprocessing import context
from persian import convert_en_numbers,convert_fa_numbers
from typing import Union,List

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, CreateView,UpdateView
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,JsonResponse
from django.db.models import QuerySet,ProtectedError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

import device
import place

from .forms import EditBrandCategoryForm, \
    OperationForm, AddDeviceForm,CategoryForm,\
        EditPartsForm,EditStatusForm,EditDeviceNgoingForm,\
            DeviceProvidestatus,DeviceUnrepairableForm
from .models import Input,Category,BrandCategory,Part,NumberPart
from place.models import Branch, Place

from .functions import create_work_order_number,save_date_time


user = get_user_model()


class SeeAllDevice(ListView):
    model = Input
    template_name = "device/device_all.html"
    context_object_name = "devices"



class DeviceNgoing(View):
    device_id=None
    device=None

    def get(self,request):

        devices=Input.objects.filter(status='ngoing')
        print(devices,'llllll')
        places=Place.objects.filter(update='no_update')
        category=Category.objects.all()
        return render(request,'device/devices_ngoing.html',context={'devices':devices,'places':places,'category':category})

    def load_part_table_ajax(request):
        DeviceNgoing.device_id=request.GET.get('device_id')
        category=Category.objects.get(input=DeviceNgoing.device_id)
        parts=Part.objects.filter(category=category)
        return JsonResponse(list(parts.values('name','brand','id')),safe=False)
    
    def load_data_ajax(request):
        DeviceNgoing.device_id = request.GET.get("device_id")
        DeviceNgoing.device: Input = Input.objects.get(id=int(DeviceNgoing.device_id))
 
        # return JsonResponse(list(DeviceNgoing.device.values('branch','delivery','transferee_operator')),safe=False)
        return JsonResponse(
            {
                'device_id':DeviceNgoing.device_id,
                'phone':DeviceNgoing.device.branch.phone,
                'transferee_operator':DeviceNgoing.device.transferee_operator,
                "serial": DeviceNgoing.device.serial,
                'problem':DeviceNgoing.device.problem,
                'place':DeviceNgoing.device.place.name,
                'place_id':DeviceNgoing.device.place.id,
                'branch':DeviceNgoing.device.branch.name,
                "delivery": DeviceNgoing.device.delivery,
                'branch_id':DeviceNgoing.device.branch.id,
                'category':DeviceNgoing.device.category.name,
                'category_id':DeviceNgoing.device.category.id,
                'brand_category':DeviceNgoing.device.brand_category.name,
                'brand_category_id':DeviceNgoing.device.brand_category.id,   
            }
        )
    def obj_exists(self, data: str) -> bool:

        try:
            input=Input.objects.get(serial=convert_fa_numbers(data))
            if input.status != 'finished':
                return True
        except ObjectDoesNotExist:
            return False

    def update(self, data: dict) -> json:
        if DeviceNgoing.device.serial != data["serial"]:
            if self.obj_exists(data=data["serial"]):
                return JsonResponse({"msg": "exists"})
        Input.objects.filter(id=DeviceNgoing.device_id).update(serial=convert_fa_numbers(data.pop('serial')),**data)
        return JsonResponse({"msg": "success"})

    def ajax_delete(request):
        device_id = request.GET.get("device_id")
        input: Input = get_object_or_404(Input, id=int(device_id))
        input.delete()
        return JsonResponse({"msg": "success"})
    
    def ajax_repair_city(request):
        device_id = request.GET.get("device_id")
        Input.objects.filter(id=device_id).update(status='repair_city') 
        return JsonResponse({"msg": "success"})

    def post(self,request):
        if 'unrepairable' in request.POST:
            form=DeviceUnrepairableForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data)
                Input.objects.filter(id=DeviceNgoing.device_id).update(status='unrepairable',**form.cleaned_data,exit_date=save_date_time(),transferee_operator=request.user.username)
                print(DeviceNgoing.device_id,'fffffffffffffffffff')
                return JsonResponse({"msg": "success"})
            else:
                return JsonResponse({"msg": "error"})

        if 'form_edit' in request.POST:
            form=EditDeviceNgoingForm(request.POST)
            if form.is_valid():
                return self.update(form.cleaned_data)
        input:Input=Input.objects.get(id=DeviceNgoing.device_id)
        part=None
        for data in request.POST:
            if len(request.POST.getlist(data))>1 :
                part='yes'
                print(request.POST.getlist(data))
                part_id=request.POST.getlist(data)[0]
                number=request.POST.getlist(data)[1]
                form=EditStatusForm({'number':number})
                if form.is_valid():
                    part=NumberPart.objects.get_or_create(number=form.cleaned_data['number'],part_id=int(part_id))
                    input.parts.add(part[0])
                    input.status='provide' 
                    input.provide_date=save_date_time()       

                else:
                    return JsonResponse({"msg": "error"})

        if request.POST['description'] != '':
            form=EditStatusForm({'description':request.POST['description']})
            if form.is_valid():
                input.description=form.cleaned_data['description']
                input.status='provide'
                input.provide_date=save_date_time()       
            else:
                return JsonResponse({"msg": "error"})
        elif part == None:
            return JsonResponse({'msg':'not device and description'})

        if 'finish_bool' in request.POST:
            form=EditStatusForm({'delivery':request.POST['delivery']})
            if form.is_valid():
                if form.cleaned_data['delivery'] == '' :
                    return JsonResponse({"msg": "null"})
                input.delivery_operator=request.user.username
                input.transferee=form.cleaned_data['delivery']
                input.status='finished'
                input.exit_date=save_date_time()
            else:
                return JsonResponse({"msg": "error"})
        input.save()
        return JsonResponse({"msg": "success"})

class DeviceRepairCity(DeviceNgoing):
    
    def get(self,request):
        devices=Input.objects.filter(status='repair_city')
        places=Place.objects.filter(update='no_update')
        category=Category.objects.all()
        context={
            'devices':devices,
            'places':places,
            'category':category
        }
        return render(request,'device/repair_city.html',context=context)


class DeviceUnrepairable(DeviceNgoing):
    
    def get(self,request):
        devices=Input.objects.filter(status='unrepairable')
        places=Place.objects.filter(update='no_update')
        category=Category.objects.all()
        context={
            'devices':devices,
            'places':places,
            'category':category
        }
        return render(request,'device/device_unrepairable.html',context=context)

class DeviceProvide(View):
    device_id=None
    def get(self,request):
        devices=Input.objects.filter(status='provide')
        return render(request,'device/device_provide.html',context={'devices':devices})
    
    def get_device_id(request):
        DeviceProvide.device_id=request.GET.get('device_id')
        print(DeviceProvide.device_id)
        return JsonResponse({"msg": "success"})

    def return_status_ngoing(request):
        device_id=request.GET.get('device_id')
        input:Input=Input.objects.get(id=device_id)
        input.parts.clear()
        input.description= '-'
        input.exit_date='-'
        input.status='ngoing'
        input.save()
        return JsonResponse({"msg": "success"})
        
    def edit_status_provide(self,data:dict,user):
        Input.objects.filter(id=DeviceProvide.device_id)\
            .update(
                transferee=data.get('delivery'),
                delivery_operator=user,
                status='finished',exit_date=save_date_time()
            )
        return JsonResponse({"msg": "success"})
      
       
        
    def post(self,request):
        print(request.POST)

        if 'status' in request.POST:
            form=DeviceProvidestatus(request.POST)
            print(form.errors)
            if form.is_valid():
                print(form.cleaned_data,'lllllllllllll')
                return self.edit_status_provide(data=form.cleaned_data,user=request.user.username)
        


class DevicePrint(View):

    def get(self,request):
        devices=Input.objects.all()
        return render(request,'device/device_print.html',context={'devices':devices})

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
            serial =convert_fa_numbers(serial)
            if  self.status(serial) == 'ngoing' or self.status(serial) == 'provide':
                return render(request, "device/form_operation.html", context={'status':True})
            request.session["serial"] = serial
            return redirect("/device/add/")
        return render(request, "device/form_operation.html")


class EditStatus(View):

    def get(self,request):
        parts=Part.objects.all()
        return render(request,'device/form_editstatus.html',context={'parts':parts})
    
    def post(self,request):
        form=EditStatusForm({'m':'2'})
        k={'m':[1,2,3],'b':[1,2]}
        for data in request.POST:
            if len(request.POST.getlist(data))>1 :
                print(request.POST.getlist(data))
                part_id=request.POST.getlist(data)[0]
                number=request.POST.getlist(data)[1]
                form=EditStatusForm({'number':number})
                if form.is_valid():
                    part=NumberPart.objects.get_or_create(number=form.cleaned_data['number'],part_id=int(part_id))
                    # print(part[0].id)
                    input:Input=Input.objects.filter(work_order_number='14016/2').values_list('parts')
                    # input.parts.add(part[0])
                    print(input)
                    print(form.cleaned_data)


class Storing(View):

    def get(self, request):
        devices=Category.objects.all()
        places=Place.objects.filter(update='no_update')
       
        context = {
            'devices':devices,
            'places':places,
          
        }
        return render(request, "device/form_add_device.html", context=context)

    def check_create_work_order_number(self) -> str:
        """check filed work_order_number not null for create work_order_number"""
        try:
            last_object: Input = Input.objects.first()
            last_work_orde_number = last_object.work_order_number
        except AttributeError:
            last_work_orde_number = None
        work_order_number = create_work_order_number(last_work_orde_number)
        return work_order_number

    def post(self, request):
        form = AddDeviceForm(request.POST)
        print(form.errors,'rrrrrrrrr')
        devices=Category.objects.all()
        places=Place.objects.all()  
        # context = {"form": form,'devices':devices,'places':places}\
        if form.is_valid():
            Input.objects.create(
               **form.cleaned_data,
                work_order_number=self.check_create_work_order_number(),
                serial=request.session.get("serial"),
                transferee_operator=request.user.username,
                status='ngoing'
            )
            
            return redirect("/device/operation/")
        # return render(request,"device/form_add_device.html", context=context)


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
        print(place_name,'kkkkkkkkkkkkkkkkkkkk')
        branchs = Branch.objects.filter(place_id=place_name,update='no_update')
        print(branchs.values('id', 'name'))
        return JsonResponse(list(branchs.values('id', 'name')), safe=False)

    def load_brand_category(request):
        category_name=request.GET.get('category_name')
        brands=BrandCategory.objects.filter(category__name=category_name)
        return JsonResponse(list(brands.values('id','name')),safe=False)


class EditParts(View):
    part_id=None
    part=None
    
    def get(self,request):
        category=Category.objects.all()
        parts=Part.objects.all()
        context={
            'category':category,
            'parts':parts
        }
        return render(request,'device/form_parts.html',context=context)

    def obj_exists(self,data:dict) -> bool:
        return Part.objects.filter(**data).exists()

    def create(self,data:dict) -> json:
        if self.obj_exists(data):
            return JsonResponse({'msg':'exists'})
        Part.objects.create(brand=convert_fa_numbers(data.pop('brand')),**data)
        return JsonResponse({'msg':'success'})
    
    def load_data_ajax(request) -> json:
        EditParts.part_id=request.GET.get('part_id')
        EditParts.part:Part=get_object_or_404(Part,id=int(EditParts.part_id))
        return JsonResponse({
                'name':EditParts.part.name,
                'brand':EditParts.part.brand,
            })
    
    def update(self,data:dict) -> json:
        category=data['category']
        if EditParts.part.name != data['name'] or \
            EditParts.part.brand != data['brand'] or \
                EditParts.part.category.name != category.name:
                if self.obj_exists(data):
                    return JsonResponse({'msg':'exists'})
        Part.objects.filter(id=int(EditParts.part_id))\
            .update(brand=convert_fa_numbers(data.pop('brand')),**data)
        return JsonResponse({'msg':'success'}) 

    def ajax_delete(request) -> json:
        part_id = request.GET.get("part_id")
        part: Part = get_object_or_404(Part, id=int(part_id))
        try:
            part.delete()
        except ProtectedError:
            return JsonResponse({"msg": "protectederror"})
        return JsonResponse({"msg": "success"})

    def post(self,request):
        form=EditPartsForm(request.POST)
        print(form.errors)
        if form.is_valid():
            if 'form_add' in form.data:
                return self.create(form.cleaned_data)
            else:
                return self.update(form.cleaned_data)
        else:
            return JsonResponse({"msg": "error"})
    


    