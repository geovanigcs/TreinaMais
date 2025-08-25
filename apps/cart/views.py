from django.shortcuts import render
from django.http import HttpResponse


def cart_view(request):
    return HttpResponse("Carrinho - Em desenvolvimento")


def add_to_cart(request, product_id):
    return HttpResponse(f"Adicionar produto {product_id} ao carrinho - Em desenvolvimento")


def remove_from_cart(request, product_id):
    return HttpResponse(f"Remover produto {product_id} do carrinho - Em desenvolvimento")


def update_cart(request, product_id):
    return HttpResponse(f"Atualizar produto {product_id} no carrinho - Em desenvolvimento")


def clear_cart(request):
    return HttpResponse("Limpar carrinho - Em desenvolvimento")
