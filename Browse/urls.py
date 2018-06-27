from django.urls import path

from Browse import views


urlpatterns = [
    path('feed/', views.feed, name='feed'),
    path('event/', views.event_page, name='event_detail'),
    path('rsvp_response/', views.rsvp_status_change, name='rsvp_status_change'),
    path('uni_socs_profile/', views.uni_socs_profile, name='profile'),
    path('uni_soc_profile_all_events', views.uni_soc_profile_all_events, name='uni_soc_profile_all_events'),
    path('search_all_events/', views.search_all_event_from_uni, name='search_all_events'),
    path('my_events/', views.my_events, name='my_events'),

]
