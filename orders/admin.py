from django.contrib import admin
from .models import Customer, Medication, Order, Statement

admin.site.register(Customer)
admin.site.register(Medication)
admin.site.register(Order)
admin.site.register(Statement)