from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('cars/', views.cars, name="cars"),
    path('cars/<int:car_id>', views.car, name="car"),
    path('signup/', views.signup, name="signup"),
    path('profile/', views.ProfileUpdateView.as_view(), name="profile"),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name="order"),
    path('orders/', views.OrderListView.as_view(), name="orders"),
    path('userorders/', views.UserOrderListView.as_view(), name="userorders"),
    path('userorders/create', views.UserOrderCreateView.as_view(), name="orders_create"),
    path('userorders/<int:pk>/edit', views.UserOrderUpdateView.as_view(), name="orders_edit"),
    path('userorders/<int:pk>/delete', views.UserOrderDeleteView.as_view(), name="orders_delete"),
]
