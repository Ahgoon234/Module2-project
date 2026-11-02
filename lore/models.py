from django.db import models
import uuid
from django.contrib.auth.models import User

CONDITION_CHOICES = [
    ('new','New'),
    ('used','Used'),
]

FUEL_CHOICES = [
    ('petrol','Petrol'),
    ('diesel','Diesel'),
    ('electric','Electric'),
    ('hybrid','Hybrid'),
]

TRANSMISSION_CHOICES = [
    ('automatic','AutoGear'),
    ('manual','ManualGear'),
]


#==============CategoryModel===================#
class CategoryModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='cars/category/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

#=============BrandModel=================#
class BrandModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    title = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='brands/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


#===========================CarModel==========================#
class CarModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    name = models.CharField(max_length=300) 
    brand = models.ForeignKey(BrandModel, on_delete= models.RESTRICT)
    category = models.ForeignKey(CategoryModel, on_delete= models.PROTECT, blank=False, null=False, related_name='cars')
    price = models.DecimalField(max_digits=12,decimal_places=2)
    stock = models.PositiveIntegerField(blank=True,null=True)
    thumbnail = models.ImageField(upload_to='cars/')
    year = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_CHOICES,
        default='petrol'
    )
    transmission = models.CharField(
        max_length=20,
        choices=TRANSMISSION_CHOICES,
        default='automatic'
    )
    engine = models.CharField(max_length=100)
    horsepower = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default='new'
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
#=========================CarImageModel=======================#
class CarImageModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    car = models.ForeignKey(CarModel,on_delete=models.CASCADE, related_name= 'images')
    image = models.ImageField(upload_to='cars/gallery/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.car.name
    
    
#========================ContactMessageModel========================#
class ContactMsgModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField(max_length=400)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name} - {self.email}'
    
    
#=================SparepartCategoryModel==================#
class PartCategoryModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


#===================SparepartModel=======================#
class SparepartModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(PartCategoryModel, on_delete=models.PROTECT, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='spareparts')
    stock = models.PositiveIntegerField()
    brand = models.ForeignKey(BrandModel,on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
#=================SparepartImageModel====================#
class PartImageModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    sparepart = models.ForeignKey(SparepartModel,on_delete=models.CASCADE,related_name= 'images')
    image = models.ImageField(upload_to='spareparts/gallery')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.sparepart.name
    
    
#=================BlogModel====================#
class BlogModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='blogs')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
#==================Cart Model==================#
class CartModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"
    
    
#===============CartItem Model====================#
class CartItemModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='items')
    sparepart = models.ForeignKey(SparepartModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sparepart.name} x {self.quantity}'
    
    
#=============Order Model================#
class OrderModel(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    CANCEL_REASON_CHOICES = (
        ('invalid_address', 'Invalid address'),
        ('customer_request', 'Customer requested cancellation'),
        ('invalid_phone', 'Invalid or unreachable phone number'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    address = models.TextField()
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    cancel_reason = models.CharField(
        max_length=50,
        choices=CANCEL_REASON_CHOICES,
        blank=True,
        null=True
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order - {self.user.username} - {self.status}'
    
    
#=============OrderItem Model==================#
class OrderItemModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='items')
    sparepart = models.ForeignKey(SparepartModel, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sparepart.name} x {self.quantity}'
    
    
#===============User Profile Model==================#
class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    
    def __str__(self):
        return self.user.username