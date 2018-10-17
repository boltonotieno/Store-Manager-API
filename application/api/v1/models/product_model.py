
class Product(object):
    """Class contain product model functions"""
    products = []
    def __init__(self):
        """Initialises the product model"""
        # self.products = []
        
    def create_product(self, name, price, quantity, min_quantity, category):
        """Creates a new product"""
        product = dict(
            product_id=len(self.products)+1,
            product_name = name,
            product_price = price,
            product_quantity =quantity,
            product_min_quantity = min_quantity,
            product_category = category
        )

        self.products.append(product)

        return {'message' : 'Created successfully'}

    def get_all_product(self):
        """Fetches all products"""
        return {'Products' : self.products, 'message' : 'success' }

    def get_one_product(self, product_id):
        if product_id in self.products:
            return {'Product' : self.products[product_id], 'message' : 'success'}
        return {'message' : 'Not found'}

