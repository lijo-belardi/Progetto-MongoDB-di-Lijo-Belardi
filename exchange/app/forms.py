from django import forms
from .models import OrderToBuy


class PublishOrderToBuy(forms.ModelForm):
    class Meta:
        model = OrderToBuy
        fields = ['price', 'quantity']