"""
purpose:
1- integrating modules functionalitis 
2- (and for me: testing some actions like add a user, order a product
    test a method, etc...)
"""
from sys import path
import logging
import typer
from apps.database.managers import user_manager, order_manager
from apps.account.user import StandardUser, AdminUser
from apps.account.auth import *
from apps.shop.product import Product
from apps.shop.order import Order
from apps.shipment.shipment_factory import ShipmentFactory
from apps.shop.product_factory import ProductFactory
from setting import USERS_LOG_PATH
# from apps.utils.functions import log_errors
import csv

# NOTE
# a good interactive cli.you can build good menus.:
# https://github.com/mohammadT77/m98_event

app = typer.Typer(help = "welcome to yegane shop!")

logging.basicConfig(filename=USERS_LOG_PATH, level=logging.ERROR,style='{',
                    # format="%(asctime)s : %(levelname)s : %(message)s")
                    format="{asctime}:{levelname}:{message}")
# by ai
class SimpleSessionManager:
    def __init__(self):
        self.current_user = None

    def login(self, username):
        self.current_user = username
        print(f"{username} is now logged in.")

    def logout(self):
        print(f"{self.current_user} is now logged out.")
        self.current_user = None

    def get_current_user(self):
        return self.current_user

# Create a session manager instance
session_manager = SimpleSessionManager()

@app.command(help= "this is for new users.")
def new_user(username, password, user_role:str= typer.Argument(help= "choose a role admin[a]")):
    try:
        Authenticator.add_user(username, password, user_role)
    except UsernameAlreadyExist as e:
        logging.exception("UsernameAlreadyExist")
    except PasswordTooShort as e:
        logging.exception("PasswordTooShort")

# by ai
@app.command()
def login(username, password):
    try:
        
        if Authenticator.login(username, password):
            session_manager.login(username)
            print(f"Welcome {username}!")
    except UserNotFound:
        print("Invalid username or password")

@app.command(help="Logout from the system")
def logout(username: str):
    """Logout the current user from the system"""
    try:
        if Authenticator.logout(username):
            session_manager.logout()
            print(f"👋 Goodbye {username}! Successfully logged out")
    except (UserNotFound, InvalidUsername) as e:
        print(e)
    except Exception as e:
        print(f"❌ Error during logout: {e}")

        
# by both
@app.command(help="Delete a user (admin only)")
def del_user(admin_username: str, admin_password: str, user_to_delete: str):
    """Delete a user from the system. Only admins can delete standard users."""
    try:
        if Authenticator.delete_user(admin_username, admin_password, user_to_delete):
            print(f"User {user_to_delete} successfully deleted")
    except AccessDenied:
        print("Access denied. Only admins can delete users and cannot delete other admins.")
    except UserNotFound:
        print("Invalid username or password")
    except Exception as e:
        print(f"Error: {e}")


@app.command(help="list of products")
def prods():
    """Shows all product types and their available products"""
    Product.display_all_products()

@app.command(help="Optional arguments ex:\n--inventory=13\nProduct types: Electronic, FoodStuffs, Detergent")
def add_prod(prod_type: str, prod_name: str, cost: float, inventory: int = 0, ordered: int = 0):
    
    try:
        prod = ProductFactory.create_product(prod_type, prod_name, cost, inventory, ordered)
        print(f"{prod_type} product '{prod_name}' added successfully")
    except ValueError as e:
        print(e)


@app.command()
def ord(prod, amount):
    username = session_manager.current_user
    order = Order(username, prod, int(amount))
    

@app.command(help="a dict for print user cart")
def cart(username):
    try:
        print(user_manager.get_cart(username))
    except KeyError as e:
        print(e)

@app.command(help="Finalize orders in the cart and choose shipping method")
def final(username: str, prod: str):
    """Finalize an order and set up shipping"""
    try:
        if not session_manager.get_current_user():
            raise NotLoggedIn("Please login first ⛔")
            
        if session_manager.get_current_user() != username:
            raise AccessDenied("You can only finalize your own orders ⛔")
            
        order_manager.finalize_order(username, prod)
        
    except (ValueError, AccessDenied, NotLoggedIn) as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def add_shipment():
    shipment_type = input("Enter the shipment type (Standard, Express, International): ")
    details = input("Enter shipment details: ")

    try:
        shipment = ShipmentFactory.create_shipment(shipment_type, details)
        print(f"Shipment type {shipment_type} with details {details} has been added.")
    except ValueError as e:
        print(e)



if __name__ == "__main__":
    app()
    

    