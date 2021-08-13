from django.conf import settings
from django.db import models

# Create your models here.
from products.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    DELIVERY = 'DLV'
    DONE = 'DN'
    CANCELED = 'CNC'

    STATUSES = (
        (FORMING, 'Формирование'),
        (SENT_TO_PROCEED, 'Передан в обработку'),
        (DELIVERY, 'Доставка'),
        (DONE, 'Выдан'),
        (CANCELED, 'Отменен')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUSES, default=FORMING, max_length=3)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ('-created',)

    def __str__(self):
        return f'Заказ #{self.pk}'

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.get_product_cost, items)))

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='orderitems')

    @property
    def get_product_cost(self):
        return self.quantity * self.product.price
