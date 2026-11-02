"""
URL configuration for module2_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from views.pageview import *
from views.carview import *
from views.categoryview import *
from views.sparepartview import *
from views.dashboardview import *
from views.brandview import *
from views.partcategoryview import *
from views.blogview import *
from views.contactmsgview import *
from views.auth_view import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ag_management_site/', admin.site.urls),
    
    #=================Auth View===================#
    path('register/', register_view, name='register_view'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('resend_otp/', resend_otp, name='resend_otp'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    
    #=============================Website view=================================#
    path('',index,name='home'),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
    path('service/',service,name='service'),
    path('cars/',cars,name='cars'),
    path('car_detail/<uuid:car_id>/',car_detail,name='car_detail'),
    path('spareparts/',spareparts,name='spareparts'),
    path('sparepart_detail/<uuid:sp_id>/',sparepart_detail,name='sparepart_detail'),
    path('account/',account,name='account'),
    path('blog/',blog,name='blog'),
    path('blog_detail/<uuid:blog_id>/',blog_detail,name='blog_detail'),
    
    #==================Add to Cart View==================#
    path('cart/',cart,name='cart'),
    path('add_to_cart/<uuid:sp_id>/',add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<uuid:sp_id>/',remove_from_cart,name='remove_from_cart'),
    path('orders/',orders,name='orders'),
    
    #================Profile image view=================#
    path('user_pf/',user_pf,name='user_pf'),
    path('edit_user_pf/',edit_user_pf,name='edit_user_pf'),
    
    #===============================Dashboard view====================================#
    path('dashboard/',dashboard,name='dashboard'),
    
    #==================Admin Profile===============#
    path('admin_pf/',admin_pf,name='admin_pf'),
    path('user_control/<int:user_id>/',user_control,name='user_control'),
    
    #==============Order view==============#
    path('order_list/',order_list,name='order_list'),
    path('order_update/<uuid:order_id>/',order_update,name='order_update'),
    
    #==============Brand view=============#
    path('brand_list',brand_list,name='brand_list'),
    path('brand_create/',brand_create,name='brand_create'),
    path('brand_update/<uuid:brand_id>/',brand_update,name='brand_update'),
    path('brand_delete/<uuid:brand_id>/',brand_delete,name='brand_delete'),
    
    #=============Category veiw============#
    path('category_list/',category_list,name='category_list'),
    path('category_create/',category_create,name='category_create'),
    path('category_update/<uuid:category_id>/',category_update,name='category_update'),
    path('category_delete/<uuid:category_id>/',category_delete,name='category_delete'),
    
    #================Car veiw==================#
    path('car_list/',car_list,name='car_list'),
    path('car_create/',car_create,name='car_create'),
    path('car_update/<uuid:car_id>/',car_update,name='car_update'),
    path('car_delete/<uuid:car_id>/',car_delete,name='car_delete'),
    
    #==============PartCategory veiw==============#
    path('partcategory_list/',partcategory_list,name='partcategory_list'),
    path('partcategory_create/',partcategory_create,name='partcategory_create'),
    path('partcategory_update/<uuid:pc_id>/',partcategory_update,name='partcategory_update'),
    path('partcategory_delete/<uuid:pc_id>/',partcategory_delete,name='partcategory_delete'),
    
    #================Sparepart veiw====================#
    path('sparepart_list/',sparepart_list,name='sparepart_list'),
    path('sparepart_create/',sparepart_create,name='sparepart_create'),
    path('sparepart_update/<uuid:sp_id>/',sparepart_update,name='sparepart_update'),
    path('sparepart_delete/<uuid:sp_id>/',sparepart_delete,name='sparepart_delete'),
    
    #===================Blog veiw=====================#
    path('blog_list/',blog_list,name='blog_list'),
    path('blog_create/',blog_create,name='blog_create'),
    path('blog_update/<uuid:blog_id>/',blog_update,name='blog_update'),
    path('blog_delete/<uuid:blog_id>/',blog_delete,name='blog_delete'),
    
    #================ContactMessage veiw==================#
    path('contactmsg_list/',contactmsg_list,name='contactmsg_list'),
    path('contactmsg_create/',contactmsg_create,name='contactmsg_create'),
    path('contactmsg_click/<uuid:msg_id>/',contactmsg_click,name='contactmsg_click'),
    path('contactmsg_delete/<uuid:msg_id>/',contactmsg_delete,name='contactmsg_delete'),
    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
