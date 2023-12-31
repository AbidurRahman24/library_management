from django.shortcuts import render, redirect,get_object_or_404
from .models import CartItem
from books.models import Book
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

def product_list(request):
    products = Book.objects.all()
    return render(request, 'index.html', {'products': products})

# Create your views here.
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.borrowing_price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    product = get_object_or_404(Book, id=product_id)
    user_account = request.user.account
    existing_cart_items = CartItem.objects.filter(user=request.user, product=product)

    if existing_cart_items.exists():
        cart_item = existing_cart_items.first()
        cart_item.quantity += 1
    else:
        cart_item = CartItem(
            user=request.user,
            product=product,
            quantity=1,
            total_price=0,
        )
        
    if user_account.balance >= product.borrowing_price:
        deducted_amount = product.borrowing_price
        user_account.balance -= deducted_amount
        user_account.save()
        cart_item.total_price = deducted_amount
        cart_item.save()
        send_transaction_email(request.user, deducted_amount, "Order Message", "order_email.html")
        return redirect('view_cart')

# def remove_from_cart(request, item_id):
#     cart_item = CartItem.objects.get(id=item_id)
#     cart_item.delete()
#     return redirect('view_cart')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    book = cart_item.product
    user_account = request.user.account

    # Calculate the amount to return to the user
    returned_amount = cart_item.total_price

    # Add the returned amount to the user's balance
    user_account.balance += returned_amount
    user_account.save()

    # Delete the CartItem (book returned)
    cart_item.delete()

    return redirect('view_cart')