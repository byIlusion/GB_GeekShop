from basketapp.models import Basket


def basket(request):
    print(f'Context processor. Basket')
    user_basket = []
    if request.user.is_authenticated:
        user_basket = Basket.objects.filter(user=request.user)
    return {
        'basket': user_basket,
    }


def basket_stat(request):
    print(f'Context processor. Basket statistic')
    total_quantity = 0
    total_sum = 0.0
    if request.user.is_authenticated:
        user_basket = basket(request)['basket']
        total_quantity = Basket.basket_total_quantity(user_basket)
        total_sum = Basket.basket_total_sum(user_basket)
    return {
        'basket_stat': {
            'total_quantity': total_quantity,
            'total_sum': total_sum,
        },
    }
