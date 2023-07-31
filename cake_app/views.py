from django.shortcuts import render
import datetime
from .models import Order, CatalogCake, CakeCategory, Sizes, Decors, Berries, Forms, Toppings


def get_cake_element():
    cake_elements = {
        'forms': Forms.objects.all(),
        'toppings': Toppings.objects.all(),
        'berries': Berries.objects.all(),
        'decors': Decors.objects.all(),
        'sizes': Sizes.objects.all()
    }
    cake_elements_json = {
        'size_titles': {0: 'не выбрано'} | {item.id: item.title for item in cake_elements['sizes']},
        'size_costs': {0: 0} | {item.id: int(item.price) for item in cake_elements['sizes']},
        'form_titles': {0: 'не выбрано'} | {item.id: item.title for item in cake_elements['forms']},
        'form_costs': {0: 0} | {item.id: int(item.price) for item in cake_elements['forms']},
        'topping_titles': {0: 'не выбрано'} | {item.id: item.title for item in cake_elements['toppings']},
        'topping_costs': {0: 0} | {item.id: int(item.price) for item in cake_elements['toppings']},
        'berry_titles': {0: 'нет'} | {item.id: item.title for item in cake_elements['berries']},
        'berry_costs': {0: 0} | {item.id: int(item.price) for item in cake_elements['berries']},
        'decor_titles': {0: 'нет'} | {item.id: item.title for item in cake_elements['decors']},
        'decor_costs': {0: 0} | {item.id: int(item.price) for item in cake_elements['decors']},
    }
    return cake_elements, cake_elements_json


def create_order(request):
    print('request:', request)
    email = request.GET.get('EMAIL')
    address = request.GET.get('ADDRESS')
    order_date = request.GET.get('DATE')
    order_time = request.GET.get('TIME')
    comment = request.GET.get('DELIVCOMMENTS')
    customer_name = request.GET.get('NAME')
    cake_name = request.GET.get('COMMENTS')
    phone = request.GET.get('PHONE')
    inscription=request.GET.get('WORDS')
    levels = request.GET.get('LEVELS')
    form = request.GET.get('FORM')
    topping = request.GET.get('TOPPING')
    berries = request.GET.get('BERRIES')
    decor = request.GET.get('DECOR')
    cake_form_obj = Forms.objects.get(id=form)
    cake_levels_obj = Sizes.objects.get(id=levels)
    cake_topping_obj = Toppings.objects.get(id=topping)
    total_cost = cake_form_obj.price + cake_levels_obj.price + cake_topping_obj.price
    cake_berries_obj = None
    cake_decor_obj = None
    if berries:
        cake_berries_obj = Berries.objects.get(id=berries)
        total_cost += cake_berries_obj.price
    if decor:
        cake_decor_obj = Decors.objects.get(id=decor)
        total_cost += cake_decor_obj.price
    if inscription:
        total_cost = total_cost + 500
    if order_date:
        order_date_dtobj = datetime.datetime.strptime(order_date, '%Y-%m-%d')
        min_date = datetime.datetime.now() + datetime.timedelta(days=1)
        if order_date_dtobj < min_date:
            total_cost = total_cost * 1.2
    order = Order.objects.create(
        client_name=customer_name,
        phonenumber=phone,
        email=email,
        comment=cake_name,
        address=address,
        delivery_datetime=f'{order_date} {order_time}',
        delivery_comment=f'{comment}',
        order_receipt_method='DELIVERY',
        cake_size=cake_levels_obj,
        cake_form=cake_form_obj,
        cake_topping=cake_topping_obj,
        cake_berry=cake_berries_obj,
        cake_decor=cake_decor_obj,
        inscription=inscription,
        total_cost=total_cost
    )


def index(request):
    phone = request.GET.get('PHONE')
    if phone:
        create_order(request)
    cake_elements, cake_elements_json = get_cake_element()

    return render(
        request,
        template_name='index.html',
        context={
            'cake_elements': cake_elements,
            'cake_elements_json': cake_elements_json,
            'cake_category': CakeCategory.objects.all()
        }
    )


def catalog_api(request, id):
    phone = request.GET.get('PHONE')
    if phone:
        create_order(request)

    cake_elements, cake_elements_json = get_cake_element()

    if not id:
        cakes = CatalogCake.objects.all()
    else:
        cakes = CatalogCake.objects.filter(category_id=id)

    cake_json = {
        'cake_titles': {0: 'не выбрано'} | {item.id: item.title for item in cakes},
        'cake_costs': {0: 0} | {item.id: int(item.price) for item in cakes},
    }

    return render(
        request,
        template_name='catalog.html',
        context={
            'cake_elements': cake_elements,
            'cake_elements_json': cake_elements_json,
            'cakes': cakes,
            'cake_json': cake_json
        }
    )
