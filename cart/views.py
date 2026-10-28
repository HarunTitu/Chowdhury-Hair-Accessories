from django.shortcuts import render, redirect
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
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_detail')

def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        product_id = str(product_id)
        quantity = int(request.POST.get('quantity', 1))

        if product_id in cart:
            if quantity > 0:
                cart[product_id] = quantity
            else:
                del cart[product_id]

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart_detail')