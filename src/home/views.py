from django.shortcuts import render

def home(request):
    return(request, 'home.html')