from django.urls import path
from . import views

urlpatterns = [path('overview',views.index, name='index')]

urlpatterns = [
    path('callback', views.callback),
]