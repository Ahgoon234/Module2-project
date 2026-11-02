from django.shortcuts import render,redirect,get_object_or_404
from lore.models import ContactMsgModel
from django.contrib.auth.decorators import login_required
from django.contrib import messages


#===============Contact Message List==============#
@login_required
def contactmsg_list(request):
    
    if not request.user.is_superuser:
        return render(request, 'errorpage.html', status=403)
    
    contactmsgs = ContactMsgModel.objects.all().order_by('-created_at')
    
    #Search
    search = request.GET.get('search','').strip()
    
    if search:
        contactmsgs = contactmsgs.filter( name__icontains=search )
    
    context = {
        'contactmsgs': contactmsgs,
        'page_title': 'ContactMessages'
    }
    return render(request,'admin/contactmsg.html',context)


#===============Contact Message Create==============#
@login_required
def contactmsg_create(request):
    
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'errorpage.html', status=403)
    
    if request.method == 'POST':
        
        name = request.POST.get('name','').strip()
        email = request.POST.get('email','').strip()
        phone = request.POST.get('phone','').strip()
        message = request.POST.get('message','').strip()
        
        if not all([name, email, phone, message]):
            messages.error(request,'Please fill all fields.')
            return redirect('contact')
        
        if email.lower() != request.user.email.lower():
            messages.error(request,'Wrong email.Please check your email from your profile.')
            return redirect('contact')
        
        if not phone.isdigit():
            messages.error(request,'Please fill a valid Phone Number(09123456789).')
            return redirect('contact')
        
        ContactMsgModel.objects.create(
            name = name,
            email = email,
            phone = phone,
            message = message,
            is_read = False
        )
        messages.success(request,'Your Message has been sent to admin successfully.')
        return redirect('contact')
    
    return redirect('contact')


#===============Contact Message Click==============#
@login_required
def contactmsg_click(request, msg_id):
    
    if not request.user.is_superuser:
        return render(request, 'errorpage.html', status=403)
    
    contactmsg = get_object_or_404(ContactMsgModel, id = msg_id)
    
    if request.method == 'POST':
        
        contactmsg_name = contactmsg.name
        
        contactmsg.is_read = not contactmsg.is_read
        
        contactmsg.save(update_fields=['is_read'])
        
        status = 'read' if contactmsg.is_read else 'unread'
        messages.success(request,f'A Message from {contactmsg_name} has been marked as {status}.')
        return redirect('contactmsg_list')
    
    return redirect('contactmsg_list')
    

#===============Contact Message Delete==============#
@login_required
def contactmsg_delete(request, msg_id):
    
    if not request.user.is_superuser:
        return render(request, 'errorpage.html', status=403)
    
    contactmsg = get_object_or_404(ContactMsgModel, id = msg_id)
    
    if request.method == 'POST':
        
        contactmsg_name = contactmsg.name
        
        contactmsg.delete()
        messages.success(request,f'A Message from {contactmsg_name} has been deleted from the list.')
        return redirect('contactmsg_list')
    
    return redirect('contactmsg_list')