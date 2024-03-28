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
admin.site.register(Order)
admin.site.register(Statement)