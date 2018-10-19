class Users():
    """Class contain user model functions"""

    users_dict = []

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
        new_user = dict(
            user_id = len(Users.users_dict)+1,
            name = name,
            username = username,
            email = email,
            password = password, 
            gender = gender,
            role = role    
        )

        self.users_dict.append(new_user)

        return self.users_dict

    def search_by_username(self, username):
        """search for existing user"""
        user = [user for user in self.users_dict if user['username'] == username]
        return user
    
    def get_all_users(self):
        """Fetches all users"""
        return Users.users_dict

    def get_one_user(self, user_id):
        """Fetches one user by id"""
        user = [user for user in self.users_dict if user['user_id'] == user_id]

        if user:
            return {'User' : user, 'message' : 'success'}
        return {'message' : 'Not found'}


    def get_user_dict(self):

        return Users.users_dict
