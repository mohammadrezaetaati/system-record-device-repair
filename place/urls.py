from django.urls import path

from .views import EditPlace,EditBranch


urlpatterns = [
    path("edit/", EditPlace.as_view(), name="edit-place"),
    path("edit-branch/", EditBranch.as_view(), name="edit-branch"),
    path("ajax-edit-branch", EditBranch.load_data_ajax, name="ajax-edit-branch"),
    path("ajax-edit-place", EditPlace.load_data_ajax, name="ajax-edit-place"),
    path("ajax-delete-place", EditPlace.ajax_delete, name="ajax-delete-place"),
    path("ajax-delete-branch", EditBranch.ajax_delete, name="ajax-delete-branch"),
]
