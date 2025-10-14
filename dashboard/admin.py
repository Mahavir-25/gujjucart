from django.contrib import admin
from dashboard.models import UserProfile,Product,Wishlist
from django.utils.html import format_html


admin.site.register(UserProfile)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'created_at')
    def image_tag(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" width="50" />'.format(obj.product_image.url))
        return "-"
    image_tag.short_description = 'Image'
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('user', 'product')
    search_fields = ('user__username', 'product__name')