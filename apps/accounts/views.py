from django.shortcuts import render
from django.http import HttpResponse


def login_view(request):
    return HttpResponse("Login - Em desenvolvimento")


def register_view(request):
    return HttpResponse("Registro - Em desenvolvimento")


def logout_view(request):
    return HttpResponse("Logout - Em desenvolvimento")


def profile_view(request):
    return HttpResponse("Perfil - Em desenvolvimento")


def address_list(request):
    return HttpResponse("Lista de endereços - Em desenvolvimento")


def order_history(request):
    return HttpResponse("Histórico de pedidos - Em desenvolvimento")
