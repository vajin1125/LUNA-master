from django.urls import path

from Users import views

urlpatterns = [
    path('register/6/', views.follow_university_societies, name='update_uni_following'),
    path('toggle_On/', views.toggle_On, name='toggle_uni_soc_following'),
    path('toggle_Off/', views.toggle_Off, name='toggle_uni_soc_unfollowing'),
    path('user_profile/', views.user_profile, name='user_profile')
]
