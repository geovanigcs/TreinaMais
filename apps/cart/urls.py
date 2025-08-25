from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='view'),
    path('add/<uuid:product_id>/', views.add_to_cart, name='add'),
    path('remove/<uuid:product_id>/', views.remove_from_cart, name='remove'),
    path('update/<uuid:product_id>/', views.update_cart, name='update'),
    path('clear/', views.clear_cart, name='clear'),
]
