from django.core.cache import cache
from ..models import Product


class BucketManager:
    def __init__(self, request):
        self.client_cache_key = 'bucket-' + self.get_client_ip(request)
        self.timeout = 86400

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def add_product_id(self, product_id):
        user_bucket_data = self.get_bucket_data()
        user_bucket_data.append(product_id)
        cache.set(self.client_cache_key, user_bucket_data, self.timeout)

    def get_products(self):
        user_bucket_data = self.get_bucket_data()

        products = Product.objects.filter(id__in=user_bucket_data)
        for product in products:
            product.count = user_bucket_data.count(product.id)
            product.price = product.price * product.count

        return products

    def get_bucket_data(self):
        user_bucket_data = cache.get(self.client_cache_key)
        if user_bucket_data is None:
            user_bucket_data = []

        return user_bucket_data

    def set_bucket_data(self, data):
        cache.set(self.client_cache_key, data, self.timeout)

    def clear_bucket_data(self):
        user_bucket_data = []
        cache.set(self.client_cache_key, user_bucket_data, self.timeout)

    def count_of_product(self):
        user_bucket_data = self.get_bucket_data()
        return len(user_bucket_data)

    def get_total_price(self, products=None):
        if products is None:
            products = self.get_products()
        total_price = 0
        for product in products:
            total_price += product.price
        return total_price
