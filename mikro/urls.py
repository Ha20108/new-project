from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomePage,name='home'),
    path('newdvice',views.newdvice,name='newdvice'),
    path('all_dvice',views.all_dvice,name='all_dvice'),
    path('hotspot_create',views.hotspot_create,name='hotspot_create'),


    #path('extract_message/<int:device_id>/', views.extract_message, name='extract_message'),
    #path('execute_command/', views.execute_command, name='execute_command'),
    path('delete_device/<int:pk>/', views.delete_device, name='delete_device'), # إضافة رابط delete
    path('edit_device/<int:pk>/', views.edit_device, name='edit_device'),
    path('device_info/<int:pk>/', views.device_info, name='device_info'),
    path('hotspot_user/<int:pk>/', views.hotspot_user, name='hotspot_user'),
    path('hotspot/<int:pk>/', views.hotspot, name='hotspot'),



    





    
    
]
