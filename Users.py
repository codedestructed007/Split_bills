import yaml
import os


class User:
    user_details = {}
    def __init__(self, user_id, name , email):
        self. user_id = user_id
        self.name = name
        self.email = email
        
        
        with open('datahouse/users.yaml','r') as f:
            users = yaml.safe_load(f)
        # check if User with 'user_id' already exists
        if os.path.getsize('datahouse/users.yaml') != 0 and  self.user_id not in users.keys():
            User.user_details[user_id] = {'name': self.name, 'email': self.email}
            new_user = User.user_details
            users.update(new_user)
            with open('datahouse/users.yaml','w') as f:
                yaml.dump(users,f)
                
        elif os.path.getsize('datahouse/users.yaml') == 0:
            User.user_details[user_id] = {'name': self.name, 'email': self.email}
            new_user = User.user_details
            with open('datahouse/users.yaml','w') as f:
                yaml.dump(new_user,f)

    
    import yaml
import os


class User:
    user_details = {}
    def __init__(self, user_id, name , email):
        self. user_id = user_id
        self.name = name
        self.email = email
        
        
        with open('datahouse/users.yaml','r') as f:
            users = yaml.safe_load(f)
        # check if User with 'user_id' already exists
        if os.path.getsize('datahouse/users.yaml') != 0 and  self.user_id not in users.keys():
            User.user_details[user_id] = {'name': self.name, 'email': self.email}
            new_user = User.user_details
            users.update(new_user)
            with open('datahouse/users.yaml','w') as f:
                yaml.dump(users,f)
                
        elif os.path.getsize('datahouse/users.yaml') == 0:
            User.user_details[user_id] = {'name': self.name, 'email': self.email}
            new_user = User.user_details
            with open('datahouse/users.yaml','w') as f:
                yaml.dump(new_user,f)






    @staticmethod
    def show_all_registered_users():
        with open('datahouse/users.yaml', 'r') as f:
            users = yaml.safe_load(f)
            return users



