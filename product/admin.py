from django.contrib import admin

from .models import *

admin.site.register(ProductCategory)
admin.site.register(ProductDescription)
admin.site.register(ProductSizeChart)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Tag)
admin.site.register(ProductTag)
admin.site.register(CartProduct)
admin.site.register(WishListProduct)
