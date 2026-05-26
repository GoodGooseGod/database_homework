import requests
from datetime import date


class OrdersAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_orders(self):
        response = requests.get(f'{self.base_url}/orders/')
        response.raise_for_status()
        return response.json()

    def get_order(self,  order_date: date, order_number: int):
        response = requests.get(f'{self.base_url}/orders/{order_date}/{order_number}')
        response.raise_for_status()
        return response.json()

    def create_order(self, **data):
        response = requests.post(
            f'{self.base_url}/orders/',
            json=data
        )
        response.raise_for_status()
        return response.json()

    def update_order(self, order_date: date, order_number: int, **data):
        response = requests.put(
            f'{self.base_url}/orders/{order_date}/{order_number}',
            json=data
        )
        response.raise_for_status()
        return response.json()

    def delete_order(self, order_date: date, order_number: int):
        response = requests.delete(
            f'{self.base_url}/orders/{order_date}/{order_number}'
        )
        response.raise_for_status()
