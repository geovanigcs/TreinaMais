from django.shortcuts import render
from django.http import HttpResponse


def product_list(request):
    return HttpResponse("Lista de produtos - Em desenvolvimento")


def products_by_category(request, category_slug):
    return HttpResponse(f"Produtos da categoria: {category_slug} - Em desenvolvimento")


def products_by_brand(request, brand_slug):
    return HttpResponse(f"Produtos da marca: {brand_slug} - Em desenvolvimento")


def product_search(request):
    return HttpResponse("Busca de produtos - Em desenvolvimento")


def product_detail(request, product_slug):
    return HttpResponse(f"Detalhes do produto: {product_slug} - Em desenvolvimento")
