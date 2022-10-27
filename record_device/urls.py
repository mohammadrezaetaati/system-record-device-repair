from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from device.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('device/', include('device.urls')),
    path('place/', include('place.urls')),
    path('', home),

    path('user/', include('user.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
