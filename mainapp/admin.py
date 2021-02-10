from django.contrib import admin
from mainapp.models import ProductCategory, Product


# admin.site.register(ProductCategory)
# admin.site.register(Product)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'quantity', 'price')
    ordering = ('category', 'name')
    search_fields = ('name',)
    list_display_links = ('id', 'name')
    fields = ('image', 'name', 'short_description', 'description', 'category', ('quantity', 'price'))
    readonly_fields = ('category',)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')
