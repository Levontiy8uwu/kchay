from django.contrib import admin
from django.urls import path, include
from business_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('business_app.urls')),
    path('', views.index, name='index'),
]