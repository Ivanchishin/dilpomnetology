import yaml
from django.db import transaction

from .models import (
    Supplier,
    Product,
    ProductInfo,
    Parameter,
    ProductParameter
)


def import_shop_from_yaml(file, user):
    data = yaml.safe_load(file)

    if not data or 'shop' not in data or 'goods' not in data:
        raise ValueError("Invalid YAML format")

    with transaction.atomic():

        #Поставщики
        supplier, _ = Supplier.objects.get_or_create(
            name=data['shop']
        )

        for item in data['goods']:

            #Товары
            product, _ = Product.objects.get_or_create(
                name=item['name'],
                defaults={'description': item.get('model', '')}
            )

            #Информация о товарах
            product_info, _ = ProductInfo.objects.update_or_create(
                product=product,
                supplier=supplier,
                defaults={
                    'price': item['price'],
                    'quantity': item['quantity']
                }
            )

            # === Очистка старых параметров ===
            ProductParameter.objects.filter(product_info=product_info).delete()

            # === Параметры ===
            for param_name, param_value in item.get('parameters', {}).items():

                parameter, _ = Parameter.objects.get_or_create(
                    name=param_name
                )

                ProductParameter.objects.create(
                    product_info=product_info,
                    parameter=parameter,
                    value=str(param_value)
                )

    return True