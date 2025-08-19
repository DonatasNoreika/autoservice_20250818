from django.contrib import admin
from .models import Order, OrderLine, Service, Car

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderLine)
admin.site.register(Service)
admin.site.register(Car)