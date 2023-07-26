from django.contrib import admin

from .models import CakeCategory
from .models import CatalogCake
from .models import ComponentType
from .models import Component
from .models import Delivery
from .models import Bakery
from .models import Order
from .models import OrderItems


@admin.register(CakeCategory)
class CakeCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(CatalogCake)
class CatalogCakeAdmin(admin.ModelAdmin):
    pass


@admin.register(ComponentType)
class ComponentTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    pass


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    pass


@admin.register(Bakery)
class BakeryAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    pass
