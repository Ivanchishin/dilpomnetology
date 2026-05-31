import os
from django.conf import settings
from celery import shared_task
from .services import send_order_emails
from .importyaml import import_shop_from_yaml
from .models import User
from django.core.files.storage import default_storage

@shared_task
def send_order_emails_task(order_id):
    from .models import Order
    order = Order.objects.get(id=order_id)
    send_order_emails(order)
    return True

@shared_task
def import_yaml_task(file_path, user_id):
    user = User.objects.get(id=user_id)
    full_path = os.path.join(
        settings.MEDIA_ROOT,
        file_path
    )
    with open(
            full_path,
            "r",
            encoding="utf-8"
    ) as file:
        import_shop_from_yaml(
            file=file,
            user=user
        )
    return True