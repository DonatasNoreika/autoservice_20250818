from django.shortcuts import render, reverse, redirect
from django.views import generic
from django.core.paginator import Paginator
from .models import Service, Order, Car, CustomUser
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from .forms import OrderReviewForm, CustomUserCreateForm, CustomUserChangeForm
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy

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


class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = 'order'
    form_class = OrderReviewForm

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid(self, form):
        form.instance.order = self.get_object()
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class UserOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "user_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)

def signup(request):
    form = CustomUserCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.info(request, "Vartotojas registruotas")
        return redirect('login')
    return render(request, 'signup.html', context={"form": form})


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')
    context_object_name = "user"

    def get_object(self, queryset=None):
        return self.request.user