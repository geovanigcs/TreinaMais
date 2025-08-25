def cart(request):
    """Context processor para o carrinho"""
    return {
        'cart_total_items': 3,
        'cart_total_price': 1299.70,
    }


def categories(request):
    """Context processor para categorias"""
    return {
        'main_categories': [
            {'name': 'Musculação', 'slug': 'musculacao'},
            {'name': 'Cardio', 'slug': 'cardio'},
            {'name': 'Acessórios', 'slug': 'acessorios'},
            {'name': 'Suplementos', 'slug': 'suplementos'},
        ]
    }
