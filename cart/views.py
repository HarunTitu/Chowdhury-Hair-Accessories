from django.shortcuts import redirect
from products.models import Product


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('product_detail', id=product.id)
def cart_detail(request):
    cart = request.session.get('cart', {})

    cart_items = []

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': product.price * quantity,
        })

    total = sum(item['subtotal'] for item in cart_items)

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total': total,
    })