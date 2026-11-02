from django.shortcuts import render,redirect,get_object_or_404
from lore.models import PartCategoryModel,SparepartModel
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#==================PartCategory List================#
@login_required
def partcategory_list(request):
    
    if not request.user.has_perm('lore.view_partcategorymodel'):
        return render(request, 'errorpage.html', status=403)
    
    partcategories = PartCategoryModel.objects.all().order_by('-created_at')
    
    #Search
    search = request.GET.get('search','').strip()
    
    if search:
        partcategories = partcategories.filter( name__icontains=search )
    
    
    context = {
        'partcategories': partcategories,
        'page_title': 'Sparepart Categories',
    }
    return render(request,'admin/partcategory_list.html',context)


#==================PartCategory Create================#
@login_required
def partcategory_create(request):
    
    if not request.user.has_perm('lore.add_partcategorymodel'):
        return render(request, 'errorpage.html', status=403)
    
    if request.method == 'POST':
        
        name = request.POST.get('name')
        
        if not name:
            messages.error(request,'Please fill Name properly.')
            return redirect('partcategory_list')
        
        PartCategoryModel.objects.create(
            name = name,
        )
        messages.success(request,'A New Partcategory has been created successfully.')
        return redirect('partcategory_list')
    
    return redirect('partcategory_list')


#==================PartCategory Update================#
@login_required
def partcategory_update(request,pc_id):
    
    if not request.user.has_perm('lore.change_partcategorymodel'):
        return render(request, 'errorpage.html', status=403)
    
    partcategory = get_object_or_404(PartCategoryModel, id = pc_id)
    
    if request.method == 'POST':
        
        name = request.POST.get('name')
        
        if not name:
            messages.error(request,'Please fill name.')
            return redirect('partcategory_list')
        
        partcategory.name = name 
        
        partcategory.save()
        messages.success(request,f'{partcategory.name} has been updated successfully.')
        return redirect('partcategory_list')
    
    return redirect('partcategory_list')


#==================PartCategory Delete================#
@login_required
def partcategory_delete(request,pc_id):
    
    if not request.user.has_perm('lore.delete_partcategorymodel'):
        return render(request, 'errorpage.html', status=403)
    
    partcategory = get_object_or_404(PartCategoryModel, id = pc_id)   
    
    if request.method == 'POST':
        
        partcategory_name = partcategory.name
        
        if SparepartModel.objects.filter(category=partcategory).exists():
            messages.error(request, 'Cannot delete this category because it is being used by spareparts.')
            return redirect('partcategory_list')
        
        partcategory.delete()
        messages.success(request,f'{partcategory_name} has been deleted successfully.')
        return redirect('partcategory_list')
    
    return redirect('partcategory_list')
