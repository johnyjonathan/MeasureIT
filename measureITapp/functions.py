import string
import random
from .models import AllLabs, UserLabs
import paramiko, platform, subprocess
from scp import SCPClient
from os import path, remove
import time

def generate_id (size = 8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def addCreatedLab(user, id_number):
    add_lab = UserLabs.objects.create(user = user, id_number = id_number)
    add_lab.save()
    pass

def pingServer(ip):
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
    args = "ping " + " " + ping_str + " " + ip
    need_sh = False if  platform.system().lower()=="windows" else True

    # Ping
    return subprocess.call(args, shell=need_sh) == 0

def modyfiCommand(command):
    if " " in command:
        modyfi = command.replace(" ","+")
        return modyfi
    else:
        return command

class ServerConnector:
    def __init__(self, ip_server, ip_device, server_password, device_password, server_name, device_name):
        self.server_ip = ip_server
        self.device_ip = ip_device
        self.server_name = server_name
        self.device_name = device_name
        self.server_pass = server_password
        self.device_pass = device_password
    
    def establishConnection(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.load_system_host_keys()
        self.ssh.connect(self.server_ip, 22, self.server_name, self.server_pass)
        
        
    def useCommand(self, command):
        self.ssh.exec_command(command)

    def commandToTelnet(self, command):
        func_ssh_str = """telnetConnect('{0}','{1}','{2}','{3}')"""
        func_ssh = func_ssh_str.format(self.device_ip, self.device_name, self.device_pass, command)
        command_value_str = """python3 -c "import telnet; telnet.{0}" """
        command_value = command_value_str.format(func_ssh)
        self.ssh.exec_command(command_value)


    def getFileScp(self):
        scp = SCPClient(self.ssh.get_transport())
        scp.get("/home/" + self.server_name + "/telnet_output.txt")
    
    def isFileExist(self):
        timeout = time.time()+11
        timeout_end = time.time()+30
        while True:
            if time.time() > timeout:
                self.getFileScp()
                time.sleep(2)
                if path.isfile('telnet_output.txt'):
                    return 1
                    break
                    
                else:
                    return 0
            elif time.time() > timeout_end:
                return 'can not reach the file'

class FileManager:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, "r")
    
    def read(self):
        self.lines_list = self.file.readlines()
        return self.lines_list

    def delete(self):
        self.file.close()
        if path.exists(self.filename):
            remove(self.filename)

    def cutText(self, key_word):
        l1 = [string_ for string_ in self.lines_list if key_word in string_]
        index_ = self.lines_list.index(l1[0])
        cutted_list =[]
        for x in range(index_, len(self.lines_list)):
            cutted_list.append(self.lines_list[x])
        return cutted_list[:-1]