from django.core.mail import send_mail
from django.conf import settings


def send_order_emails(order):

    items_text = ""

    for item in order.items.all():

        items_text += (
            f"Товар: {item.product_info.product.name}\n"
            f"Поставщик: {item.product_info.supplier.name}\n"
            f"Количество: {item.quantity}\n"
            f"Цена: {item.product_info.price}\n"
            f"Сумма: {item.total_price()}\n\n"
        )

    total = order.total_sum()

    admin_subject = f"Новый заказ #{order.id}"

    admin_message = (
        f"Поступил новый заказ.\n\n"
        f"Клиент: {order.user.email}\n"
        f"Заказ №: {order.id}\n\n"
        f"{items_text}"
        f"Итого: {total}"
    )

    send_mail(
        subject=admin_subject,
        message=admin_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['admin@example.com'],
        fail_silently=False
    )

    client_subject = f"Ваш заказ #{order.id} принят"

    client_message = (
        f"Здравствуйте.\n\n"
        f"Ваш заказ успешно принят.\n\n"
        f"{items_text}"
        f"Итого: {total}\n\n"
        f"Спасибо за заказ."
    )

    send_mail(
        subject=client_subject,
        message=client_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.user.email],
        fail_silently=False
    )