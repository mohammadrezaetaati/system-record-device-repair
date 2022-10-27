from django.contrib.auth.models import Permission
from django.contrib.auth.mixins import PermissionRequiredMixin




class RegistrarPermission(PermissionRequiredMixin):

    def has_permission(self) -> bool:
        user=self.request.user
        return user.add or user.edit or user.delete or user.change_status
        

class AdministratorPermission(PermissionRequiredMixin):
    
    def has_permission(self) -> bool:
        user=self.request.user
        if user.role == 'administrator':
            return True
        return False
              
        # has_perm('user.can_edit') or \
        #         user.has_perm('user.can_add') or \
        #         user.has_perm('user.can_delete')
                

# def administrator(user:object):
#     """
#     It takes a user object and adds the permission to access all the admin pages to that user
    
#     :param user: the user object
#     :type user: object
#     """
#     user.user_permissions.clear()
#     permission=Permission.objects.get(codename='can_all_access')
#     user.user_permissions.add(permission)
#     user.is_staff = True
#     user.is_superuser = True


# def reporter(user:object):
#     """
#     It takes a user object and adds the permission to report to it
    
#     :param user: The user object that you want to assign the permissions to
#     :type user: object
#     """
#     user.user_permissions.clear()
#     user.is_staff = False
#     user.is_superuser = False
#     permission=Permission.objects.get(codename='can_report')
#     user.user_permissions.add(permission)
#     print(Permission.objects.filter(user=user),'hhhhhhhhhh')


# def registrar(user:object, data:dict):
#     """
#     It takes a user object and a dictionary of permissions and adds or removes the permissions from the
#     user object
    
#     :param user: The user object that you want to add permissions to
#     :type user: object
#     :param data: This is the data that is passed from the form
#     :type data: dict
#     """
#     permission_registrar={'add':'can_add','edit':'can_edit','delete':'can_delete'}
#     user.user_permissions.clear()
#     user.is_staff = False
#     user.is_superuser = False
#     for role,permission_code in permission_registrar.items():
#             if data.get(role):
#                 permission=Permission.objects.get(codename=permission_code)
#                 user.user_permissions.add(permission)
#             else:
#                 permission=Permission.objects.get(codename=permission_code)
#                 user.user_permissions.remove(permission)

#     print(Permission.objects.filter(user=user),'hhhhhhhhhh')
