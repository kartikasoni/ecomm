from django.contrib import admin
from .models import Product

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'name', 'price', 'stock','description', 'category', 'image_url']
    list_filter = ['category']
    search_fields = ['name', 'description', 'category']
   # readonly_fields = ['image_preview', 'created_at', 'updated_at']
    # search_fields = ['name', 'category']
    # list_filter = ['category', 'created_at']
