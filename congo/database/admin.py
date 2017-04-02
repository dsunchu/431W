from django.contrib import admin
from .models import supplier
from .models import RegisteredUser

# Register your models here.

admin.site.register(supplier)
admin.site.register(RegisteredUser)