from .models import (
    Cart,

)


def count_total_product_amount(request):
    total_price = 0
    user_cart = Cart.objects.filter(owner=request.user).first()
    total_product = user_cart.products.count()
    user_cart.total_products = total_product
    for i in user_cart.products.all():
        total_price += i.price
    user_cart.final_price = total_price
    user_cart.save()

    return total_product, total_price
