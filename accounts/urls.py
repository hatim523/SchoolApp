from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('user_redirect', views.user_redirect, name='user_redirect'),
    path('logout', views.logout, name='logout'),
]