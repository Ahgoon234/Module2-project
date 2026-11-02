from django.shortcuts import render,get_object_or_404,redirect
from lore.models import CategoryModel,BrandModel,CarModel,CarImageModel,CONDITION_CHOICES,FUEL_CHOICES,TRANSMISSION_CHOICES
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal, InvalidOperation


#==================Car List=================#
@login_required
def car_list(request):
    
    if not request.user.has_perm('lore.view_carmodel'):
        return render(request, 'errorpage.html', status=403)
    
    cars = (
        CarModel.objects
        .select_related('brand','category')
        .prefetch_related('images')
        .all().order_by('-created_at')
    )
    brands = BrandModel.objects.all().order_by('title')
    categories = CategoryModel.objects.all().order_by('name')
    
    #Search
    search = request.GET.get('search','').strip()
    
    if search:
        cars = cars.filter( name__icontains=search )
        
    #Filter
    brand_id = request.GET.get('brand')
    category_id = request.GET.get('category')
    condition = request.GET.get('condition')    
    
    if brand_id:
        cars = cars.filter(brand_id = brand_id)
        
    if category_id:
        cars = cars.filter(category_id = category_id)
        
    if condition in [value for value, label in CONDITION_CHOICES]:
        cars = cars.filter(condition = condition)
    
    context = {
        'cars': cars,
        'brands': brands,
        'categories': categories,
        'condition_choices': CONDITION_CHOICES,
        'fuel_choices': FUEL_CHOICES,
        'transmission_choices': TRANSMISSION_CHOICES,
        'page_title':'Cars',
    }    
    return render(request,'admin/car_list.html',context)


#=================Car Create==================#
@login_required
def car_create(request):   
    
    if not request.user.has_perm('lore.add_carmodel'):
        return render(request, 'errorpage.html', status=403)
    
    if request.method == 'POST':       
         
        name = request.POST.get('name')
        brand_id = request.POST.get('brand')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        thumbnail = request.FILES.get('thumbnail')
        year = request.POST.get('year')
        mileage = request.POST.get('mileage')
        color = request.POST.get('color')
        fuel_type = request.POST.get('fuel_type')
        transmission = request.POST.get('transmission')
        engine = request.POST.get('engine')
        horsepower = request.POST.get('horsepower')
        description = request.POST.get('description')
        condition = request.POST.get('condition')
        is_featured = request.POST.get('is_featured') == 'on'  
        
        if not all([name, brand_id, category_id, price, stock, thumbnail, year, mileage, color, fuel_type, transmission, engine, horsepower, description, condition]):
            messages.error(request,'Please fill all fields.')
            return redirect('car_list')
        
        # Price check
        try:
            price = Decimal(price)
            
            if not price.is_finite() or price <= 0:
                messages.error(request,'Price must be greater than 0.')
                return redirect('car_list')
            
        except (InvalidOperation, ValueError):
            messages.error(request,'Please enter a valid amount.')
            return redirect('car_list')
        
        # Stock check 
        if not stock.isascii() or not stock.isdecimal() or int(stock) <= 0:
            messages.error(request,'Stock must be Positive Whole Number(1,2,3,..).')
            return redirect('car_list')
            
        stock = int(stock)
        
        # Horsepower check
        if not horsepower.isascii() or not horsepower.isdecimal() or int(horsepower) <= 0:
            messages.error(request, 'Horsepower must be a Positive Whole Number.')
            return redirect('car_list')

        horsepower = int(horsepower)
        
        # Year check
        if not year.isascii() or not year.isdecimal() or int(year) <= 0:
            messages.error(request,'Year must be Positive Whole Number(2019,2020,...).')
            return redirect('car_list')
        
        year = int(year)
        
        # Mileage Check
        if not mileage.isascii() or not mileage.isdecimal():
            messages.error(request, 'Mileage must be a Whole Number.')
            return redirect('car_list')

        mileage = int(mileage)
         
        car = CarModel.objects.create(
            name = name,
            brand_id = brand_id,
            category_id = category_id,
            price = price,
            stock = stock,
            thumbnail = thumbnail,
            year = year,
            mileage = mileage,
            color = color,
            fuel_type = fuel_type,
            transmission = transmission,
            engine = engine,
            horsepower = horsepower,
            description = description,
            condition = condition,
            is_featured = is_featured,
        )
        
        gallery_images = request.FILES.getlist('gallery_images')        
        for image in gallery_images:
            CarImageModel.objects.create(
                image = image,
                car = car,
            ) 

        messages.success(request,'A New Car has been added to the list.')
        return redirect('car_list')  
      
    return redirect('car_list')


