
class Product(object):
    """Class contain product model functions"""
    products = [] 
    def __init__(self, name, price, quantity, min_quantity, category):
        """Initialises the product model"""
        self.name = name
        self.price = price
        self.quantity= quantity
        self.min_quantity= min_quantity
        self.category = category
        
    def create_product(self):
        """Creates a new product"""
        product = dict(
            product_id=len(self.products)+1,
            product_name = self.name,
            product_price = self.price,
            product_quantity = self.quantity,
            product_min_quantity = self.min_quantity,
            product_category = self.category
        )

        self.products.append(product)

        return {'message' : 'Created successfully'}

    def get_all_product(self):
        """Fetches all products"""
        return {'Products' : self.products, 'message' : 'success' }
