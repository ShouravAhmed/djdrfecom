from django.db.models import IntegerChoices


class OfferType(IntegerChoices):
    FLAT_DISCOUNT = 0, 'Flat Discount'
    CLEARANCE_SALE = 1, 'Clearance Sale'
    FREE_DELIVERY = 2, 'Free Delivery'
    PROMO_CODE = 3, 'Promo Code'


class DiscountType(IntegerChoices):
    PERCENTAGE = 0, 'Percentage'
    FIXED = 1, 'Fixed'
