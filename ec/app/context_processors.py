
from .models import Product, Cart

def categories_processor(request):
    categories = Product.objects.values_list('category', flat=True).distinct()
    return {'categories': categories}

def cart_items_processor(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user).select_related('product')
    else:
        cart_items = []
    return {'cart_items': cart_items}