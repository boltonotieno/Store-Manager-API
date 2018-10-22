class Sale():
    """Class contain sales model functions"""
    sales = []
    def __init__(self, name, price, quantity):
        """Initialises the sales model"""
        self.name = name
        self.price = price
        self.quantity = quantity

    def create_sale(self):
        """Creates a new sale"""
        cart_item = dict(
            product_name = self.name,
            product_price = self.price,
            product_quantity = self.quantity,
            total_price = int(self.price) * int(self.quantity)     
        )
        
        sale = dict(
            sale_id = len(self.sales)+1,
            cart_items = cart_item
        )

        self.sales.append(sale)

        return {'Sales' : self.sales, 'message' : 'Created successfully'}

    def get_all_sale(self):
        """Fetches all sales"""
        pass

    def get_one_sale(self, sale_id):
        """Fetches one sale by id"""
        pass
