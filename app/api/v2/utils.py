from .models.product_model import Products

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

            if self.data['category_id'].isdigit() == False:
                return {'message' : 'Invalid product category id'},400

    def validate_sales(self):
            if self.data['name'].isalpha() == False:
                return {'message' : 'Invalid product name'},400
            
            if self.data['quantity'].isdigit() == False:
                return {'message' : 'Invalid product quantity'},400

    def validate_users(self):

            if self.data['username'].isalpha() == False:
                return {'message' : 'Invalid username'},400
            
            if self.data['gender'].isalpha() == False:
                return {'message' : 'Invalid user gender'},400

            if self.data['gender'] != "male" and self.data['gender'] != "female":
                return {'message' : 'Gender should  either be male or female'},400

            if self.data['role'].isalpha() == False:
                return {'message' : 'Invalid user role'},400

            if self.data['role'] != 'admin' and self.data['role'] != 'attendant':
                return {'message' : 'Role should  either be admin or attendant'},400
                