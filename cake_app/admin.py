from django.contrib import admin
from django.utils.html import format_html
from django.db.models import F, Sum

from .models import CakeCategory
from .models import CatalogCake
from .models import ComponentType
from .models import Component
from .models import Bakery
from .models import Order
from .models import OrderComponents
from .models import OrderCatalogCakes


@admin.register(CakeCategory)
class CakeCategoryAdmin(admin.ModelAdmin):
    def preview_image(self, obj):
        if not obj.image:
            return 'выберите картинку'
        return format_html('<img src="{url}" style="max-height: 200px;"/>', url=obj.image.url)
    readonly_fields = ['preview_image',]
    fields = [
        'title',
        'image',
        'preview_image'
    ]


@admin.register(CatalogCake)
class CatalogCakeAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price']
    def preview_image(self, obj):
        if not obj.image:
            return 'выберите картинку'
        return format_html('<img src="{url}" style="max-height: 200px;"/>', url=obj.image.url)
    readonly_fields = ['preview_image',]
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
    def total_price(self, obj):
        components = OrderComponents.objects.filter(order=obj).aggregate(
            total_price=Sum(
                F('price')*F('quantity')
            )
        )
        cakes = OrderCatalogCakes.objects.filter(order=obj).aggregate(
            total_price=Sum(
                F('price')*F('quantity')
            )
        )
        prices = [cakes['total_price'], components['total_price']]
        return sum([price for price in prices if price])
    total_price.short_description = 'общая стоимость заказа'
    readonly_fields = ['total_price',]
    list_display = ['client_name', 'status', 'id', 'phonenumber', 'total_price', 'created_at']
    search_fields = ['client_name', 'phonenumber']
    list_filter = ['status', 'order_receipt_method']
    ordering = ['-created_at',]
    fields = [
        'status',
        'created_at',
        'completed_at',
        'client_name',
        'phonenumber',
        'email',
        'comment',
        'order_receipt_method',
        'bakery',
        'address',
        'delivery_datetime',
        'delivered_at',
        'delivery_comment',
        'total_price',
        'inscription'
    ]
    inlines = [
        OrderCatalogCakesInline,
        OrderComponentsInline
    ]
