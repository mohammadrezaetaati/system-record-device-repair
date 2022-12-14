from django.urls import path,include

from .views import CreateUser,Login,logout,Accounts,EditAccount,EditPassword,EditPasswordUser,ViewInformations,delete_account

urlpatterns = [
    path('edit-password-user/<int:id>/', EditPasswordUser.as_view(),name='edit-password-user'),
    path('edit-password/<int:id>/', EditPassword.as_view(),name='edit-password'),
    path('information/<int:pk>', ViewInformations.as_view(),name='user-informations'),
    path('edit/<int:id>/', EditAccount.as_view(),name='edit'),
    path('delete/', delete_account,name='delete-account'),
    path('accounts/', Accounts.as_view(),name='accounts'),
    path('create/', CreateUser.as_view(),name='create-user'),
    path('login/', Login.as_view(),name='login'),
    path('logout/', logout,name='logout'),
]