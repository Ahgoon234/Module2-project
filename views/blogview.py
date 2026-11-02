from django.shortcuts import render,redirect,get_object_or_404
from lore.models import BlogModel
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#=====================Blog List=====================#
@login_required
def blog_list(request):
    
    if not request.user.has_perm('lore.view_blogmodel'):
        return render(request, 'errorpage.html', status=403)
    
    blogs = BlogModel.objects.all().order_by('-created_at')
    
    #Search
    search = request.GET.get('search','').strip()
    
    if search:
        blogs = blogs.filter( title__icontains=search )
    
    
    context = {
        'blogs': blogs,
        'page_title': 'Blogs',
    }
    return render(request,'admin/blog_list.html',context)


#=====================Blog Create=====================#
@login_required
def blog_create(request):
    
    if not request.user.has_perm('lore.add_blogmodel'):
        return render(request, 'errorpage.html', status=403)
    
    if request.method == 'POST':
        
        title = request.POST.get('title')
        content = request.POST.get('content')
        thumbnail = request.FILES.get('thumbnail')
        
        if not title or not content or not thumbnail:
            messages.error(request,'Please fill all fields.')
            return redirect('blog_list')
        
        BlogModel.objects.create(
            title = title,
            content = content,
            thumbnail = thumbnail
        )
        messages.success(request,'A New Blog has been created successfully.')
        return redirect('blog_list')
    
    return redirect('blog_list')


#=====================Blog Update=====================#
@login_required
def blog_update(request,blog_id):
    
    if not request.user.has_perm('lore.change_blogmodel'):
        return render(request, 'errorpage.html', status=403)
    
    blog = get_object_or_404(BlogModel, id = blog_id)
    
    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        thumbnail = request.FILES.get('thumbnail')
        
        
        if thumbnail:
            
            if blog.thumbnail:
                blog.thumbnail.delete(save=False)
            blog.thumbnail = thumbnail
            
        blog.save()
        messages.success(request,f'"{blog.title}" has been updated successfully.')
        return redirect('blog_list')
    
    return redirect('blog_list')


#=====================Blog Delete=====================#
@login_required
def blog_delete(request,blog_id):
    
    if not request.user.has_perm('lore.delete_blogmodel'):
        return render(request, 'errorpage.html', status=403)
    
    blog = get_object_or_404(BlogModel, id = blog_id)
    
    if request.method == 'POST':
        
        blog_title = blog.title
        
        if blog.thumbnail:
            blog.thumbnail.delete(save=False)
        
        blog.delete()
        messages.success(request,f'"{blog_title}" has been deleted from the list.')
        return redirect('blog_list')
    
    return redirect('blog_list')