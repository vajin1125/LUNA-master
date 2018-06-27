from django.urls import path

from Registration import views

urlpatterns = [
    path('register/1/', views.registrations_uni_list, name='universities_list'),
    path('register/2/', views.user_university_selection, name='university_selected'),
    path('register/3/', views.request_university_email_domain, name='uni_domain'),
    path('register/4/', views.student_uni_email_input , name='email_input'),
    path('register/5/<user_id>/<verification_key>/', views.email_verification, name='email_verification')
]
