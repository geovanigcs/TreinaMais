from django.shortcuts import render
from django.http import HttpResponse


def order_list(request):
    return HttpResponse("Lista de pedidos - Em desenvolvimento")


def checkout(request):
    return HttpResponse("Checkout - Em desenvolvimento")


def order_detail(request, order_id):
    return HttpResponse(f"Detalhes do pedido: {order_id} - Em desenvolvimento")
