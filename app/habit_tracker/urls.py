from django.contrib import admin
from django.urls import path, include

handler403 = 'tracker.views.custom_403'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),
]