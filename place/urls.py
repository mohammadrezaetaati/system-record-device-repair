from django.urls import path

from .views import EditPlace


urlpatterns = [
    path("edit/", EditPlace.as_view(), name="edit-place"),
    path("ajax-edit-place", EditPlace.ajax_edit, name="ajax-edit-place"),
    path("ajax-delete-place", EditPlace.ajax_delete, name="ajax-delete-place"),


    # path("test/", test, name="test"),

]
