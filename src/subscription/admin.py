from django.contrib import admin

# Register your models here.
from .models import Customer, Plan, Website

admin.site.register(Customer)
admin.site.register(Plan)
admin.site.register(Website)