from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator
from .models import Service, Order, Car
from django.db.models import Q

# Create your views here.
def index(request):
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        "num_services": Service.objects.count(),
        "num_orders_done": Order.objects.filter(status__exact='f').count(),
        "num_cars": Car.objects.count(),
        'num_visits': num_visits,
    }
    return render(request, template_name="index.html", context=context)


def search(request):
    query = request.GET.get('query')

    cars_search_results = Car.objects.filter(
        Q(make__icontains=query) | Q(model__icontains=query) | Q(license_plate__icontains=query) | Q(
            vin_code__icontains=query) | Q(client_name__icontains=query))

    context = {
        "query": query,
        "cars": cars_search_results,
    }
    return render(request, template_name="search.html", context=context)

def cars(request):
    cars = Car.objects.all()
    paginator = Paginator(cars, per_page=5)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    return render(request, template_name="cars.html", context={'cars': paged_cars})

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