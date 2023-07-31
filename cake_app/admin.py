from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Bakery, Berries, CakeCategory, CatalogCake, Component, ComponentType, Decors, Forms, Order,
    OrderCatalogCakes, OrderComponents, Sizes, Toppings,
)


@admin.register(CakeCategory)
class CakeCategoryAdmin(admin.ModelAdmin):
    def preview_image(self, obj):
        if not obj.image:
            return 'выберите картинку'
        return format_html('<img src="{url}" style="max-height: 200px;"/>', url=obj.image.url)

    readonly_fields = ['preview_image', ]
    fields = [
        'title',
        'image',
        'preview_image'
    ]


@admin.register(CatalogCake)
class CatalogCakeAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'category', 'price']

    def preview_image(self, obj):
        if not obj.image:
            return 'выберите картинку'
        return format_html('<img src="{url}" style="max-height: 200px;"/>', url=obj.image.url)

    readonly_fields = ['preview_image', ]
    fields = [
        'title',
        'category',
        'description',
        'price',
        'image',
        'preview_image'
    ]
    list_filter = ['category']
    search_fields = ['title', 'description']


@admin.register(ComponentType)
class ComponentTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ['title', 'component_type', 'price']
    list_filter = ['component_type']
    search_fields = ['title']


@admin.register(Bakery)
class BakeryAdmin(admin.ModelAdmin):
    list_display = ['title', 'address', 'contact_phone']


class OrderComponentsInline(admin.TabularInline):
    model = OrderComponents


class OrderCatalogCakesInline(admin.TabularInline):
    model = OrderCatalogCakes


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'cake_option', 'comment', 'delivery_datetime', 'delivery_comment',
                    'total_cost']
    search_fields = ['client_name', 'phonenumber']
    list_filter = ['status', 'order_receipt_method']
    ordering = ['-created_at', ]

    inlines = [
        OrderCatalogCakesInline,
        OrderComponentsInline
    ]


@admin.register(Sizes)
class SizesAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']
    search_fields = ['title']


@admin.register(Decors)
class DecorsAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']
    search_fields = ['title']


@admin.register(Berries)
class BerriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']
    search_fields = ['title']


@admin.register(Forms)
class FormsAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']
    search_fields = ['title']


@admin.register(Toppings)
class ToppingsAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']
    search_fields = ['title']
