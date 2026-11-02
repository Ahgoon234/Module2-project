from django.shortcuts import render,get_object_or_404,redirect
from lore.models import CarModel,BrandModel,CategoryModel,SparepartModel,PartCategoryModel,BlogModel,ContactMsgModel,CartModel,CartItemModel,UserProfileModel,OrderModel,OrderItemModel,CONDITION_CHOICES,FUEL_CHOICES,TRANSMISSION_CHOICES
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_POST


# =======Home======= #
def index(request):
    new_cars = (
        CarModel.objects
        .filter(condition='new')
        .select_related('brand','category')
        .order_by('-created_at')[:5]
    )
    used_cars = (
        CarModel.objects
        .filter(condition='used')
        .select_related('brand','category')
        .order_by('-created_at')[:5]
    )
    featured_cars = (
        CarModel.objects
        .filter(is_featured = True)
        .select_related('brand','category')
        .order_by('-created_at')
    )
    brands = BrandModel.objects.all()
    categories = CategoryModel.objects.all()
    blogs = BlogModel.objects.all().order_by('-created_at')[:2]
    
    context = {
        'new_cars': new_cars,
        'used_cars': used_cars,
        'featured_cars': featured_cars,
        'brands': brands,
        'categories': categories,
        'blogs': blogs,
        'fuel_choices': FUEL_CHOICES,
    }
    return render(request, 'website/index.html',context)


# =======About us======= #
def about(request):
    contactmsgs = ContactMsgModel.objects.all().order_by('-created_at')
    brands = BrandModel.objects.all().order_by('-created_at')
    cars_count = CarModel.objects.count()
    review_count = ContactMsgModel.objects.count()
    user_count = User.objects.count()
    
    context = {
        'contactmsgs': contactmsgs,
        'brands': brands,
        'cars_count': cars_count,
        'review_count': review_count,
        'user_count': user_count,
    }
    return render(request,'website/about.html',context)


# =======Contact======= #
@login_required
def contact(request):
    brands = BrandModel.objects.all()
    return render(request,'website/contact.html',{'brands': brands})


# =======Service======= #
def service(request):
    brands = BrandModel.objects.all().order_by('-created_at')
    
    return render(request,'website/service.html',{'brands': brands})


# =======Car showroom======= #
def cars(request):
    cars = (
        CarModel.objects
        .select_related('brand','category')
        .prefetch_related('images')
        .all().order_by('-created_at')
    )
    brands = BrandModel.objects.all()
    categories = CategoryModel.objects.all()
    
    # Search 
    search = request.GET.get('search','').strip()
    
    if search:
        cars = cars.filter(
            Q(name__icontains=search) |
            Q(brand__title__icontains=search) |
            Q(category__name__icontains=search) |
            Q(condition__icontains=search)
        )
    
    # Filter
    brand_id = request.GET.get('brand')
    category_id = request.GET.get('category')
    fuel_type = request.GET.get('fuel_type')
    
    if brand_id:
        cars = cars.filter(brand_id = brand_id)
        
    if category_id:
        cars = cars.filter(category_id = category_id)
        
    if fuel_type:
        cars = cars.filter(fuel_type = fuel_type)
    
    # Pagination
    paginator = Paginator(cars, 6)
    page_number = request.GET.get('page')
    cars = paginator.get_page(page_number)
    
    context = {
        'cars': cars,
        'brands': brands,
        'categories': categories,
        'fuel_choices': FUEL_CHOICES,
        'condition_choices': CONDITION_CHOICES,
        'transmission_choices': TRANSMISSION_CHOICES,
    }
    return render(request,'website/cars.html',context)


# =======Car Detail======= #
@login_required
def car_detail(request, car_id):
    car = get_object_or_404(
        CarModel.objects
        .select_related('brand','category')
        .prefetch_related('images'), 
        id = car_id
        )
    related_cars = (
        CarModel.objects
        .select_related('brand','category')
        .prefetch_related('images')
        .exclude(id = car_id)
        .filter(category= car.category)
        .order_by('-created_at')[:4]
    )
    context = {
        'car': car,
        'related_cars': related_cars,
    }
    return render(request,'website/car_detail.html',context)