#===============Car Update===============#
@login_required
def car_update(request,car_id):
    
    if not request.user.has_perm('lore.change_carmodel'):
        return render(request, 'errorpage.html', status=403)
    
    car = get_object_or_404(CarModel, id = car_id)    
    
    if request.method == 'POST':
        
        name = request.POST.get('name')
        brand_id = request.POST.get('brand')
        category_id = request.POST.get('category') 
        price = request.POST.get('price')
        stock = request.POST.get('stock') 
        year = request.POST.get('year')
        mileage = request.POST.get('mileage')
        color = request.POST.get('color')
        fuel_type = request.POST.get('fuel_type')
        transmission = request.POST.get('transmission')
        engine = request.POST.get('engine')
        horsepower = request.POST.get('horsepower')
        description = request.POST.get('description')
        condition = request.POST.get('condition')
        is_featured = request.POST.get('is_featured') == 'on'       
        thumbnail = request.FILES.get('thumbnail')
        
        if not all([name, brand_id, category_id, price, stock, year, mileage, color, fuel_type, transmission, engine, horsepower, description, condition]):
            messages.error(request,'Update failed.One of the fields seems to be blank.')
            return redirect('car_list')
        
        # Price check
        if price:
            try:
                price = Decimal(price)

                if not price.is_finite() or price <= 0:
                    messages.error(request,'Price must be greater than 0.')
                    return redirect('car_list')

            except (InvalidOperation, ValueError):
                messages.error(request,'Please enter a valid amount.')
                return redirect('car_list')
        
        # Stock check 
        if stock:
            if not stock.isascii() or not stock.isdecimal() or int(stock) <= 0:
                messages.error(request,'Stock must be Positive Whole Number(1,2,3,..).')
                return redirect('car_list')

            stock = int(stock)
        
        # Horsepower Check
        if horsepower:
            if not horsepower.isascii() or not horsepower.isdecimal() or int(horsepower) <= 0:
                messages.error(request, 'Horsepower must be a Positive Whole Number.')
                return redirect('car_list')

            horsepower = int(horsepower)
        
        # Year check
        if year:
            if not year.isascii() or not year.isdecimal() or int(year) <= 0:
                messages.error(request,'Year must be Positive Whole Number(2019,2020,...).')
                return redirect('car_list')

            year = int(year)
        
        # Mileage Check
        if mileage:
            if not mileage.isascii() or not mileage.isdecimal():
                messages.error(request, 'Mileage must be a Whole Number.')
                return redirect('car_list')
    
            mileage = int(mileage)
            
        car.name = name 
        car.brand_id = brand_id 
        car.category_id = category_id 
        car.price = price 
        car.stock = stock 
        car.year = year 
        car.mileage = mileage 
        car.color = color
        car.fuel_type = fuel_type 
        car.transmission = transmission 
        car.engine = engine 
        car.horsepower = horsepower 
        car.description = description 
        car.condition = condition 
        car.is_featured = is_featured 
        
        if thumbnail:
            
            if car.thumbnail:
                car.thumbnail.delete(save=False)
                
            car.thumbnail = thumbnail 
                       
        car.save()       
        
        delete_images = request.POST.getlist('delete_images')       
        for image_id in delete_images:
            
            image = CarImageModel.objects.filter(
                id = image_id,
                car = car,
            ).first()    
                    
            if image:
                if image.image:
                    image.image.delete(save=False)
                image.delete()    
                           
        gallery_images = request.FILES.getlist('gallery_images')        
        for image in gallery_images:
            
            CarImageModel.objects.create(
                image = image,
                car = car,
            )           
        
        messages.success(request,f'{car.name} has been updated successfully.')
        return redirect('car_list')    
    
    return redirect('car_list')


#===============Car Delete==================#
@login_required
def car_delete(request,car_id):
    
    if not request.user.has_perm('lore.delete_carmodel'):
        return render(request, 'errorpage.html', status=403)
    
    car = get_object_or_404(CarModel, id = car_id) 
      
    if request.method == 'POST':
        
        car_name = car.name
        
        if car.thumbnail:
            car.thumbnail.delete(save=False)  
                   
        for image in car.images.all():
            if image.image:
                image.image.delete(save=False)  
                                        
        car.delete()        
        messages.success(request,f'{car_name} has been deleted from the list.')
        return redirect('car_list')
    
    return redirect('car_list')
            