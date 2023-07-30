from django.shortcuts import render

from .models import Component, Order, CatalogCake, CakeCategory


def index(request):
    phone = request.GET.get('PHONE')
    if phone:
        email = request.GET.get('EMAIL')
        address = request.GET.get('ADDRESS')
        order_date = request.GET.get('DATE')
        order_time = request.GET.get('TIME')
        comment = request.GET.get('DELIVCOMMENTS')
        customer_name = request.GET.get('NAME')
        cake_name = request.GET.get('COMMENTS')
        order = Order.objects.create(
            client_name=customer_name,
            phonenumber=phone,
            email=email,
            comment=cake_name,
            address=address,
            delivery_datetime=order_date,
            delivery_comment=f'{order_time} {comment}',
            order_receipt_method='DELIVERY'
        )
    components = Component.objects.all()
    cake_elements = {
        'forms': components.filter(component_type_id=1),
        'toppings': components.filter(component_type_id=2),
        'berries': components.filter(component_type_id=3),
        'decors': components.filter(component_type_id=4),
        'sizes': components.filter(component_type_id=5)
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
        email = request.GET.get('EMAIL')
        address = request.GET.get('ADDRESS')
        order_date = request.GET.get('DATE')
        order_time = request.GET.get('TIME')
        comment = request.GET.get('DELIVCOMMENTS')
        customer_name = request.GET.get('NAME')
        cake_name = request.GET.get('COMMENTS')
        order = Order.objects.create(
            client_name=customer_name,
            phonenumber=phone,
            email=email,
            comment=cake_name,
            address=address,
            delivery_datetime=order_date,
            delivery_comment=f'{order_time} {comment}',
            order_receipt_method='DELIVERY'
        )
    components = Component.objects.all()
    cake_elements = {
        'forms': components.filter(component_type_id=1),
        'toppings': components.filter(component_type_id=2),
        'berries': components.filter(component_type_id=3),
        'decors': components.filter(component_type_id=4),
        'sizes': components.filter(component_type_id=5)
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