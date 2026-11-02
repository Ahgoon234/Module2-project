from django.shortcuts import render,get_object_or_404,redirect
from lore.models import CategoryModel,BrandModel,CarModel,SparepartModel,PartCategoryModel,BlogModel,OrderModel,UserProfileModel,CONDITION_CHOICES,FUEL_CHOICES,TRANSMISSION_CHOICES
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import CharField
from django.db.models.functions import Cast


#======================Dashboard========================#
@login_required
def dashboard (request):
    
    if not request.user.is_staff and not request.user.is_superuser:
        return render(request, 'errorpage.html', status=403)
    
    cars = CarModel.objects.all().order_by('-created_at')
    brands = BrandModel.objects.all().order_by('-created_at')
    categories = CategoryModel.objects.all().order_by('-created_at')
    spareparts = SparepartModel.objects.all().order_by('-created_at')
    partcategories = PartCategoryModel.objects.all().order_by('-created_at')
    blogs = BlogModel.objects.all().order_by('-created_at')
    
    context ={
        'cars': cars,   
        'brands': brands,
        'categories': categories,
        'spareparts': spareparts,
        'partcategories': partcategories,
        'blogs': blogs,
        'condition_choices': CONDITION_CHOICES,
        'fuel_choices': FUEL_CHOICES,
        'transmission_choices': TRANSMISSION_CHOICES,
        'page_title':'Dashboard',
    }
    return render(request,'admin/dashboard.html',context)


#=================Admin profile======================#
@login_required
def admin_pf(request):
    
    if not request.user.is_staff and not request.user.is_superuser:
        return render(request, 'errorpage.html', status=403)
    
    profile, created = UserProfileModel.objects.get_or_create(user = request.user)
    
    if request.method == 'POST':
        
        profile_image = request.FILES.get('profile_image')
        
        if profile_image:
            
            if profile.profile_image:
                profile.profile_image.delete(save=False)
                
            profile.profile_image = profile_image
            
            profile.save()
            messages.success(request,'Profile Photo updated successfully.')
            return redirect('admin_pf')
        
    users = User.objects.all().order_by('-date_joined')
    
    context = {
        'profile': profile,
        'users': users,
        'user_count': users.count()
    }
    
    return render(request,'admin/admin_pf.html',context)

#===================User Table Actions=================#
@login_required
@require_POST
def user_control(request, user_id):
    
    if not request.user.is_superuser:
        return render(request,'errorpage.html', status=403)
    
    user = get_object_or_404(User, id = user_id)
    
    if user.is_superuser:
        messages.error(request,'Superuser account cannot be deactivated.')
        return redirect('admin_pf')
    
    user.is_active = not user.is_active
    user.save(update_fields=['is_active'])
    
    if user.is_active:
        messages.success(request,f'{user.username} has been activated successfully.')
        
    else:
        messages.success(request,f'{user.username} has been deactivated successfully.')
        
    return redirect('admin_pf')

#==================Order_List=====================#
@login_required
def order_list(request):
    
    if not request.user.has_perm('lore.view_ordermodel'):
        return render(request, 'errorpage.html', status=403)
    
    orders = (
        OrderModel.objects
        .select_related('user')
        .prefetch_related('items__sparepart')
        .order_by('-created_at')
    )
    
    #Search 
    search = request.GET.get('search','').strip()
    search_id = search.replace('-','')
    
    if search_id:
        orders = (
            orders.annotate(
                order_id_text = Cast('id',output_field=CharField())
            ).filter(
                order_id_text__istartswith = search_id
                )
            )
        
    #Filter 
    status = request.GET.get('status','').strip()
    
    if status in ['pending','confirmed','cancelled']:
        orders = orders.filter(status = status)

    for order in orders:
        for item in order.items.all():
            item.subtotal = item.price * item.quantity

    context = {
        'orders': orders,
        'order_count': orders.count(),
        'cancel_reason_choices': OrderModel.CANCEL_REASON_CHOICES,
        'status_choices': OrderModel.STATUS_CHOICES,
        'search': search,
        'status': status,
        'page_title':'Orders',
    }

    return render(request, 'admin/order_list.html', context)


#================Order Update====================#
@login_required
def order_update(request,order_id):
    
    if not request.user.has_perm('lore.change_ordermodel'):
        return render(request, 'errorpage.html', status=403)
    
    order = get_object_or_404(OrderModel, id = order_id)
    order_code = order.id.hex[:12].upper()
    
    if request.method != 'POST':
        return redirect('order_list')
    
    action = request.POST.get('action')
    
    if action == 'confirm':
        
        if order.status != 'pending':
            messages.error(request,'This order has already been Cancelled or Confirmed.')
            return redirect('order_list')
        
        order.status = 'confirmed'
        order.cancel_reason = None
        order.save()
        
        messages.success(request,f'Order #{order_code} has been confirmed.')
        return redirect('order_list')
    
    if action == 'cancel':
        
        cancel_reason = request.POST.get('cancel_reason')
        valid_reasons = dict(OrderModel.CANCEL_REASON_CHOICES)
        
        if cancel_reason not in valid_reasons:
            messages.error(request,'Please select a valid reason to cancel this order.')
            return redirect('order_list')
        
        if order.status != 'pending':
            messages.error(request,'This order has already been Cancelled or Confirmed.')
            return redirect('order_list')
        
        with transaction.atomic():
            order_items = order.items.select_related('sparepart')
            
            for item in order_items:
                
                sparepart = item.sparepart
                sparepart.stock += item.quantity
                sparepart.save()
                
            order.status = 'cancelled'
            order.cancel_reason = cancel_reason
            order.save()
            
        messages.success(request,f'Order #{order_code} has been cancelled.')
        return redirect('order_list')
        
    messages.error(request,'Invalid order action.')
    return redirect('order_list')