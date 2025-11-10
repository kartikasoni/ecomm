from django.shortcuts import render
from urllib import request
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Sum, F
from .models import Product, Cart, Wishlist, Order, OrderItem
from .models_address import Address
# Profile view
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'app/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'app/edit_profile.html', {'user': user})

# Address management views
@login_required
def saved_address(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'app/saved_address.html', {'addresses': addresses})

@login_required
def add_address(request):
    if request.method == 'POST':
        Address.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
            phone=request.POST.get('phone'),
        )
        messages.success(request, 'Address added successfully!')
        return redirect('saved_address')
    return render(request, 'app/add_address.html')

@login_required
def edit_address(request, address_id):
    address = Address.objects.get(id=address_id, user=request.user)
    if request.method == 'POST':
        address.full_name = request.POST.get('full_name', address.full_name)
        address.address = request.POST.get('address', address.address)
        address.city = request.POST.get('city', address.city)
        address.state = request.POST.get('state', address.state)
        address.pincode = request.POST.get('pincode', address.pincode)
        address.phone = request.POST.get('phone', address.phone)
        address.save()
        messages.success(request, 'Address updated successfully!')
        return redirect('saved_address')
    return render(request, 'app/edit_address.html', {'address': address})

@login_required
def delete_address(request, address_id):
    address = Address.objects.get(id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted successfully!')
    return redirect('saved_address')
from decimal import Decimal

# Create your views here.
def home(request):
    from .models import Blog
    blogs = Blog.objects.all().order_by('-date')[:3]  # Show latest 3 blogs
    """Home page view"""
    products = Product.objects.all()
    featured_products = products.order_by('-created_at')[:4]  # 4 newest
    latest_products = products.order_by('-created_at')[:10]  # 10 newest (New Arrivals)
    best_seller_products = products.order_by('price')[:10]  # 10 cheapest (Best Seller)
    trending_products = products.order_by('-updated_at')[:10]  # 10 most recently updated (Trending)
    special_offer_products = products.order_by('price')[:10]  # 10 cheapest (Special Offer)
    categories = Product.objects.values_list('category', flat=True).distinct()

    subscribe_success = False
    if request.method == 'POST' and 'subscribe_email' in request.POST:
        email = request.POST.get('subscribe_email')
        message = request.POST.get('subscribe_message', '')
        # Here you could save to DB or send an email. For now, just show success.
        subscribe_success = True

    context = {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'best_seller_products': best_seller_products,
        'trending_products': trending_products,
        'special_offer_products': special_offer_products,
        'categories': categories,
        'subscribe_success': subscribe_success,
        'blogs': blogs
    }
    return render(request, "app/home.html", context)

def blog(request):
    from .models import Blog
    category = request.GET.get('category')
    blogs = Blog.objects.all().order_by('-date')
    if category:
        blogs = blogs.filter(category=category)
    categories = Blog.objects.values_list('category', flat=True).distinct()
    top_categories = categories  # For now, same as categories, but could be limited or sorted by count
    recent_posts = Blog.objects.all().order_by('-date')[:3]  # Always show latest 3 blogs, not filtered by category
    return render(request, "app/blog.html", {
        'blogs': blogs,
        'categories': categories,
        'recent_posts': recent_posts,
        'selected_category': category,
        'top_categories': top_categories
    })

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # TODO: Add password reset logic
        messages.success(request, 'Password reset instructions have been sent to your email.')
        return redirect('login')
    return render(request, "app/forget_password.html")
  
@login_required
def account_dashboard(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    wishlist_count = Wishlist.objects.filter(user=user).count()
    address_count = Address.objects.filter(user=user).count()
    cart_count = Cart.objects.filter(user=user).count()
    recent_orders = orders.order_by('-created_at')[:3]
    context = {
        'user': user,
        'orders': orders,
        'orders_count': orders.count(),
        'wishlist_count': wishlist_count,
        'address_count': address_count,
        'cart_count': cart_count,
        'recent_orders': recent_orders,
    }
    return render(request, "app/account_dashboard.html", context)

def blogdetails(request, blog_id):
    from .models import Blog
    blog_post = get_object_or_404(Blog, pk=blog_id)
    recent_posts = Blog.objects.exclude(pk=blog_id).order_by('-date')[:3]
    return render(request, "app/blogdetails.html", {'post': blog_post, 'recent_posts': recent_posts})

def About_us(request):
    return render(request, "app/About_us.html")

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, "app/wishlist.html", {'wishlist_items': wishlist_items})

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        # TODO: Add email sending logic
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact_us')
    return render(request, "app/contact_us.html")

def product_list(request):
    """Display all products"""
    all_products = Product.objects.all()
    featured_products = all_products[:6]  # Get first 6 products as featured
    latest_products = Product.objects.order_by('-created_at')[:6]  # Get 6 most recent products
    categories = Product.objects.values_list('category', flat=True).distinct()
    
    return render(request, 'app/products.html', {
        'products': all_products,
        'featured_products': featured_products,
        'latest_products': latest_products,
        'categories': categories
    })


def product_detail(request, product_id):
    """Display single product details"""
    product = Product.objects.get(product_id=product_id)
    return render(request, 'app/product_detail.html', {'product': product})

def category_products(request, category_name):
    """Display products by category"""
    products = Product.objects.filter(category=category_name)
    categories = Product.objects.values_list('category', flat=True).distinct()
    
    context = {
        'products': products,
        'category': category_name,
        'categories': categories
    }
    return render(request, 'app/category.html', context)




# CART VIEWS
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        # stock check
        if product.stock < quantity:
            messages.error(request, f'Only {product.stock} items available in stock!')
            return redirect('product_detail', product_id=product_id)
        
        # upsert cart row
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock:
                messages.error(request, f'Cannot add more than {product.stock} items!')
                return redirect('cart_view')
            cart_item.save()
            messages.success(request, f'Updated {product.name} quantity in cart!')
        else:
            messages.success(request, f'{product.name} added to cart!')

    # if this was triggered with ?buy_now=1, go straight to checkout
    if request.GET.get('buy_now') == '1':
        return redirect('checkout')

    # default go to cart
    return redirect('cart_view')
     
    
    


@login_required
def cart_view(request):
    """Display shopping cart"""
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    
    total = sum(item.subtotal for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'app/cart.html', context)


@login_required
def update_cart(request, cart_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > cart_item.product.stock:
            messages.error(request, f'Only {cart_item.product.stock} items available!')
        elif quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully!')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart!')
    
    return redirect('cart_view')


@login_required
def remove_from_cart(request, cart_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart!')
    return redirect('cart_view')


# WISHLIST VIEWS
@login_required
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    product = get_object_or_404(Product, product_id=product_id)
    
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if created:
        messages.success(request, f'{product.name} added to wishlist!')
    else:
        messages.info(request, f'{product.name} is already in your wishlist!')
    
    return redirect('wishlist_view')


@login_required
def wishlist_view(request):
    """Display wishlist"""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'app/wishlist.html', context)


@login_required
def remove_from_wishlist(request, wishlist_id):
    """Remove item from wishlist"""
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    product_name = wishlist_item.product.name
    wishlist_item.delete()
    messages.success(request, f'{product_name} removed from wishlist!')
    return redirect('wishlist_view')


@login_required
def move_to_cart(request, wishlist_id):
    """Move item from wishlist to cart"""
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    product = wishlist_item.product
    
    # Check stock first so we don't allow impossible quantities
    if product.stock <= 0:
        messages.error(request, f"Sorry, {product.name} is out of stock.")
        return redirect('wishlist_view')
    
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        # only increase if we won't exceed stock
        if cart_item.quantity + 1 > product.stock:
            messages.warning(request, f"Only {product.stock} units of {product.name} available. Quantity not increased.")
        else:
            cart_item.quantity += 1
            cart_item.save()
    
    wishlist_item.delete()
    messages.success(request, f'{product.name} moved to cart!')
    return redirect('cart_view')


# CHECKOUT & ORDER VIEWS
@login_required
def checkout(request):
    """Checkout page"""
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart_view')
    
    total = sum(item.subtotal for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'app/checkout.html', context)


@login_required
def place_order(request):
    """Process order placement"""
    if request.method == 'POST':
        print('DEBUG POST DATA:', request.POST)
        cart_items = Cart.objects.filter(user=request.user).select_related('product')
        
        if not cart_items.exists():
            messages.error(request, 'Your cart is empty!')
            return redirect('cart_view')
        
        # Get form data
        full_name = request.POST.get('full_name')
        if not full_name:
            # Try to fallback to user's full name or username
            full_name = request.user.get_full_name() or request.user.username
        if not full_name:
            messages.error(request, 'Full name is required to place an order.')
            return redirect('checkout')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        payment_method = request.POST.get('payment_method')
        
        # Calculate total
        total = sum(item.subtotal for item in cart_items)
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            total_amount=total,
            payment_method=payment_method,
            payment_status='completed' if payment_method == 'cod' else 'pending',
            order_status='confirmed'
        )
        
        # Create order items and update stock
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            
            # Update product stock
            product = cart_item.product
            product.stock -= cart_item.quantity
            product.save()
        
        # Clear cart
        cart_items.delete()
        
        messages.success(request, f'Order #{order.order_id} placed successfully!')
        return redirect('order_detail', order_id=order.order_id)
    
    return redirect('checkout')


