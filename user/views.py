from itertools import permutations
from optparse import AmbiguousOptionError
from persian import convert_fa_numbers

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth import authenticate,login,logout as logout_
from django.views.generic import ListView,UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .permissions import AdministratorPermission,RegistrarPermission
from .forms import SingupForm,EditPasswordUserForm
from .models import User
# from .models import Person
# from .permissions import registrar, reporter,administrator





class Singup(LoginRequiredMixin,AdministratorPermission,View):

    def get(self,request):
        form = SingupForm(request.GET)
        return render(request,'user/singup.html',context={'form':form})

    def post(self,request):
        form = SingupForm(request.POST)

        if form.errors:
            print(form.errors,'llllllllllll')
            return JsonResponse(form.errors.get_json_data())
            # for filed,mees in form.errors.get_json_data().items():
            #     print(filed,mees)
            # if 'username' in form.errors:
            #     print('username already exists')
            # if 'password2' in form.errors:
            #     print(form.errors.json_data())
        if form.is_valid():
            form.save()
            return render(request,'user/singup.html')

           
class Login(View):

    def get(self,request):
        return render(request,'user/login.html')

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        username=convert_fa_numbers(username)
        user = authenticate(request,username=username,password=password)
        print(user)
    
        print(username,'jjjjjjjjjjjjjjjjjjjjjjj')
        print(password)
        if user:
            login(request,user)
            return redirect('/device/ngoing/')
        else:
            return render(request,'user/login.html',context={'invalid':True})


class Accounts(LoginRequiredMixin,AdministratorPermission,ListView):
    model = User
    template_name = 'user/accounts.html'
    context_object_name = 'accounts'


class EditAccount(LoginRequiredMixin,AdministratorPermission,UpdateView):
    model = User
    template_name = 'user/edit-informations.html'
    pk_url_kwarg = "id"
    context_object_name = 'account'
    success_url = '/user/accounts/'
    fields=['first_name','last_name','username','add','edit','delete','role','change_status']

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.username=convert_fa_numbers(form.cleaned_data.get('username')) 
        print(form.cleaned_data)
        if form.cleaned_data.get('role') == 'administrator':
            form.instance.add=True
            form.instance.edit=True
            form.instance.delete=True
            form.instance.change_status=True
        # if form.cleaned_data.get('role') == 'reporter':
        #     reporter(user=form.instance)
        # if form.cleaned_data.get('role') == 'registrar':
        #     registrar(user=form.instance,data=form.cleaned_data)
        form.save()
        return response

class EditPassword(LoginRequiredMixin,AmbiguousOptionError,UpdateView):
    model = User
    template_name='user/edit-password.html'
    pk_url_kwarg = "id"
    context_object_name = 'account'
    success_url = '/user/accounts/'
    fields=['password']
    
    def form_valid(self, form):
        response = super().form_valid(form)
        password = form.cleaned_data.get('password')
        user = self.get_object()
        user.set_password(password)
        user.save()
        return response

class EditPasswordUser(UpdateView):

    model = User
    form_class = EditPasswordUserForm
    template_name = 'user/edit-password-user.html'
    pk_url_kwarg = 'id'
    context_object_name = 'account'
    success_url = '/user/edit-password-user/'

    def form_invalid(self, form):
        message_error=[]
        for error in form.errors.get_json_data().get('password2'):
            message_error.append(error['code'])
        return JsonResponse(list(message_error),safe=False)
    def form_valid(self, form) :
        message_error=[]
        if form.instance.check_password(form.cleaned_data.get('old_password')) :
            if form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
                form.instance.set_password(form.cleaned_data.get('password2'))
                form.save()
                message_error.append('success')  
                login(self.request,form.instance) 
        else:
            message_error.append('Not correct old_password')
        return JsonResponse(list(message_error),safe=False)


def delete_account(request):
    user_id=request.GET.get('user_id')
    user:User=User.object.filter(id=user_id)
    user.delete()
    return JsonResponse({'msg':'success'})


def logout(request):
    logout_(request)
    return render(request,'user/login.html')