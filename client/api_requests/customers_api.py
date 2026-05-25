import requests


class CustomersAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_customers(self):
        response = requests.get(f'{self.base_url}/customers/')
        response.raise_for_status()
        return response.json()

    def get_customer(self, register_customer_number: int):
        response = requests.get(f'{self.base_url}/customers/{register_customer_number}')
        response.raise_for_status()
        return response.json()

    def create_customer(self, data: dict):
        response = requests.post(
            f'{self.base_url}/customers/',
            json=data
        )
        response.raise_for_status()
        return response.json()

    def update_customer(self, register_customer_number: int, data: dict):
        response = requests.put(
            f'{self.base_url}/customers/{register_customer_number}',
            json=data
        )
        response.raise_for_status()
        return response.json()

    def delete_customer(self, register_customer_number: int):
        response = requests.delete(
            f'{self.base_url}/customers/{register_customer_number}'
        )
        response.raise_for_status()
