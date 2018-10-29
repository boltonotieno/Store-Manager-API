class Validation:

    def __init__(self, data):
        self.data = data

    def validate_product(self):
            if self.data['name'].isalpha() == False:
                return {'message' : 'Invalid product name'},400

            if self.data['price'].isdigit() == False:
                return {'message' : 'Invalid product price'},400
            
            if self.data['quantity'].isdigit() == False:
                return {'message' : 'Invalid product quantity'},400

            if self.data['min_quantity'].isdigit() == False:
                return {'message' : 'Invalid product minimum quantity'},400

            if self.data['category'].isalpha() == False:
                return {'message' : 'Invalid product category'},400

    def validate_sales(self):
            if self.data['name'].isalpha() == False:
                return {'message' : 'Invalid product name'},400

            if self.data['price'].isdigit() == False:
                return {'message' : 'Invalid product price'},400
            
            if self.data['quantity'].isdigit() == False:
                return {'message' : 'Invalid product quantity'},400
                
