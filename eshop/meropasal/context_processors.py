from .models import CartItems

def cart_item_count(request) -> dict[str, int]:
    cart_item_count = 0
    if request.user.is_authenticated:
        user = request.user
        cart_item_count = CartItems.objects.filter(cart__user=user).count()
    return {'cart_item_count': cart_item_count}