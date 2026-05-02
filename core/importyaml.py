import yaml
from django.db import transaction

from .models import (
    Supplier,
    Product,
    ProductInfo,
    Parameter,
    ProductParameter,
)


def import_shop_from_yaml(file, user):
    data = yaml.safe_load(file)

    if not data or 'goods' not in data or 'shop' not in data:
        raise ValueError("Invalid YAML structure")

    with transaction.atomic():
        supplier, _ = Supplier.objects.get_or_create(
            name=data['shop'],
            defaults={'user': user}
        )

        for item in data['goods']:
            product, _ = Product.objects.get_or_create(
                name=item['name'],
                defaults={'description': item.get('model', '')}
            )

            product_info, _ = ProductInfo.objects.update_or_create(
                product=product,
                supplier=supplier,
                defaults={
                    'price': item['price'],
                    'quantity': item['quantity']
                }
            )

            for param_name, param_value in item.get('parameters', {}).items():
                parameter, _ = Parameter.objects.get_or_create(name=param_name)

                ProductParameter.objects.update_or_create(
                    product_info=product_info,
                    parameter=parameter,
                    defaults={'value': str(param_value)}
                )

    return True