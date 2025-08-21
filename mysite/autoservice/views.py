from django.shortcuts import render
from .models import Service, Order, Car

# Create your views here.
def index(request):
    context = {
        "num_services": Service.objects.count(),
        "num_orders_done": Order.objects.filter(status__exact='f').count(),
        "num_cars": Car.objects.count(),
    }
    return render(request, template_name="index.html", context=context)

