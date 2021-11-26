from django.db import models
from django.contrib.auth.models import User

class AllLabs(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    ip_adress = models.CharField(max_length=16)
    id_number = models.CharField(max_length=8)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserLabs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_number = models.ForeignKey(AllLabs,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100, default="12345")
    ip_adress = models.CharField(max_length=16)
    add_date = models.DateTimeField(auto_now_add=True)
    port = models.IntegerField(default="23")
    lab = models.ForeignKey(AllLabs,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    


class Measures(models.Model):
    name = models.CharField(max_length=100)
    device = models.ForeignKey(Device,on_delete=models.CASCADE)
    command = models.CharField(max_length=100)
    output = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    lab = models.ForeignKey(AllLabs,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Commands(models.Model):
    name = models.CharField(max_length=100)
    command = models.CharField(max_length=200)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
