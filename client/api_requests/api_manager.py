from .customers_api import CustomersAPI
from .products_api import ProductsAPI
from .orders_api import OrdersAPI


class APIManager:
    def __init__(self, base_url: str):
        self.customers = CustomersAPI(base_url)
        self.products = ProductsAPI(base_url)
        self.orders = OrdersAPI(base_url)
