from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(District)
admin.site.register(DistTemp)