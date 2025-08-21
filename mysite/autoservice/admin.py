from django.contrib import admin
from .models import Order, OrderLine, Service, Car

# Register your models here.

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'price']
    list_editable = ['name', 'price']

class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'client_name', 'license_plate', 'vin_code']
    list_filter = ['make', 'model', 'client_name']
    search_fields = ['license_plate', 'vin_code']

class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0
    fields = ['service', 'quantity', 'line_sum']
    readonly_fields = ['line_sum']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['car', 'date', 'total', 'status']
    inlines = [OrderLineInLine]
    readonly_fields = ['date', 'total']
    list_editable = ['status']

    fieldsets = [
        ("General", {"fields": ['car', 'date', 'total', 'status']})
    ]

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['order', 'service', 'service__price', 'quantity', 'line_sum']

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Car, CarAdmin)