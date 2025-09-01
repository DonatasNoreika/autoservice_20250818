from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Service(models.Model):
    name = models.CharField()
    price = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"


class Car(models.Model):
    make = models.CharField()
    model = models.CharField()
    license_plate = models.CharField()
    vin_code = models.CharField()
    client_name = models.CharField()
    photo = models.ImageField(upload_to='cars', null=True, blank=True)

    def __str__(self):
        return f"{self.make} {self.model}"

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"

class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(to="Car", on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)

    ORDER_STATUS = (
        ('c', 'Created'),
        ('p', 'In Progress'),
        ('f', 'Finished'),
        ('x', 'Cancelled'),
    )

    status = models.CharField(verbose_name="Status", choices=ORDER_STATUS, max_length=1, blank=True, default='c')


    def total(self):
        total = 0
        for line in self.lines.all():
            total += line.line_sum()
        return total


    def __str__(self):
        return f"{self.car} - {self.date}"

    class Meta:
        verbose_name = "Užsakymas"
        verbose_name_plural = "Užsakymai"

class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE, related_name='lines')
    service = models.ForeignKey(to="Service", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def line_sum(self):
        return self.service.price * self.quantity

    def __str__(self):
        return f"{self.service} ({self.service.price}) - {self.quantity}"

    class Meta:
        verbose_name = "Eilutė"
        verbose_name_plural = "Eilutės"