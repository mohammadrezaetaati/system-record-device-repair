from django.urls import path,include

from .views import Singup,Login,logout,Accounts,EditAccount,EditPassword,EditPasswordUser,delete_account

urlpatterns = [
    path('edit-password-user/<int:id>/', EditPasswordUser.as_view(),name='edit-password-user'),
    path('edit-password/<int:id>/', EditPassword.as_view(),name='edit-password'),
    path('edit/<int:id>/', EditAccount.as_view(),name='edit'),
    path('delete/', delete_account,name='delete-account'),
    path('accounts/', Accounts.as_view(),name='accounts'),
    path('singup/', Singup.as_view(),name='singup'),
    path('login/', Login.as_view(),name='login'),
    path('logout/', logout,name='logout'),
]