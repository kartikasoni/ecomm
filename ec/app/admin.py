from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Product, Cart, Wishlist, Order, OrderItem

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = [
        'product_id',
        'name',
        'price',
        'stock',
        'category',
        'image_preview',
        'updated_at',
        'edit_link',  # 👈 new column with "Edit" button
    ]
    list_display_links = ['name']  # 👈 makes product name clickable (edit page)
    list_filter = ['category']
    search_fields = ['name', 'description', 'category']
    readonly_fields = ['image_preview', 'created_at', 'updated_at']
    list_editable = ['price', 'stock', 'category']  # 👈 removed 'name' from here
    list_per_page = 10
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True
    fields = ['name', 'description', 'price', 'stock', 'category', 'image_url', 'image_preview']

    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image_url.url)
        return 'No Image'
    image_preview.short_description = 'Image Preview'

    # 👇 Add an explicit "Edit" link column
    def edit_link(self, obj):
        # replace 'app' below with your actual app name (the one where models.py is)
        url = reverse('admin:app_product_change', args=[obj.pk])
        return format_html(f'<a class="button" href="{url}">Edit</a>')
    edit_link.short_description = 'Edit Product'

# Register other models
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItem)
