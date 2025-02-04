from pandas import read_csv
from .user import AdminUser, StandardUser
from ..database.file_handler import UserFileManager
from apps.utils.functions import encrypter
from setting import DIRS
import csv
#local import: Authenticator.add_user() : from apps.account.user import AdminUser

"""
purpose:
1- Authentication users.
2- Exeption handling of authentication procces

"""




# encrypter or User password encrypter

class UsernameAlreadyExist(Exception):
    def __init__(self, message="Username already exist ⛔"):
        super().__init__(message)

class PasswordTooShort(Exception):
    def __init__(self, message="Password is too short ⛔"):
        super().__init__(message)

class InvalidUsername(Exception):
    def __init__(self, message="Username is invalid ⛔"):
        super().__init__(message)

class InvalidPassword(Exception):
    def __init__(self, message="Password is invalid ⛔"):
        super().__init__(message)

class AccessDenied(Exception):
    def __init__(self, message="Access denied ⛔"):
        super().__init__(message)

class NotLoggedIn(Exception):
    def __init__(self, message="You are not logged in ⛔"):
        super().__init__(message)

# by ai
class UserNotFound(Exception):
    def __init__(self, message="User not found in the database ⛔"):
        super().__init__(message)
        
        
# Authexeption class is bas class for all exeptins
class Authexeption:
    @staticmethod
    def check_username_exist(username):
        usernames = read_csv(DIRS["USERS_DATA_PATH"])["username"]
        for i in usernames:
            if i == username:
                raise UsernameAlreadyExist(f"Username '{username}' is already taken ⛔")
        
    @staticmethod
    def check_password_length(password):
        if len(password) < 8:
            raise PasswordTooShort("Password must be at least 8 characters long ⛔")
    
    @staticmethod
    def check_username_valid(username):
        if not username in read_csv(DIRS["USERS_DATA_FILE"])["username"]:
            raise InvalidUsername(f"Username '{username}' does not exist ⛔")
    
    @staticmethod
    def check_password_valid(username, password):
        if encrypter(password) != data_base[username]:
            raise InvalidPassword(f"Incorrect password for user '{username}' ⛔")
        
    @staticmethod
    def is_admin(role):
        if role != "admin":
            raise AccessDenied("This action requires admin privileges ⛔")
            






class Authenticator():
    
    @staticmethod
    def add_user(username, password, user_role):
        from apps.account.user import AdminUser, StandardUser
        if user_role == "admin" or user_role == "a":
            user = AdminUser(username, password, user_role)
        elif user_role == "standard" or user_role == "s":
            user = StandardUser(username, password, user_role)
        else:
            raise ValueError('invalid input')
            


    @staticmethod
    def delete_user(admin_username: str, admin_password: str, user_to_delete: str) -> bool:
        """
        Delete a user from the system. Only admins can delete standard users.
        
        Args:
            admin_username: Username of the admin attempting to delete
            admin_password: Password of the admin
            user_to_delete: Username of the user to be deleted
            
        Raises:
            AccessDenied: If the user is not an admin
            UserNotFound: If either admin or user to delete not found
        """
        with open(DIRS["USERS_DATA_PATH"], 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            # Find admin user and verify logged in
            admin_found = False
            for row in rows:
                if row['username'] == admin_username:
                    if row['password'] == encrypter(admin_password):
                        if row['role'] != 'a':
                            raise AccessDenied(f"User '{admin_username}' does not have admin privileges ⛔")
                        if row['logged_in'] != 'True':
                            raise AccessDenied(f"Admin '{admin_username}' must be logged in to delete users ⛔")
                        admin_found = True
                        break
            
            if not admin_found:
                raise UserNotFound(f"Admin user '{admin_username}' not found ⛔")
                
            # Find and delete target user
            user_found = False
            new_rows = []
            for row in rows:
                if row['username'] == user_to_delete:
                    if row['role'] == 'a':
                        raise AccessDenied(f"Cannot delete admin user '{user_to_delete}' ⛔")
                    user_found = True
                else:
                    new_rows.append(row)
                    
            if not user_found:
                raise UserNotFound(f"User '{user_to_delete}' not found ⛔")
                
            # Write back to file
            with open(DIRS["USERS_DATA_PATH"], 'w', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=['username', 'role', 'logged_in', 'password'])
                writer.writeheader()
                writer.writerows(new_rows)
                
            return True
    
    @staticmethod
    def login(username: str, password: str) -> bool:
        """
        Authenticate a user by their username and password.
        
        Args:
            username (str): Username of the user trying to log in.
            password (str): Password of the user trying to log in.
            
        Returns:
            bool: True if authentication is successful
            
        Raises:
            UserNotFound: If username not found or password incorrect
        """
        with open(DIRS["USERS_DATA_PATH"], 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)  # Convert to list to allow modification
            
            # Find and verify user
            user_found = False
            for row in rows:
                if row['username'] == username:
                    if row['password'] == encrypter(password):
                        row['logged_in'] = 'True'  # Update login status
                        user_found = True
                        break
            
            if not user_found:
                raise UserNotFound(f"Invalid username or password for '{username}' ⛔")
            
            # Write back to file with updated login status
            with open(DIRS["USERS_DATA_PATH"], 'w', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=['username', 'role', 'logged_in', 'password'])
                writer.writeheader()
                writer.writerows(rows)
                
            return True
    
    @staticmethod
    def logout(username: str) -> bool:
        """
        Logs out a user from the system.
        
        Args:
            username (str): Username of the user to log out
            
        Returns:
            bool: True if logout successful
            
        Raises:
            UserNotFound: If username not found
            InvalidUsername: If user is not logged in
        """
        with open(DIRS["USERS_DATA_PATH"], 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            # Find user and update logged_in status
            user_found = False
            for row in rows:
                if row['username'] == username:
                    user_found = True
                    if row['logged_in'] != 'True':
                        raise InvalidUsername(f"User '{username}' is not logged in ⛔")
                    row['logged_in'] = 'False'
                    break
                    
            if not user_found:
                raise UserNotFound(f"User '{username}' not found ⛔")
                
            # Write back to file
            with open(DIRS["USERS_DATA_PATH"], 'w', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=['username', 'role', 'logged_in', 'password'])
                writer.writeheader()
                writer.writerows(rows)
                
            return True