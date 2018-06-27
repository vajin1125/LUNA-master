from django.urls import path

from Fb_data import views

urlpatterns = [
    path('data_entry_interface/', views.data_entry_interface, name='data_entry_interface'),
    path('add_university/', views.add_university, name='add_university'),
    path('add_university_society/', views.add_university_society, name='add_university_society'),
    path('add_event/', views.add_event, name='add_event'),
]
