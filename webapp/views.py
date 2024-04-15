from django.shortcuts import render

def home(request):
    return render(request,"webapp/index.html")

def register(request):
    pass