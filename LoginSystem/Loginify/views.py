from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserDetails
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserDetailsSerializer
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

@api_view(['GET'])
def get_all_user_details(request):
    if request.method == "GET":
        users = UserDetails.objects.all()
        serializer = UserDetailsSerializer(users, many=True)
        return Response({"users": serializer.data}, status=200)

@api_view(['GET'])
def get_user_by_email(request, email):
    try:
        # Retrieve user by email
        user = UserDetails.objects.get(email=email)
        # Serialize the user
        serializer = UserDetailsSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except UserDetails.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT'])
def update_user_details(request, username):
    try:
        user = UserDetails.objects.get(username=username)
    except UserDetails.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserDetailsSerializer(user, data=request.data, partial=True)  
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user_by_email(request, email):
    try:
        user = UserDetails.objects.get(email=email)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
    except UserDetails.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

