from django.contrib import admin
from .models import AllLabs, UserLabs, Device, Measures, Commands

admin.site.register(AllLabs)
admin.site.register(UserLabs)
admin.site.register(Device)
admin.site.register(Measures)
admin.site.register(Commands)