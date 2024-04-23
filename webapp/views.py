from django.shortcuts import render ,redirect
from .forms import CreateUserForm,LoginForm ,AddRecord,UpdateRecord

from django.contrib import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from .models import Record


def home(request):
    return render(request,"webapp/index.html")

def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('login')
    
    context = {'form': form}

    return render(request,"webapp/register.html",context = context)


def login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request , data = request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request , username = username, password = password)

            if user is not None:
                auth.login(request , user)

                return redirect('dashboard')

    context = {'form': form}

    return render(request, 'webapp/login.html', context = context)


@login_required(login_url='login')
def dashboard(request):
    records = Record.objects.all()

    context = {
        'records': records
    }

    return render(request, 'webapp/dashboard.html',context)


@login_required(login_url='login')
def create_record(request):

    form = AddRecord()

    if request.method == 'POST':
        form = AddRecord(request.POST)

        if form.is_valid():
            form.save()

            return redirect('dashboard')
        
    context = {
        'form': form,
    }

    return render(request, 'webapp/create_record.html',context)


def logout(request):
    auth.logout(request)
    
    return redirect('login')