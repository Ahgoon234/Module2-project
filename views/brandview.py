from django.shortcuts import render,redirect,get_object_or_404
from lore.models import BrandModel,CarModel,SparepartModel
from django.contrib.auth.decorators import login_required
from django.contrib import messages


#==============Brand List===============#
@login_required
def brand_list(request):
    
    if not request.user.has_perm('lore.view_brandmodel'):
        return render(request, 'errorpage.html', status=403)
    
    brands = BrandModel.objects.all().order_by('-created_at')
    
    #Search
    search = request.GET.get('search','').strip()
    
    if search:
        brands = brands.filter( title__icontains=search )
    
    context ={
        'brands': brands ,
        'page_title': 'Brands'
    }
    return render(request,'admin/brand_list.html',context)


#==============Brand Create================#
@login_required
def brand_create(request):
    
    if not request.user.has_perm('lore.add_brandmodel'):
        return render(request, 'errorpage.html', status=403)
    
    if request.method == 'POST':        
        
        title = request.POST.get('title')
        logo = request.FILES.get('logo')  
        
        if not title or not logo:
            messages.error(request,'Please fill all fields.')
            return redirect('brand_list')
        
        BrandModel.objects.create(
            title = title,
            logo = logo,
        )
        messages.success(request,'A New Brand has been created successfully.')
        return redirect('brand_list')
    
    return redirect('brand_list')


#==============Brand Update===============#
@login_required
def brand_update(request, brand_id):
    
    if not request.user.has_perm('lore.change_brandmodel'):
        return render(request, 'errorpage.html', status=403)
    
    brand = get_object_or_404(BrandModel, id=brand_id)
    
    if request.method == 'POST':
        brand.title = request.POST.get('title')   
        logo = request.FILES.get('logo')
        
        if logo: 
                       
            if brand.logo:
                brand.logo.delete(save=False)
            brand.logo = logo
            
        brand.save()
        messages.success(request,f'"{brand.title}" has been updated successfully.')
        return redirect('brand_list')
    
    return redirect('brand_list')


#===================Brand Delete==================#
@login_required
def brand_delete(request,brand_id):
    
    if not request.user.has_perm('lore.delete_brandmodel'):
        return render(request, 'errorpage.html', status=403)
    
    brand = get_object_or_404(BrandModel, id = brand_id)    
    
    if request.method == 'POST':
        
        brand_title = brand.title
        
        if CarModel.objects.filter(brand=brand).exists() or SparepartModel.objects.filter(brand=brand).exists():
            messages.error(request, 'This brand is being used by cars or spareparts.')
            return redirect('brand_list')
        
        if brand.logo:
            brand.logo.delete(save=False)       
            
        brand.delete()       
        messages.success(request,f'"{brand_title}" has been deleted from the list.')
        return redirect('brand_list')
    
    return redirect('brand_list')
