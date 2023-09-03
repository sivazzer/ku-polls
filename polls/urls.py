from django.urls import include, path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('polls/', include('polls.url')),
    path('admin/', admin.site.urls)
]