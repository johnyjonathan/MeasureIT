from django.core.exceptions import ObjectDoesNotExist
from django.http import request
from django.shortcuts import redirect, render, get_object_or_404
from .forms import UserCreationForm, CreateLabForm, AddLabForm, AddDeviceForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import AllLabs, Device, UserLabs
from .functions import generate_id, addCreatedLab
from django.contrib import messages

tiles = True

def home(request):
    return render(request, 'measureit/index.html')

def signin(request):
    if request.method == 'GET':
        return render (request, 'measureit/login.html',{'form': AuthenticationForm()})
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render (request, 'measureit/login.html',{'form': AuthenticationForm(), 'error': 'Username or password did not match'})
        else:
            login(request, user)
            return redirect('loggedin')

def loggedin(request):
    labs = AllLabs.objects.filter(owner = request.user)
    return render(request, 'measureit/loggedin.html', {'labs':labs})

def signup(request):
    if request.method == 'GET':
        return render(request, 'measureit/signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:   
                user = User.objects.create_user(request.POST['username'], email=request.POST['email'], password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('loggedin')
            except IntegrityError:
                return render(request, 'measureit/signup.html', {'form': UserCreationForm(), 'error':'That username has already taken'})
        else:
            return render(request, 'measureit/signup.html', {'form': UserCreationForm(), 'error':'Passwords did not match'})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def createLab(request):
    if request.method == "GET":
        return render(request, 'measureit/createlab.html', {'form':CreateLabForm()})
    else:
        try:
            form = CreateLabForm(request.POST)
            if not form.is_valid():
                #messages.info(request, 'Fields can not be empty.')
                return render(request, 'measureit/createlab.html', {'form':CreateLabForm(), 'error': 'Fields can not be empty.'})
            else:
                newlab = form.save(commit=False)
                try:   
                    exist_ip = AllLabs.objects.get(ip_adress = newlab.ip_adress)
                    return render(request, 'measureit/createlab.html', {'form':CreateLabForm(), 'error': 'IP adress already exist'})
                except ObjectDoesNotExist:
                    newlab.owner = request.user
                    newlab.id_number = generate_id()

                    newlab.save()
                    messages.info(request, 'Succes!')
                    return redirect('createlab')
        except ValueError:
            return render(request, 'measureit/createlab.html', {'form':CreateLabForm(), 'error': 'Something gone wrong :('})


def joinLab (request):
    if request.method == "GET":
        return render(request, 'measureit/joinlab.html')
    else:
        if request.POST.get("join"):
            ip_adress = AllLabs.objects.filter(ip_adress = request.POST['join_ip'])

            if len(ip_adress) == 0:
                return render(request, 'measureit/joinlab.html', {'error' : "There aren't any matching IP adress"})
            else: 
                id_number = get_object_or_404(AllLabs, ip_adress = request.POST['join_ip'])
                return redirect('labauth', id_number = id_number.id_number)
             

def LabAuth(request, id_number):
    if request.method == "GET":
        return render(request,'measureit/labauth.html',{'id':id_number})
    else:
        if request.POST.get("connect"):
            password_from_db = get_object_or_404(AllLabs,id_number = id_number)
            password = request.POST.get("password")
            if password_from_db.password == password:
                return redirect('labsite', id_number = id_number)
            else:
                return render(request,'measureit/labauth.html',{'error':'Bad'})

def labSite(request, id_number): 
    if request.method == "GET":
        lab_info = AllLabs.objects.filter(id_number = id_number)
        lab_devices = Device.objects.filter(lab = lab_info[0].id)
        return render(request,'measureit/labsite.html', {'lab_info':lab_info, 'lab_devices': lab_devices})
    else:
        if request.POST.get("add_device"):
           return redirect('adddevice', id_number = id_number)
        if request.POST.get("add_m_measuer"):
            return redirect('add_m_measure', id_number = id_number)
        
    
def addDevice(request, id_number):
    if request.method == "GET":
        return render(request,'measureit/add_device.html',{'form':AddDeviceForm()})
    else:
        p_key = get_object_or_404(AllLabs, id_number = id_number)
        try:
            form = AddDeviceForm(request.POST)
            if not form.is_valid():
                return render(request,'measureit/add_device.html',{'form':AddDeviceForm(), 'error': 'Fields can not be empty.'})
            else:
                newdevice = form.save(commit=False)
                newdevice.lab_id = p_key.id
                newdevice.save()
                return render(request,'measureit/add_device.html',{'form':AddDeviceForm(), 'error': 'Oki :)'})
        except ValueError:
            return render(request,'measureit/add_device.html',{'form':AddDeviceForm(), 'error': 'Something gone wrong :('})

def addManualMeasure(request, id_number):
    return render(request,'measureit/add_m_measure.html',{'form':AddDeviceForm()})
    

