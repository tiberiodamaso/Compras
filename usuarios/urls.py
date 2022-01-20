from django.urls import path

from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
