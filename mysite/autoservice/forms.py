from .models import OrderReview
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = ['content']