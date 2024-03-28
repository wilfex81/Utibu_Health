from django.contrib import admin
from .models import Customer, Medication, Order, Statement

admin.site.register(Customer)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'formatted_price')

    def formatted_price(self, obj):
        currency_symbol = 'KSH.'
        return f"{currency_symbol} {obj.price}"

    formatted_price.short_description = 'Price'

admin.site.register(Medication, MedicationAdmin)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'medications_list', 'total_price')

    def medications_list(self, obj):
        return ", ".join([f"{medication.name} - {medication.price}" for medication in obj.medications.all()])

    medications_list.short_description = 'Medications'

admin.site.register(Order, OrderAdmin)
admin.site.register(Statement)