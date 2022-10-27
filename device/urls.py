from django.urls import path

from .views import SeeAllDevice, \
     Storing,Ajax,EditCategory,\
        EditBrandCategory,EditStatus,EditParts,\
            DeviceNgoing,DeviceProvide,DevicePrint,\
                DeviceRepairCity,DeviceUnrepairable,Chart


urlpatterns = [
    path("chart/", Chart.as_view(), name="device-chart"),
    path("unrepairable/", DeviceUnrepairable.as_view(), name="device-unrepairable"),
    path("print/", DevicePrint.as_view(), name="device-print"),
    path("all/", SeeAllDevice.as_view(), name="device-all"),
    path("ngoing/", DeviceNgoing.as_view(), name="device-ngoing"),
    path("provide/", DeviceProvide.as_view(), name="device-provide"),
    path("repair-city/", DeviceRepairCity.as_view(), name="device-repair-city"),
    path("ajax-repair-city/", DeviceRepairCity.ajax_repair_city, name="ajax-repair-city"),
    path("ajax-status-provide/", DeviceProvide.get_device_id, name="ajax-status-provide"),
    path("ajax-return-status-ngoing/", DeviceProvide.return_status_ngoing, name="ajax-return-status-ngoing"),
    path("load_part_table_ajax", DeviceNgoing.load_part_table_ajax, name="load_part_table_ajax"),
    path("ajax-edit-device", DeviceNgoing.load_data_ajax, name="ajax-edit-device"),
    path("ajax-delete-device", DeviceNgoing.ajax_delete, name="ajax-delete-device"),
    path("edit-status/", EditStatus.as_view(), name="edit-status"),
    path("add/", Storing.as_view(), name="add-device"),
    path("parts/", EditParts.as_view(), name="edit-part"),
    path("load-data-ajax", EditParts.load_data_ajax, name="load-data-ajax"),
    path("ajax-delete-part", EditParts.ajax_delete, name="ajax-delete-part"),
    path('ajax/load-branchs/', Ajax.load_Branchs, name='ajax_load_branchs'),
    path('ajax/load-brands-category/', Ajax.load_brand_category, name='ajax_load_brands-category'),
    path('add-category',EditCategory.as_view(),name='add-category'),
    path('edit-brand-category/',EditBrandCategory.as_view(),name='edit-brand-category'),

]
