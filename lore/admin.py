from django.contrib import admin
from lore.models import BrandModel,CategoryModel,CarImageModel,CarModel,ContactMsgModel,SparepartModel,PartCategoryModel,PartImageModel,BlogModel

# Register your models here.

admin.site.register(BrandModel)
admin.site.register(CategoryModel)
admin.site.register(CarImageModel)
admin.site.register(CarModel)
admin.site.register(ContactMsgModel)
admin.site.register(SparepartModel)
admin.site.register(PartCategoryModel)
admin.site.register(PartImageModel)
admin.site.register(BlogModel)