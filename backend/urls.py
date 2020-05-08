from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/users/', include('authentication.urls')),
    path('api/users/', include('profiles.urls', namespace='profiles')),
    path('admin/', admin.site.urls),
]
