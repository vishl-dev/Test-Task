from django.contrib import admin
from .models import Component


# Register your models here.
@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
