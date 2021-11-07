from django.contrib import admin

from .models import Category, Product, Order, ProductOrder

#
# class ProductInline(admin.TabularInline):
#     model = Product
#     extra = 3
#
#
# class CategoryAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['id']}),
#     ]
#     inlines = [ProductInline]
#     # list_display = ('name',)
#     list_filter = ['name']
#     search_fields = ['name']
#
#
# admin.site.register(Category, CategoryAdmin)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ProductOrder)
