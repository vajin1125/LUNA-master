from django.urls import path
from Uni_Socs import views


urlpatterns = [
    path('register/5/', views.show_all_uni_socs, name='query_clubs')
]
