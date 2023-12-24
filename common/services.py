import logging

from .service_decorators import only_field_decorator

# from product.models import Product


logger = logging.getLogger('main')


def get_object(objects, **kwargs):
    logger.info(f"Get an Object from: {kwargs['model_name']}, if {kwargs}")
    return objects.get(**kwargs)


@only_field_decorator
def filter_objects(objects, **kwargs):
    logger.info(f"Get all Objects from: {kwargs['model_name']}, if {kwargs}")
    return objects.filter(**kwargs)


@only_field_decorator
def all_objects(objects, **kwargs):
    logger.info(f"Get all Objects from: {kwargs['model_name']}")
    return objects.all()


# def create_product(title: str):
#     all_products = all_objects(Product.objects)
#     filtered_produts = filter_objects(
#         objects=all_products,
#         title=title,
#         only=('title', 'quantity_in_stock'),
#         prefetch_related=('product_size_chart', 'product_description'),
#         select_related=('product_photos', 'product_tags')
#     )
