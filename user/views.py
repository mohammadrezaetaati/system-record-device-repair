from persian import convert_fa_numbers

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout as logout_
from django.views.generic import ListView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.db.models import Q, Count

from device.models import DeviceInput
from .permissions import AdministratorPermission, RegistrarPermission
from .forms import CreateUserForm, EditPasswordUserForm, EditAccountForm, AccountForm
from .models import User


class CreateUser(LoginRequiredMixin, AdministratorPermission, View):
    def get(self, request):
        form = CreateUserForm(request.GET)
        return render(request, "user/create-user.html", context={"form": form})

    def post(self, request):
        request.POST = request.POST.copy()
        request.POST["username"] = convert_fa_numbers(request.POST.get("username"))
        form = CreateUserForm(request.POST)
        if form.errors:
            for error in form.errors.get_json_data()["username"]:
                if error.get("code") == "unique":
                    return JsonResponse({"msg": "unique"})
        if form.is_valid():
            form.save()
            return JsonResponse({"msg": "success"})


class Login(View):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        username = convert_fa_numbers(username)
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_first_login:
                login(request, user)
                return redirect(reverse(("edit-password-user"), args=[user.id]))
            login(request, user)
            return redirect("/device/ngoing/")
        else:
            return render(request, "user/login.html", context={"invalid": True})


class Accounts(LoginRequiredMixin, AdministratorPermission, ListView):

    model = User
    template_name = "user/accounts.html"
    context_object_name = "accounts"
    form_class = AccountForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["number_all_user"] = User.object.all().count()
        context["number_users"] = User.object.values("role").annotate(
            count=Count("role")
        )
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        form = self.form_class(self.request.GET)
        if form.is_valid():
            search = convert_fa_numbers(form.cleaned_data.get("search"))
            qs = (
                super()
                .get_queryset()
                .filter(
                    Q(username__contains=search)
                    | Q(first_name__contains=search)
                    | Q(last_name__contains=search)
                )
            )
            print(form.cleaned_data, "yyyyyyyyyyy")
        return qs


class EditAccount(LoginRequiredMixin, AdministratorPermission, UpdateView):

    model = User
    form_class = EditAccountForm
    template_name = "user/edit-informations.html"
    pk_url_kwarg = "id"
    context_object_name = "account"
    success_url = "/user/accounts/"
    initial = {"name": "ali"}

    def post(self, request, *args, **kwargs):
        request.POST = request.POST.copy()
        request.POST["username"] = convert_fa_numbers(request.POST.get("username"))
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class EditPassword(LoginRequiredMixin, AdministratorPermission, UpdateView):

    model = User
    template_name = "user/edit-password.html"
    pk_url_kwarg = "id"
    context_object_name = "account"
    success_url = "/user/accounts/"
    fields = ["password"]

    def form_valid(self, form):
        response = super().form_valid(form)
        password = form.cleaned_data.get("password")
        user = self.get_object()
        user.set_password(password)
        user.is_first_login = True
        user.save()
        return response


class EditPasswordUser(LoginRequiredMixin, UpdateView):

    model = User
    form_class = EditPasswordUserForm
    template_name = "user/edit-password-user.html"
    pk_url_kwarg = "id"
    context_object_name = "account"
    success_url = "/user/edit-password-user/"

    def get(self, request, *args: str, **kwargs):
        if self.request.user.id != kwargs["id"]:
            return render(request, "errors/page_403.html")
        return super().get(request, *args, **kwargs)

    def form_invalid(self, form):
        message_error = []
        for error in form.errors.get_json_data().get("password2"):
            message_error.append(error["code"])
        return JsonResponse(list(message_error), safe=False)

    def form_valid(self, form):
        message_error = []
        if form.instance.check_password(form.cleaned_data.get("old_password")):
            if form.cleaned_data.get("password1") == form.cleaned_data.get("password2"):
                form.instance.set_password(form.cleaned_data.get("password2"))
                form.save()
                if form.instance.is_first_login:
                    message_error.append("success,user new")
                    form.instance.is_first_login = False
                    form.save()
                else:
                    message_error.append("success")
                login(self.request, form.instance)
        else:
            message_error.append("Not correct old_password")
        return JsonResponse(list(message_error), safe=False)

class ViewInformations(DetailView):

    model = User
    template_name = "user/view-informations.html"
    # context_object_name = 'devices'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["devices"] = DeviceInput.objects.filter(
            place__storekeeper__id=self.get_object().id
        )
        return context

    # def get(self,request):
    #     user=Place.objects.filter(storekeeper__username='170')
    #     print(user)
    #     return render(request,'user/view-informations.html')


def delete_account(request):
    user_id = request.GET.get("user_id")
    user: User = User.object.filter(id=user_id)
    user.delete()
    return JsonResponse({"msg": "success"})


def logout(request):
    logout_(request)
    return render(request, "user/login.html")
