from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_view),  
    path('login/', views.login_view),   
    path('signup/',views.signup_view),
    path('api/getusers/',views.get_all_user_details),
    path('api/getuserbyemail/<str:email>/',views.get_user_by_email),
    path('api/updateuser/<str:username>/',views.update_user_details),
    path('api/deleteuser/<str:email>/',views.delete_user_by_email),
]