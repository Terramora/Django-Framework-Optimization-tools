from django import forms

from ordersapp.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        models = Order
        exclude = ('user',)


class OrderItemsForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ()