# =======Sparepart======= #
def spareparts(request):
    spareparts = (
        SparepartModel.objects
        .select_related('brand','category')
        .prefetch_related('images')
        .all().order_by('-created_at')
    )
    brands = BrandModel.objects.all()
    partcategories = PartCategoryModel.objects.all()
    
    # Filter
    brand_id = request.GET.get('brand')
    category_id = request.GET.get('partcategory')
    
    if brand_id:
        spareparts = spareparts.filter(brand_id = brand_id)
        
    if category_id:
        spareparts = spareparts.filter(category_id = category_id)
    
    # Pagination
    paginator = Paginator(spareparts, 6)
    page_number = request.GET.get('page')
    spareparts = paginator.get_page(page_number)
    
    context = {
        'spareparts': spareparts,
        'brands': brands,
        'partcategories': partcategories,
    }
    return render(request,'website/spareparts.html',context)


# =======Sparepart Detail======= #
@login_required
def sparepart_detail(request,sp_id): 
    sparepart = get_object_or_404(
        SparepartModel.objects
        .select_related('brand','category')
        .prefetch_related('images'),
        id = sp_id
    )
    related_spareparts = (
        SparepartModel.objects
        .select_related('brand','category')
        .prefetch_related('images')
        .exclude(id = sp_id)
        .filter(category = sparepart.category)
        .order_by('-created_at')[:3]
    )
    context = {
        'sparepart': sparepart,
        'related_spareparts': related_spareparts,
    }
    return render(request,'website/sparepart_detail.html',context)


# =======Account======= #
def account(request):
    
    if request.user.is_authenticated:
        return render(request, 'errorpage.html', status=403)
    
    return render(request,'website/account.html')


# =======Blog======= #
def blog(request):
    blogs = BlogModel.objects.all().order_by('-created_at')
    
    # Search
    search = request.GET.get('search','').strip()
    if search:
        blogs = blogs.filter(
            Q(title__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(blogs, 4)
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    
    recent_blogs = BlogModel.objects.order_by('-created_at')[:3]
    
    context = {
        'blogs': blogs,
        'recent_blogs': recent_blogs,
    }
    return render(request,'website/blog.html',context)


# =======Blog Detail======= #
@login_required
def blog_detail(request,blog_id):
    blog = get_object_or_404(BlogModel, id = blog_id)
    recent_blogs = BlogModel.objects.order_by('-created_at')[:3]
        
    context = {
        'blog': blog,
        'recent_blogs': recent_blogs,
    }
    return render(request,'website/blog_detail.html',context)


#===============Profile===============#
@login_required
def user_pf(request):
    
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'errorpage.html', status=403)
    
    profile, created = UserProfileModel.objects.get_or_create(user = request.user)
    
    orders = (
        OrderModel.objects
        .filter(user = request.user)
        .prefetch_related('items__sparepart')
        .order_by('-created_at')
        )
    
    for order in orders:
        for item in order.items.all():
            item.subtotal = item.price * item.quantity
            
    context = {
        'profile': profile,
        'orders': orders,
    }
    
    return render(request,'website/user_pf.html',context)


@login_required
def edit_user_pf(request):
    
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'errorpage.html', status=403)
    
    profile, created = UserProfileModel.objects.get_or_create(user = request.user )
    
    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        
        if profile_image:
            
            if profile.profile_image:
                profile.profile_image.delete(save=False)
                
            profile.profile_image = profile_image
            profile.save()
            messages.success(request,'Profile image has been updated successfully.')
            
        return redirect('user_pf')
    return redirect('user_pf')


#===========My Cart=============#
@login_required
def cart(request):
    
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'errorpage.html', status=403)
    
    cart, created = CartModel.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('sparepart')

    total = 0

    for item in cart_items:
        item.subtotal = item.sparepart.price * item.quantity
        total += item.sparepart.price * item.quantity

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'website/cart.html', context)


