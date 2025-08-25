from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('categoria/<slug:category_slug>/', views.products_by_category, name='category'),
    path('marca/<slug:brand_slug>/', views.products_by_brand, name='brand'),
    path('buscar/', views.product_search, name='search'),
    path('<slug:product_slug>/', views.product_detail, name='detail'),
]
