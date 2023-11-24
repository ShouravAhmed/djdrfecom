from django.db.models import IntegerChoices


class OfferType(IntegerChoices):
    FLAT_DISCOUNT = 0, 'Flat Discount'
    CLEARANCE_SALE = 1, 'Clearance Sale'
    FREE_DELIVERY = 2, 'Free Delivery'
    TRUSTED_CUSTOMER_DEAL = 3, 'Trusted Customer Deal'
    LUCKY_CUSTOMER_DEAL = 4, 'Lucky Customer Deal'
