from django.urls import path

from Fb_login import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('login_success/', views.login_success, name='login_success'),
]
