from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_view),  
    path('login/', views.login_view),
    path('signup/',views.signup_view),
]