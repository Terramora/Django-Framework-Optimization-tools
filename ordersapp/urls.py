from django.urls import path
from ordersapp import views

app_name = 'ordersapp'

urlpatterns = [
    path('', views.OrderList.as_view(), name='order_list'),
    path('read/<pk>/', views.OrderItemRead.as_view(), name='order_read'),
    path('update/<pk>/', views.OrderItemUpdate.as_view(), name='order_update'),
    path('delete/<pk>/', views.OrderItemDelete.as_view(), name='order_delete'),
    path('create/', views.OrderItemCreate.as_view(), name='order_create'),
    path('forming/complete/<pk>/', views.order_forming_complete, name='order_forming_complete'),

]
