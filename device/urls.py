from django.urls import path

from .views import SeeAllDevice, \
    Operation, Storing,Ajax,EditCategory,EditBrandCategory


urlpatterns = [
    path("see-all/", SeeAllDevice.as_view(), name="device-all"),
    path("operation/", Operation.as_view(), name="operation"),
    path("add/", Storing.as_view(), name="add-device"),
    path('ajax/load-branchs/', Ajax.load_Branchs, name='ajax_load_branchs'),
    path('ajax/load-brands-category/', Ajax.load_brand_category, name='ajax_load_brands-category'),
    path('add-category',EditCategory.as_view(),name='add-category'),
    path('edit-brand-category/',EditBrandCategory.as_view(),name='edit-brand-category'),

]
