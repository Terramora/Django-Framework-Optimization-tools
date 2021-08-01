from django.shortcuts import render
from products.models import Product, ProductCategory
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def index(requests):
    context = {'title': 'GeekShop Store'}
    return render(requests, 'products/index.html', context)


def products(requests, category_id=None, page=1):
    context = {
        'categories': ProductCategory.objects.all(),
        'year': datetime.now().year,
        'title': 'Products'
    }
    products = Product.objects.all() if not category_id else Product.objects.filter(category_id=category_id)

    if products.exists():
        paginator = Paginator(products, 3)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(1)

        context['products'] = products_paginator
    else:
        context['products'] = None
    return render(requests, 'products/products.html', context)
