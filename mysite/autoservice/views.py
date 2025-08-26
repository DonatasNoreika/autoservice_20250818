from django.shortcuts import render
from django.views import generic

from .models import Service, Order, Car

# Create your views here.
def index(request):
    context = {
        "num_services": Service.objects.count(),
        "num_orders_done": Order.objects.filter(status__exact='f').count(),
        "num_cars": Car.objects.count(),
    }
    return render(request, template_name="index.html", context=context)


def cars(request):
    return render(request, template_name="cars.html", context={'cars': Car.objects.all()})

def car(request, car_id):
    return render(request, template_name="car.html", context={'car': Car.objects.get(pk=car_id)})

class OrderListView(generic.ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = 'orders'
    paginate_by = 5


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = 'order'