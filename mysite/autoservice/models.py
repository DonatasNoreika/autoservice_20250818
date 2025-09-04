from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tinymce.models import HTMLField
from django.contrib.auth.models import AbstractUser
from PIL import Image

class CustomUser(AbstractUser):
    photo = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        min_side = min(img.width, img.height)
        left = (img.width - min_side) // 2
        top = (img.height - min_side) // 2
        right = left + min_side
        bottom = top + min_side
        img = img.crop((left, top, right, bottom))
        img = img.resize((300, 300), Image.LANCZOS)
        img.save(self.photo.path)

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
    description = HTMLField(null=True, blank=True)

    def __str__(self):
        return f"{self.make} {self.model}"

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"

class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(to="Car", on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(to="autoservice.CustomUser", on_delete=models.SET_NULL, null=True, blank=True, related_name="client")
    deadline = models.DateTimeField(null=True, blank=True)

    ORDER_STATUS = (
        ('c', 'Created'),
        ('p', 'In Progress'),
        ('f', 'Finished'),
        ('x', 'Cancelled'),
    )

    status = models.CharField(verbose_name="Status", choices=ORDER_STATUS, max_length=1, blank=True, default='c')

    def is_overdue(self):
        return self.deadline and timezone.now() > self.deadline

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


class OrderReview(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(to="autoservice.CustomUser", on_delete=models.CASCADE, related_name="author")
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.date_created}"

    class Meta:
        ordering = ['-pk']