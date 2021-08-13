from django.db import models
from users.models import User
from products.models import Product


class BasketQuerySet(models.QuerySet):
    
    def delete(self):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
            
        super(BasketQuerySet, self).delete()


# Create your models here.
class Basket(models.Model):
    objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина {self.user.username} | Продукт {self.product.name}'

    def total_quantity(self):
        return sum((basket.quantity for basket in Basket.objects.filter(user=self.user)))

    def sum(self):
        return self.quantity * self.product.price

    def total_sum(self):
        return sum((basket.sum() for basket in Basket.objects.filter(user=self.user)))


    def delete(self, using=None, keep_parents=False):
        self.product.quantity += self.quantity
        self.product.save()

        super(Basket, self).delete()

