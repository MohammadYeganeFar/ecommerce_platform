from abc import ABC, abstractmethod
import logging
from apps.utils.functions import encrypter
from apps.database.managers import user_manager
from setting import USERS_LOG_PATH

"""
purpose:
1- create users(standard and admin)


"""
logging.basicConfig(filename=USERS_LOG_PATH, level=logging.INFO,style='%',
                    format="%(asctime)s : %(levelname)s : %(message)s")
                    # format="{asctime}:{levelname}:{message}")
class User():
    logged_in = False
    def __init__(self,username, password, role ):
        self.new_user(username, password, role)

    @user_manager.add_user
    def new_user(self, username, password, user_role):
        from apps.account.auth import Authexeption
        Authexeption.check_username_exist(username)
        Authexeption.check_password_length(password)
        logging.info("new user: usernam = %s", username)
        # logging.info(f"new user: usernam = {username}, role = {user_role}")
        return [username, user_role, self.logged_in, encrypter(password)]
    

class StandardUser(User):
    pass

class AdminUser(User):
    pass

