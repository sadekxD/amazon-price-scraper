class Product:
    def __init__(self, name, price, link):
        self.product_name = name
        self.product_price = price
        self.product_link = link

    def serialize(self):
        return {
            'name': self.product_name,
            'price': self.product_price,
            'link': self.product_link,
        }

    def from_json(self, json):
        self.product_name = json['name']
        self.product_price = json['price']
        self.product_link = json['link']
