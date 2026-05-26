import requests


class ProductsAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_products(self):
        response = requests.get(f'{self.base_url}/products/')
        response.raise_for_status()
        return response.json()

    def get_product(self, barcode: int):
        response = requests.get(f'{self.base_url}/products/{barcode}')
        response.raise_for_status()
        return response.json()

    def create_product(self, **data):
        response = requests.post(
            f'{self.base_url}/products/',
            json=data
        )
        response.raise_for_status()
        return response.json()

    def update_product(self, barcode: int, **data):
        response = requests.put(
            f'{self.base_url}/products/{barcode}',
            json=data
        )
        response.raise_for_status()
        return response.json()

    def delete_product(self, barcode: int):
        response = requests.delete(
            f'{self.base_url}/products/{barcode}'
        )
        response.raise_for_status()
