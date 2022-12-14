from django.contrib.auth.mixins import PermissionRequiredMixin




class RegistrarPermission(PermissionRequiredMixin):

    def has_permission(self) -> bool:
        user=self.request.user
        if user.role == 'registrar' or user.role == 'administrator':
        # return user.add or user.edit or user.delete or user.change_status
            return True
        return False
        

class AdministratorPermission(PermissionRequiredMixin):
    
    def has_permission(self) -> bool:
        user=self.request.user
        if user.role == 'administrator':
            return True
        return False
              
  
class StoreKeeperPermission(PermissionRequiredMixin):
    
    def has_permission(self) -> bool:
        user=self.request.user
        if user.role == 'storekeeper' or user.role == 'registrar' or user.role == 'administrator':
            return True
        return False
        

