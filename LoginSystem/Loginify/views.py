from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserDetails
from django.contrib import messages
# Create your views here.

def test_view(request):
    return HttpResponse("Hello, world!")

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = UserDetails.objects.get(username=username)
            if user.password == password:
                messages.success(request, "Login successful!")
            else:
                messages.error(request, "Login not successful! Incorrect password.")
        except UserDetails.DoesNotExist:
            messages.error(request, "Login not successful! User does not exist.")
        
    return render(request, 'Loginify/login.html')

def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if UserDetails.objects.filter(username=username).exists():
            messages.error(request, "User already exists!")
            return render(request, 'Loginify/signup.html')

        UserDetails.objects.create(username=username, email=email, password=password)
        messages.success(request, "User created successfully!")
        return redirect('/Loginify/login/')  

    return render(request, 'Loginify/signup.html')



