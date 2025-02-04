"""
purpose:
1- creating instances of file managers
2- preventing circular imports
"""

from apps.database.file_handler import UserFileManager, ProductFileManager, OrderFileManager
from setting import DIRS

# by ai
# Create manager instances
user_manager = UserFileManager(DIRS["USERS_CARTS_PATH"], "users_file")
product_manager = ProductFileManager(DIRS["PRODUCTS_DATA_PATH"], "products_file") 
order_manager = OrderFileManager(DIRS["USERS_CARTS_PATH"], "orders_file") 