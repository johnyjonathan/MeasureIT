from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields
from django.forms import ModelForm
from .models import AllLabs, UserLabs, Device, Measures, Commands


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CreateLabForm(ModelForm):
    class Meta:
        model = AllLabs
        fields = ['name','description','ip_adress','password']

class AddLabForm(ModelForm):
    class Meta:
        model = UserLabs
        fields = []

class AddDeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ['name','password','ip_adress','port']
        
class MeasureForm(ModelForm):
    class Meta:
        model = Measures
        fields =['name', 'device', 'command','output','lab']
        
class AddCommandForm(ModelForm):
    class Meta:
        model = Commands
        fields = ['name', 'command', 'device']