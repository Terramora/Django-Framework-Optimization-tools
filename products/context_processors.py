from baskets.models import Basket


def basket(requests, basket_list=None):
    if requests.user.is_authenticated:
        basket_list = Basket.objects.filter(user=requests.user)

    return {
        'basket': basket_list
    }
