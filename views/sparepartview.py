from django.shortcuts import render,redirect,get_object_or_404
from lore.models import SparepartModel,PartCategoryModel,PartImageModel,BrandModel,OrderItemModel
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal, InvalidOperation


#==================Sparepart List==================#
@login_required
def sparepart_list(request):
    
    if not request.user.has_perm('lore.view_sparepartmodel'):
        return render(request, 'errorpage.html', status=403)
    
    spareparts = (
        SparepartModel.objects
        .select_related('brand','category')
        .prefetch_related('images')
        .all().order_by('-created_at')
    )   
    brands = BrandModel.objects.all()
    partcategories = PartCategoryModel.objects.all()   
    
    #Search
    search = request.GET.get('search','').strip()
    
    if search:
        spareparts = spareparts.filter( name__icontains=search )
        
    #Filter
    brand_id = request.GET.get('brand')
    category_id = request.GET.get('category')
    
    if brand_id:
        spareparts = spareparts.filter(brand_id = brand_id)
        
    if category_id:
        spareparts = spareparts.filter(category_id = category_id)
     
    context = {
        'spareparts': spareparts,
        'brands': brands,
        'partcategories': partcategories,
        'page_title': 'Spareparts',
    }    
    return render(request,'admin/sparepart_list.html',context)


#==================Sparepart Create==================#
@login_required
def sparepart_create(request):    
    
    if not request.user.has_perm('lore.add_sparepartmodel'):
        return render(request, 'errorpage.html', status=403)
    
    if request.method == 'POST':
        
        name = request.POST.get('name')
        brand_id = request.POST.get('brand')
        category_id = request.POST.get('partcategory')
        price = request.POST.get('price')
        stock = request.POST.get('stock') 
        description = request.POST.get('description')
        thumbnail = request.FILES.get('thumbnail') 
        
        if not all([name, brand_id, category_id, price, stock, description, thumbnail]):
            messages.error(request,'Please fill all fields.')
            return redirect('sparepart_list')
        
        # Price check
        try:
            price = Decimal(price)
            
            if not price.is_finite() or price <= 0:
                messages.error(request,'Price must be greater than 0.')
                return redirect('sparepart_list')
            
        except(InvalidOperation, ValueError):
            messages.error(request,'Please enter a valid amount.')
            return redirect('sparepart_list')
        
        # Stock check
        if not stock.isascii() or not stock.isdecimal() or int(stock) <= 0:
            messages.error(request,'Stock must be Positive Whole Number(1,2,3,...)')
            return redirect('sparepart_list')
        
        stock = int(stock)
           
        sparepart = SparepartModel.objects.create(
            name = name,
            brand_id = brand_id,
            category_id = category_id or None,
            price = price,
            stock = stock or 0,
            description = description,
            thumbnail = thumbnail,
        )        
        
        gallery_images = request.FILES.getlist('gallery_images')        
        for image in gallery_images:
            PartImageModel.objects.create(
                image = image,
                sparepart = sparepart,
            )            
        
        messages.success(request,'A New Sparepart has been added to the list.')
        return redirect('sparepart_list')    
        
    return redirect('sparepart_list')


#==================Sparepart Update==================#
@login_required
def sparepart_update(request,sp_id):
    
    if not request.user.has_perm('lore.change_sparepartmodel'):
        return render(request, 'errorpage.html', status=403)
    
    sparepart = get_object_or_404(SparepartModel, id = sp_id) 
       
    if request.method == 'POST':
        
        name = request.POST.get('name')
        brand_id = request.POST.get('brand')
        category_id = request.POST.get('partcategory')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')        
        thumbnail = request.FILES.get('thumbnail')    
        
        if not all([name, brand_id, category_id, price, stock, description]):
            messages.error(request,'Please fill all fields')  
            return redirect('sparepart_list')
        
        # Price check
        if price:
            try:
                price = Decimal(price)
                
                if not price.is_finite() or price <= 0:
                    messages.error(request,'Price must be greater than 0.')
                    return redirect('sparepart_list')
                
            except(InvalidOperation, ValueError):
                messages.error(request,'Please enter a valid amount.')
                return redirect('sparepart_list')
            
        # Stock check
        if stock:
            if not stock.isascii() or not stock.isdecimal() or int(stock) <= 0:
                messages.error(request,'Stock must be Positive Whole Number(1,2,3,...)')
                return redirect('sparepart_list')
            
        brand = get_object_or_404(BrandModel, id=brand_id)
        category = get_object_or_404(PartCategoryModel, id=category_id)
            
        sparepart.name = name
        sparepart.brand = brand
        sparepart.category = category
        sparepart.price = price
        sparepart.stock = stock
        sparepart.description = description
          
        if thumbnail:
            
            if sparepart.thumbnail:
                sparepart.thumbnail.delete(save=False) 
                               
            sparepart.thumbnail = thumbnail    
                
        sparepart.save()        
        
        delete_images = request.POST.getlist('delete_images')        
        for image_id in delete_images:
            
            image = PartImageModel.objects.filter(
                id = image_id,
                sparepart = sparepart
            ).first()    
                    
            if image:
                if image.image:
                    image.image.delete(save=False)                                       
                image.delete()        
                        
        gallery_images = request.FILES.getlist('gallery_images')        
        for image in gallery_images:
            
            PartImageModel.objects.create(
                image = image,
                sparepart = sparepart,
            )           
            
        messages.success(request,f'"{sparepart.name}" has been updated successfully.')
        return redirect('sparepart_list') 
       
    return redirect('sparepart_list')
        
        
#==================Sparepart Delete==================#
@login_required
def sparepart_delete(request,sp_id):
    
    if not request.user.has_perm('lore.delete_sparepartmodel'):
        return render(request, 'errorpage.html', status=403)
    
    sparepart = get_object_or_404(SparepartModel, id = sp_id)    
    
    if request.method == 'POST':   
        
        sparepart_name = sparepart.name  
        
        if OrderItemModel.objects.filter(sparepart = sparepart).exists():
            messages.error(request,'Cannot delete this sparepart because it exists in order history.')
            return redirect('sparepart_list')   
        
        if sparepart.thumbnail:
            sparepart.thumbnail.delete(save=False) 
                       
        for image in sparepart.images.all():
            if image.image:
                image.image.delete() 
                       
        sparepart.delete()        
        messages.success(request,f'{sparepart_name} has been deleted from the list.')
        return redirect('sparepart_list')  
     
    return redirect('sparepart_list')