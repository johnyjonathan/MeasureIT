from django.contrib import admin
from .models import AllLabs, UserLabs, Device

admin.site.register(AllLabs)
admin.site.register(UserLabs)
admin.site.register(Device)