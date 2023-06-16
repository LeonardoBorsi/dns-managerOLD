from django.contrib import admin

from .models import (Device, Port)

admin.site.register(Device)     # display Device modal in admin
admin.site.register(Port)     # display Port modal in admin