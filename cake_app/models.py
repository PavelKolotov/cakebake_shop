from django.db import models
from django.db.models import F, Sum
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


class CakeCategory(models.Model):
    title = models.CharField(
        'название категории',
        max_length=100
    )

    class Meta():
        verbose_name = 'категория торта'
        verbose_name_plural = 'категории тортов'

    def __str__(self):
        return self.title


class CatalogCake(models.Model):
    title = models.CharField(
        'название торта',
        max_length=100
    )
    description = models.TextField('описание торта')
    category = models.ForeignKey(
        CakeCategory,
        on_delete=models.CASCADE,
        related_name='cakes'
    )
    price = models.DecimalField(
        'цена',
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    image = models.ImageField('изображение торта')

    class Meta():
        verbose_name = 'каталожный торт'
        verbose_name_plural = 'каталожные торты'

    def __str__(self):
        return self.title


class ComponentType(models.Model):
    title = models.CharField(
        'название типа',
        max_length=100
    )

    class Meta():
        verbose_name = 'тип компонента'
        verbose_name_plural = 'типы компонентов'

    def __str__(self):
        return self.title


class Component(models.Model):
    title = models.CharField(
        'название компонента',
        max_length=100
    )
    component_type = models.ForeignKey(
        ComponentType,
        on_delete=models.CASCADE,
        related_name='components'
    )
    price = models.DecimalField(
        'цена',
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )

    class Meta():
        verbose_name = 'компонент'
        verbose_name_plural = 'компоненты'

    def __str__(self):
        return self.title


class Delivery(models.Model):
    address = models.CharField(
        'адрес доставки',
        max_length=250
    )
    delivery_datetime = models.DateTimeField(
        'время доставки',
        db_index=True
    )
    delivered_at = models.DateTimeField(
        'доставили',
        null=True,
        blank=True,
        db_index=True
    )
    comment = models.TextField(
        'комментарий курьеру',
        blank=True
    )

    class Meta():
        verbose_name = 'доставка'
        verbose_name_plural = 'доставки'

    def __str__(self):
        return f'№{self.id} - {self.address}'


class Bakery(models.Model):
    title = models.CharField(
        'название кондитерской',
        max_length=100
    )
    address = models.CharField(
        'адрес кондитерской',
        max_length=250
    )
    contact_phone = PhoneNumberField(
        verbose_name='номер телефона кондитерской',
        region='RU'
    )

    class Meta():
        verbose_name = 'пекарня'
        verbose_name_plural = 'пекарни'

    def __str__(self):
        return self.title


class OrderQuerySet(models.QuerySet):
    def total_price(self):
        return self.annotate(
            total_price=Sum(
                F('items__price')*F('items__quantity')
            )
        )


class Order(models.Model):
    ORDER_STATUSES = [
        ('PLACED', 'Оформлен'),
        ('DELIVERED', 'Доставляется'),
        ('TAKEN', 'Получен')
    ]

    status = models.CharField(
        'статус заказа',
        max_length=15,
        choices=ORDER_STATUSES,
        default='PLACED',
        db_index=True
    )
    delivery = models.OneToOneField(
        Delivery,
        on_delete=models.SET_NULL,
        related_name='order',
        verbose_name='доставка',
        null=True,
        blank=True
    )
    bakery = models.ForeignKey(
        Bakery,
        on_delete=models.SET_NULL,
        related_name='orders',
        verbose_name='лавка самовывоза',
        null=True,
        blank=True
    )
    client_name = models.CharField(
        'имя клиента',
        max_length=100
    )
    phonenumber = PhoneNumberField(
        verbose_name='номер телефона',
        region='RU'
    )
    email = models.EmailField(
        verbose_name='почта клиента'
    )
    comment = models.TextField(
        'комментарий к заказу',
        blank=True
    )
    created_at = models.DateTimeField(
        'заказ зарегестрирован',
        default=timezone.now,
        db_index=True
    )
    completed_at = models.DateTimeField(
        'заказ выполнен',
        null=True,
        blank=True,
        db_index=True
    )

    objects = OrderQuerySet.as_manager()

    class Meta():
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ № {self.id}. {self.client_name}, телефон - {self.phonenumber}'


class OrderItems(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='заказ'
    )
    catalog_cake = models.ForeignKey(
        CatalogCake,
        on_delete=models.SET_NULL,
        related_name='order_items',
        verbose_name='торт из каталога',
        null=True,
        blank=True
    )
    component = models.ForeignKey(
        Component,
        on_delete=models.SET_NULL,
        related_name='order_items',
        verbose_name='компонент торта',
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField(
        'количество',
        validators=[MinValueValidator(1)],
        default=1
    )
    inscription = models.TextField(
        'надпись на торт',
        blank=True,
        help_text='заполняется для компонента "надпись"'
    )
    price = models.DecimalField(
        'цена в заказе',
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )

    class Meta():
        verbose_name = 'состав заказа'
        verbose_name_plural = 'состав заказа'

    def __str__(self):
        if self.catalog_cake:
            item_name = self.catalog_cake.title
        else:
            item_name = self.component.title
        return f'Заказ № {self.order.id}. {item_name}, {self.quantity} шт.'
