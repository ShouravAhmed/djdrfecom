from django.db.models import IntegerChoices


class CourierOption(IntegerChoices):
    PATHAO = 1, 'Pathao Courier'
    REDX = 2, 'RedX Courier'


class DeliveryType(IntegerChoices):
    REGURAL = 48, 'Regular delivery'
    ON_DEMAND = 12, 'On Demand delivery'


class ItemType(IntegerChoices):
    DOCUMENT = 1, 'Document Item'
    PARCEL = 2, 'Parcel Item'
    FRAGILE = 3, 'Fragile Item'


class PaymentMethod(IntegerChoices):
    CASH_ON_DELIVERY = 1, 'Cash On Delivery'
    SSLCOMMERZ = 2, 'sslcommerz'
    BKASH = 3, 'bKash'
