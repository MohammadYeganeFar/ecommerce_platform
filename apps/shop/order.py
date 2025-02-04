from apps.database.managers import user_manager, product_manager, order_manager
# from apps.utils.functions import log_order
from setting import DIRS



class Order:
    def __init__(self, username, product, amount):
        self.username = username
        self.product = product
        self.amount = amount
        self.to_cart()
    

   
    def to_cart(self):
        #1- is product exist? how many?
        if product_manager.exists(self.product):
            if product_manager.get_detail(self.product, "inventory") >= self.amount:
                user_manager.add_to_user_cart(self.username, self.product, self.amount)
            else:
                print(f"your given amount is greater than {self.product} inventory")
        else:
            print("Product does not exist")

        
    # @staticmethod
    # def finalize(usernaem, prod):
    #     # checking that pr













    # # @log_order
    # # def order(user, amount):
    # #     if inventory >= amount:
    # #         inventory -= amount
    # #         usercart.update({.name : amount})
    # #         return f"user: {user.username}, {name}, amount: {amount}, inventory after order: {inventory}"
    # #     else:
    # #         print("insufficient found")
    #         return False