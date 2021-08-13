from django import forms

from ordersapp.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        models = Order
        exclude = ('user',)


class OrderItemsForm(forms.ModelForm):
    price = forms.CharField(label='цена', required=False, widget=forms.TextInput(attrs={
        'readonly': True
    }))

    class Meta:
        model = OrderItem
        exclude = ()
