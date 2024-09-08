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
    SSLCOMMERZ = 2, 'SSLCommerz'
    BKASH = 3, 'bKash'


class OrderStatus(IntegerChoices):
    PLACED = 0, 'Placed'
    PROCESSING = 1, 'Processing'
    CONFIRMED = 2, 'Confirmed'
    PACKING = 3, 'Packing'
    READY_TO_SHIP = 4, 'Ready to Ship'
    SHIPPED = 5, 'Shipped'
    CANCELLED = 6, 'Cancelled'  # Added Cancelled status
    PICKUP_REQUESTED = 7, 'Pickup Requested'
    ASSIGNED_FOR_PICKUP = 8, 'Assigned for Pickup'
    PICKED = 9, 'Picked'
    PICKUP_FAILED = 10, 'Pickup Failed'
    PICKUP_CANCELLED = 11, 'Pickup Cancelled'
    AT_THE_SORTING_HUB = 12, 'At the Sorting HUB'
    IN_TRANSIT = 13, 'In Transit'
    RECEIVED_AT_LAST_MILE_HUB = 14, 'Received at Last Mile HUB'
    ASSIGNED_FOR_DELIVERY = 15, 'Assigned for Delivery'
    DELIVERED = 16, 'Delivered'
    PARTIAL_DELIVERY = 17, 'Partial Delivery'
    RETURN = 18, 'Return'
    DELIVERY_FAILED = 19, 'Delivery Failed'
    ON_HOLD = 20, 'On Hold'
    PAYMENT_INVOICE = 21, 'Payment Invoice'
    PAID_RETURN = 22, 'Paid Return'
    EXCHANGE = 23, 'Exchange'


class PaymentStatus(IntegerChoices):
    PENDING = 0, 'Pending'
    PAID = 1, 'PAID'
    PARTIALLY_PAID = 2, 'Partially Paid'
