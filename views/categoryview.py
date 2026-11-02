from django.shortcuts import render,redirect,get_object_or_404
from lore.models import CategoryModel,CarModel
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#==============Category List==============#
@login_required
def category_list(request):
    
    if not request.user.has_perm('lore.view_categorymodel'):
        return render(request, 'errorpage.html', status=403)
    
    categories = CategoryModel.objects.all().order_by('-created_at')
    
    #Search
    search = request.GET.get('search','').strip()
    
    if search:
        categories = categories.filter( name__icontains=search )
    
    context = {
        'categories': categories,
        'page_title': 'Categories'
    }
    
    return render(request,'admin/category_list.html',context)


#===============Category Create============#
@login_required
def category_create(request):
    
    if not request.user.has_perm('lore.add_categorymodel'):
        return render(request, 'errorpage.html', status=403)
    
    if request.method == 'POST':
        
        name = request.POST.get('name')
        image = request.FILES.get('image')   
        
        if not name or not image:
            messages.error(request,'Please fill all fields.')
            return redirect('category_list')
            
        CategoryModel.objects.create(
            name = name,
            image = image,
        )
        messages.success(request,'A New Category has been created successfully.')
        return redirect('category_list')   
    
    return redirect('category_list')


#================Category Update==================#    
@login_required
def category_update(request,category_id):
    
    if not request.user.has_perm('lore.change_categorymodel'):
        return render(request, 'errorpage.html', status=403)
    
    category = get_object_or_404(CategoryModel, id = category_id)  
          
    if request.method == 'POST':
        
        name = request.POST.get('name')   
        image = request.FILES.get('image')
        
        if not name:
            messages.error(request,'Please fill all fields.')
            return redirect('category_list')
        
        category.name = name
        
        if image:
            if category.image:
                category.image.delete(save=False)            
            category.image = image 
                       
        category.save()        
        messages.success(request,f'{category.name} has been updated successfully.')
        return redirect('category_list')   
     
    return redirect('category_list')


#=================Category Delete==================#
@login_required
def category_delete(request,category_id):
    
    if not request.user.has_perm('lore.delete_categorymodel'):
        return render(request, 'errorpage.html', status=403)
    
    category = get_object_or_404(CategoryModel, id = category_id)    
    
    if request.method == 'POST':
        
        category_name = category.name
        
        if CarModel.objects.filter(category = category).exists():
            messages.error(request, 'Cannot delete this category because it is being used by cars.')
            return redirect('category_list')
        
        if category.image:
            category.image.delete(save=False) 
                       
        category.delete()        
        messages.success(request,f'{category_name} has been deleted from the list.')
        return redirect('category_list')
    
    return redirect('category_list')
    
