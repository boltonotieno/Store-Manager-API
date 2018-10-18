class Sale():
    """Class contain sales model functions"""
    sales = []
    def __init__(self):
        """Initialises the sales model"""
        # self.sales = []

    def create_sale(self, name, price, quantity):
        """Creates a new sale"""
        cart_item = dict(
            product_name = name,
            product_price = price,
            product_quantity = quantity,
            total_price = int(price) * int(quantity)     
        )
        
        sale = dict(
            sale_id = len(self.sales)+1,
            cart_items = cart_item
        )

        self.sales.append(sale)

        return {'Sales' : self.sales, 'message' : 'Created successfully'}

    def get_all_sale(self):
        """Fetches all sales"""
        if len(self.sales) == 0:
            return {'message' : 'No sales'}
            
        return {'Sales' : self.sales, 'message' : 'success' }

    def get_one_sale(self, sale_id):
        """Fetches one sale by id"""
        pass