#================Add to cart=================#
@login_required
@require_POST
def add_to_cart(request,sp_id):
    
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'errorpage.html', status=403)
    
    sparepart = get_object_or_404(SparepartModel, id = sp_id)
    
    # Quantity Check
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        messages.error(request, 'Please enter a valid quantity.')
        return redirect('sparepart_detail', sp_id=sparepart.id)

    if quantity < 1:
        messages.error(request, 'Quantity must be at least 1.')
        return redirect('sparepart_detail', sp_id=sparepart.id)

    if quantity > sparepart.stock:
        messages.error(request, f'Only {sparepart.stock} pcs are available in stock.')
        return redirect('sparepart_detail', sp_id=sparepart.id)
    
    cart, created = CartModel.objects.get_or_create(user = request.user)
    cart_item, created = CartItemModel.objects.get_or_create(
        cart = cart,
        sparepart = sparepart,
    )
    
    if created:
        cart_item.quantity = quantity
    else:
        if cart_item.quantity + quantity > sparepart.stock:
            messages.error(request,f'Only {sparepart.stock} pcs are available in stock.')
            return redirect('sparepart_detail', sp_id = sparepart.id)
        
        cart_item.quantity += quantity
        
    cart_item.save()
    messages.success(request,f'{sparepart.name} has been added to your cart')
    
    return redirect('spareparts')
        
        
#============Remove from cart=================#
@login_required
@require_POST
def remove_from_cart(request,sp_id):
    
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'errorpage.html', status=403)
    
    cart_item = get_object_or_404(CartItemModel, id = sp_id, cart__user = request.user )
    sparepart_name = cart_item.sparepart.name 
    
    cart_item.delete()
    
    messages.success(request, f'{sparepart_name} has been removed from your cart.')
    
    return redirect('cart')


#==============Orders===============#
@login_required
def orders(request):
    
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'errorpage.html', status=403)
    
    cart, created = CartModel.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('sparepart')

    if not cart_items.exists():
        messages.error(request,'Your cart is empty.')
        return redirect('spareparts')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name','').strip()
        last_name = request.POST.get('last_name','').strip()
        address = request.POST.get('address','').strip()
        phone = request.POST.get('phone','').strip()
        email = request.POST.get('email','').strip()
        
        if not first_name or not last_name or not address or not phone or not email:
            messages.error(request,'Please fill in all required fields.')
            return redirect('orders')
        
        if not phone.isascii() or not phone.isdecimal() or len(phone) > 11:
            messages.error(request, 'Please enter a valid phone number.')
            return redirect('orders')
        
        if email.lower() != request.user.email.lower():
            messages.error(request,'Wrong email,please ckeck your email address from your profile.')
            return redirect('orders')
                
        with transaction.atomic():
            
            locked_items = []
            
            for item in cart_items.order_by('sparepart_id'):
                sparepart = (
                    SparepartModel.objects
                    .select_for_update()
                    .get( id = item.sparepart_id )
                )
                
                if item.quantity > sparepart.stock:
                    messages.error(request,f'Only {sparepart.stock}pcs of {sparepart.name} are available in stock.')
                    return redirect ('orders')
                
                locked_items.append((item,sparepart))
                
            total = 0 
            
            for item,sparepart in locked_items:
                total += sparepart.price * item.quantity
                
            order = OrderModel.objects.create(
                user = request.user,
                first_name = first_name,
                last_name = last_name,
                address = address,
                phone = phone,
                email = email,
                total_amount = total,
                status = 'pending',
            )
            
            for item,sparepart in locked_items:

                OrderItemModel.objects.create(
                    order = order,
                    sparepart = sparepart,
                    quantity = item.quantity,
                    price = sparepart.price,
                )
                
                sparepart.stock -= item.quantity
                sparepart.save(update_fields = ['stock'])
            
            cart.items.all().delete()
            
        messages.success(request,'You order has been placed successfully.')
        return redirect('user_pf')
    

    total = 0

    for item in cart_items:
        item.subtotal = item.sparepart.price * item.quantity
        total += item.subtotal

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'website/orders.html', context)  