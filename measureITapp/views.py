from os import path
from django.core.exceptions import ObjectDoesNotExist
from django.http import request
from django.shortcuts import redirect, render, get_object_or_404
from .forms import UserCreationForm, CreateLabForm, AddLabForm, AddDeviceForm, MeasureForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import AllLabs, Device, UserLabs, Measures
from .functions import generate_id, addCreatedLab, pingServer, ServerConnector, FileManager, modyfiCommand, reverseModyficommand
from django.contrib import messages
import paramiko

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
    if request.method == 'GET':
        labs = AllLabs.objects.filter(owner = request.user)
        _info = []
        for x in range(len(labs)):
            if pingServer(labs[x].ip_adress) == True:
                _info.append("Online")
            else:
                _info.append("Offline")
        zipped_list = zip(labs, _info)
        return render(request, 'measureit/loggedin.html', {'context':zipped_list})
    else:
        labs = AllLabs.objects.filter(owner = request.user)
        if request.POST.get('connector'):
            _name = request.POST['connector']
            _id = get_object_or_404(AllLabs, id_number = _name)
            return redirect('labauth', id_number = _id.id_number)
        else:
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
        lab = get_object_or_404(AllLabs,id_number = id_number)
        return render(request,'measureit/labauth.html',{'id':lab.name})
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
        lab_info = AllLabs.objects.filter(id_number = id_number)
        lab_devices = Device.objects.filter(lab = lab_info[0].id)
        if request.POST.get("add_device"):
           return redirect('adddevice', id_number = id_number)
        if request.POST.get("add_m_measuer"):
            return redirect('add_m_measure', id_number = id_number)
        if request.POST.get("check_status"):
            lab_info = get_object_or_404(AllLabs,id_number = id_number)
            if pingServer(lab_info.ip_adress) == True:
                messages.info(request, 'Server is online')
                return redirect('labsite', id_number = id_number)
            else:
                messages.info(request, 'Server is offline')
                return redirect('labsite',  id_number = id_number)
        if request.POST.get("use"):
            value = request.POST['use']
            device = get_object_or_404(Device, id = value)
            return redirect('device', id_number = id_number, name = device.name)
        else:
            messages.info(request, lab_devices[0].name)
            return redirect('labsite',  id_number = id_number)
        if request.POST.get("measures_list"):
            return redirect('measures', id_number = id_number)

def measures(request, id_number):
    if request.method == "GET":
        lab = get_object_or_404(AllLabs, id_number = id_number)
        measures = Measures.objects.filter(lab = lab.id)
        return render(request,'measureit/measures/measures.html',{'data':measures})   
    else:
        lab = get_object_or_404(AllLabs, id_number = id_number)
        device = get_object_or_404(Device, lab=lab.id)
        if request.POST.get('details'):
            _name = request.POST['details']
            _measure = get_object_or_404(Measures, id = _name)
            return redirect('measure_detail', id_number = id_number, id = _measure.id)
        else:
            return render(request,'measureit/measures/measures.html')         
        
def measureDetail(request, id_number, id):
    if request.method == "GET":
        measure = get_object_or_404(Measures, id = id)
        return render(request,'measureit/measures/measure_detail.html',{'measure':measure})
    else:
        if request.POST.get('back'):
           return redirect('measures', id_number = id_number)
    
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

def device(request, id_number, name):
    if request.method == "GET":
        return render(request,'measureit/device.html')
    else:
        lab_info = AllLabs.objects.filter(id_number = id_number)
        device_info = Device.objects.filter(name = name)

        server_ip = lab_info[0].ip_adress
        server_name = lab_info[0].name
        server_pass = lab_info[0].password

        device_ip = device_info[0].ip_adress
        device_name = device_info[0].name
        device_pass = device_info[0].password


        connection = ServerConnector(server_ip, device_ip, server_pass, device_pass, server_name, device_name)
        connection.establishConnection()

        if request.POST.get("send_command"):
            if path.exists('telnet_output.txt'):
                file = FileManager('telnet_output.txt')
                file.delete()
            try:
                command = request.POST['command']
                connection.commandToTelnet(command)
                if connection.isFileExist() == 1:
                    return redirect('measure_result', id_number = id_number, name = name, command = modyfiCommand(command))
                else:
                    messages.info(request, 'Can not reach file')
                    return redirect('device', id_number = id_number, name = name)
            except:
                messages.info(request, 'Error')

        return render(request,'measureit/device.html')

def measureResult(request, id_number, name, command):
    if request.method == "GET":
        file_data = FileManager('telnet_output.txt')
        measure_data = file_data.read()
        cutted = file_data.cutText(name)
        return render(request,'measureit/measures/measure_result.html',{'data':cutted})
    else:
        file_data = FileManager('telnet_output.txt')
        measure_data = file_data.read()
        cutted = file_data.cutText(name)
        if request.POST.get('return'):
            return redirect('device', id_number = id_number, name = name)   
        elif request.POST.get('exit'):
            return redirect('labsite',  id_number = id_number)
        elif request.POST.get('save'):
            measure_name = request.POST['result_name']
            lab_data = get_object_or_404(AllLabs, id_number = id_number)
            device_data = get_object_or_404(Device, lab = lab_data.id)
            try:
                form = MeasureForm()
                new_measure = form.save(commit=False)
                
                new_measure.name = measure_name
                new_measure.device = device_data
                new_measure.command = command
                new_measure.output = cutted
                new_measure.lab = lab_data
                new_measure.save()
                messages.info(request, "Saved!")
            except:
                messages.info(request, "Can not save this measure")    

            return render(request,'measureit/measures/measure_result.html',{'data':cutted})
        else:
            return render(request,'measureit/measures/measure_result.html',{'data':cutted})

