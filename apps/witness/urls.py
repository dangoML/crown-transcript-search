from django.urls import path, re_path
from django.conf.urls import url
from django.views.generic import RedirectView
from .models import Witness
from apps.witness import views

urlpatterns = [
    path('profile_picture/<int:full_name>', views.get_profile_picture_by_full_name,name="image"),
    path('create/', views.create_witness, name='create'),
    path('update/', views.update_witness, name='update'),
    path('download/<str:name>/', views.download_picture, name='download_picture'),
    path('delete/<str:full_name>/', views.delete_witness, name='delete'),
    #path('delete/', views.delete_witness, name='create'),
    

    # Matches any html file

]