@login_required
def order_list(request):
    """Display user's order history"""
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    
    context = {
        'orders': orders,
    }
    return render(request, 'app/order_list.html', context)


@login_required
def order_detail(request, order_id):
    """Display order details"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'app/order_detail.html', context)


@login_required
def cancel_order(request, order_id):
    """Cancel an order"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    if order.order_status in ['pending', 'confirmed']:
        # Restore stock
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
        
        order.order_status = 'cancelled'
        order.save()
        messages.success(request, f'Order #{order.order_id} cancelled successfully!')
    else:
        messages.error(request, 'This order cannot be cancelled!')
    
    return redirect('order_detail', order_id=order_id)


# USER AUTHENTICATION
def register(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        terms = request.POST.get('terms')
        
        if not all([username, email, password, password2, terms]):
            messages.error(request, 'All fields are required!')
            return redirect('register')
            
        if not terms:
            messages.error(request, 'You must agree to the Terms and Conditions!')
            return redirect('register')
            
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long!')
            return redirect('register')
        
        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('register')
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Registration successful! Please login.')
            return redirect('user_login')
        except Exception as e:
            messages.error(request, 'An error occurred during registration. Please try again.')
        messages.success(request, 'Registration successful! Please login.')
        return redirect('user_login')
    
    return render(request, 'app/register.html')


def user_login(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'app/login.html')


@login_required
def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')