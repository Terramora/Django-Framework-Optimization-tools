from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from baskets.models import Basket
from ordersapp.forms import OrderItemsForm
from ordersapp.models import Order, OrderItem


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:order_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemCreate, self).get_context_data(**kwargs)

        order_form = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)

        if self.request.method == 'POST':
            formset = order_form(self.request.POST)
        else:
            basket = Basket.objects.filter(user=self.request.user)
            if basket.exists():
                OrderFormSet = inlineformset_factory(Order,
                                                     OrderItem,
                                                     form=OrderItemsForm,
                                                     extra=basket.count())
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket[num].product
                    form.initial['quantity'] = basket[num].quantity
            else:
                formset = order_form()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
                Basket.objects.filter(user=self.request.user).delete()

        return super(OrderItemCreate, self).form_valid(form)


class OrderItemUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:order_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemUpdate, self).get_context_data(**kwargs)

        order_form = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)

        if self.request.method == 'POST':
            formset = order_form(self.request.POST, instance=self.object)
        else:
            formset = order_form(instance=self.object)

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        return super(OrderItemUpdate, self).form_valid(form)


class OrderItemDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:order_list')

class OrderItemRead(DetailView):
    model = Order

def order_forming_complete(request, pk):
    order_item = get_object_or_404(Order, pk=pk)
    order_item.status = Order.SENT_TO_PROCEED
    order_item.save()

    return HttpResponseRedirect(reverse('ordersapp:order_list'))
