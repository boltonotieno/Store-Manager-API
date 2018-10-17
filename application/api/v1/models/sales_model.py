class Sale():
    """Class contain sales model functions"""
    sales = []
    cart = []
    def __init__(self, name, quantity):
        """Initialises the sales model"""
        self.name = name
        self.quantity = quantity

    def create_sale(self):
        """Creates a new sale"""
        sale = dict(
            product_name = self.name,
            product_quantity = self.quantity
        )

        self.sales.append(sale)

        return {'message' : 'Created successfully'}

    def get_all_sale(self):
        """Fetches all sales"""
        pass

    def get_one_sale(self, sale_id):
        """Fetches one sale by id"""
        pass
