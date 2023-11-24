import datetime
import random
import string

from django.db import models


class OrderManager(models.Manager):
    def create_order(self, user, *args, **kwargs):
        order = self.create(customer=user, *args, **kwargs)
        order.order_id = self.generate_order_id(user.phone_number[-4:])
        order.save()
        return order

    @staticmethod
    def generate_order_id(user_phone):
        company_prefix = 'F'
        date_prefix = datetime.datetime.now().strftime('%Y%m%d')
        random_chars = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=4))
        return f"{company_prefix}{date_prefix}-{random_chars}-{user_phone[-4:]}"
