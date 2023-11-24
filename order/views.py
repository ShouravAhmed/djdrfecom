from django.shortcuts import render

# ---------------------------------------------------
# how to cache a python object
# ---------------------------------------------------
# pathao_client = PathaoApi()
# self.delivery_cost = pathao_client.get_delivery_cost(
#     self.store.store_id,
#     self.customer_city.city_id,
#     self.customer_zone.zone_id,
#     self.item_type,
#     self.delivery_type,
#     self.item_weight
# )

# import pickle
# import redis

# r = redis.StrictRedis(host='localhost', port=6379, db=0)
# obj = ExampleObject()
# pickled_object = pickle.dumps(obj)
# r.set('some_key', pickled_object)
# unpacked_object = pickle.loads(r.get('some_key'))
# obj == unpacked_object
