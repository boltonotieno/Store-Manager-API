users_dict = {}

class Users():
    """Class contain user model functions"""

    def __init__(self):
        """Initialises the user model"""
        # self.name = name
        # self.username = username
        # self.email = email
        # self.password = password
        # self.gender = gender
        # self.role = role
        
    
    def create_user(self, name, username, email, password, gender, role):
        """Creates a new user"""

        if username in users_dict:
            return {
                'message' : 'User named {} already exist'.format( username)
            }
        new_user = dict(
            name = name,
            username = username,
            email = email,
            password = password, 
            gender = gender,
            role = role    
        )  

        users_dict[username] = new_user

        return users_dict
    
    def get_all_users(self):
        """Fetches all users"""
        return users_dict

    def get_one_user(self, username):
        """Fetches one user by id"""

        if username in users_dict:
            return {'User' : users_dict[username], 'message' : 'success'}
        else:
            return {'message' : 'Not found'}


    def get_user_dict(self):

        return users_dict
