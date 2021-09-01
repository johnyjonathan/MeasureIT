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
    ip_adress = models.CharField(max_length=16)
    mac_adress = models.CharField(max_length=100)
    add_date = models.DateTimeField(auto_now_add=True)
    measure_type = models.CharField(max_length=100)
    units = models.CharField(max_length=10)
    connection_type = models.CharField(max_length=20)
    lab = models.ForeignKey(AllLabs,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
# class ManualMeasure(models.Model):
#     title = models.CharField(max_length=200)
#     date = models.DateTimeField(auto_now_add=True)
#     device = models.ForeignKey(Device,on_delete=models.CASCADE)
#     lab = models.ForeignKey(AllLabs,on_delete=models.CASCADE)
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     description = models.TextField(blank=True)
#     img = models.ImageField(upload_to="measureit/images", default='default.jpg', blank = True)
#     value = models.CharField(max_length=200)
#     prefix = models.CharField(max_length=1)
    
#     def __str__(self):
#         return self.name

class Measures(models.Model):
    name = models.CharField(max_length=100)
    device = models.ForeignKey(Device,on_delete=models.CASCADE)
    command = models.CharField(max_length=100)
    output = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    lab = models.ForeignKey(AllLabs,on_delete=models.CASCADE)
    def __str__(self):
        return self.name