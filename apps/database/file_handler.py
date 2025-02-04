import json
import csv
from os import path
from abc import ABC, abstractmethod
from sys import path
from pandas import read_csv
from setting import DIRS

"""
purpose:
1- file handilng for different procceses(authentication , production)


"""
# NOTE:


class FileManager(ABC):
    def __init__(self,  file_path, file_name):
        self.__file_path = file_path
        self.file_name = file_name


    # a getter for get file name;
    @property
    def file_path(self):
        return self.__file_path
        
    # a setter to set it
    @file_path.setter
    def file_path(self, path):
        self.__file_path = path
        
##########################################


class UserFileManager(FileManager):
    def __init__(self, file_path, file_name):
        super().__init__(file_path, file_name)
        self.product_manager = ProductFileManager(DIRS["PRODUCTS_DATA_PATH"], "products_file")

    def add_user(self, func):
        # adding new user to file
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            with open(DIRS["USERS_DATA_PATH"], "a") as file:
                # data = [username, role, logged_in, encrypted_password]
                file.write(f"\n{data[0]},{data[1]},{data[2]},{data[3]}")
        return wrapper

    def set_status(self, username, status: bool ):
        with open(DIRS["USERS_DATA_PATH"], "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    row["logged_in"] = True


    def add_to_user_cart(self, username, prod, amount: int):
        prod_cost = self.product_manager.get_detail(prod, "cost")
        
        #1- coping json file content
        with open(DIRS["USERS_CARTS_PATH"], "r") as f:
            data = json.load(f)

        #2- editing content witj new data
            data[username]["cart"][prod] = {
                "amount": amount,
                "cost": prod_cost,
                "tot cost": amount * prod_cost
            }

        #3- returning updated content to file
        with open(DIRS["USERS_CARTS_PATH"], "w") as f:
            json.dump(data, f, indent=4)

    def get_cart(self, username):
        with open(DIRS["USERS_CARTS_PATH"], "r") as f:
            data = json.load(f)
            return data[username]["cart"]


##############################################
class ProductFileManager(FileManager):
    FILE_TYPE = "csv"
    
    def __init__(self, file_path, file_name):
        super().__init__(file_path, file_name)

    def add_product(self, func):
        def wrapper(*args, **kwargs):
            row = func(*args, **kwargs)
            with open(DIRS["PRODUCTS_DATA_PATH"], "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(row)
        return wrapper


    # def read_file(self, func):
    #     def wrapper(*args, **kwargs):
    #         if path.exists(DIRS["PRODUCTS_DATA_PATH"]):
    #             with open(DIRS["PRODUCTS_DATA_PATH"], "r") as f:
    #                 func()
    #         else:
    #             print("file not found!")
    #     return wrapper

    def exists(self, prod):
        with open(DIRS["PRODUCTS_DATA_PATH"], "r") as f:
            reader = csv.DictReader(f)
            return any(row["product"] == prod for row in reader)
    
    def get_detail(self, prod, detail: str):
        with open(DIRS["PRODUCTS_DATA_PATH"], "r") as f:
            data = csv.DictReader(f)
            for row in data:
                if row["product"] == prod:
                    try:
                        return int(row[detail])
                    except ValueError:
                        return row[detail]
    def all_detail(self, prod):
        with open(DIRS["PRODUCTS_DATA_PATH"], "r") as f:
            data = csv.DictReader(f)
            for row in data:
                if row["product"] == prod:
                    return row

#####################################              
class OrderFileManager(FileManager):
    def __init__(self, file_path, file_name):
        super().__init__(file_path, file_name)

    def add_order(self, func):
        def wrapper(username, product):
            data = func(username, product)
            if path.exists(DIRS["USERS_CARTS_PATH"]):
                with open(DIRS["USERS_CARTS_PATH"], "r+") as file:
                    f_content = json.load(file)
                    f_content[username].append(product)
                    file.seek(0)
                    json.dump(f_content, file, indent=4)
            else:
                print("file not found : DIRS['USERS_CARTS_PATH']")
        return wrapper


    # def read_file(self, func):
    #     def wrapper(*args, **kwargs):
    #         if path.exists(DIRS["PRODUCTS_DATA_PATH"]):
    #             with open(DIRS["PRODUCTS_DATA_PATH"], "r") as f:
    #                 func()
    #         else:
    #             print("file not found!")
    #     return wrapper
    
    def finalize_order(self, username, prod):
        with open(DIRS["USERS_CARTS_PATH"], "r") as f:
            data = json.load(f)
            
            # Get product from cart
            prods_in_cart = data[username]["cart"]
            if prod not in prods_in_cart:
                raise ValueError(f"Product '{prod}' not found in cart")
            
            prod_data = prods_in_cart.pop(prod)
            
            # Create shipment
            from apps.shipment.shipment_factory import ShipmentFactory
            print("\n📦 Choose shipping method:")
            print("1. Standard Shipping ($20)")
            print("2. Express Shipping ($10)")
            print("3. International Shipping ($40)")
            
            choice = input("\nEnter your choice (1-3): ")
            shipping_types = {
                "1": "Standard",
                "2": "Express",
                "3": "International"
            }
            
            if choice not in shipping_types:
                raise ValueError("Invalid shipping choice")
                
            shipping_type = shipping_types[choice]
            delivery_time = input("Enter desired delivery date (YYYY-MM-DD): ")
            
            shipment = ShipmentFactory.create_shipment(shipping_type, delivery_time)
            
            # Add shipment details to order
            prod_data["shipping"] = {
                "method": shipping_type,
                "delivery_time": delivery_time,
                "tracking_id": shipment.tracking_id,
                "cost": shipment.cost
            }
            
            # Add to finalized orders
            data[username]["finalized"][prod] = prod_data
            
            # Save updated data
            with open(DIRS["USERS_CARTS_PATH"], "w") as f:
                json.dump(data, f, indent=4)
                
            print(f"\n✅ Order finalized successfully!")
            print(f"🔍 Tracking ID: {shipment.tracking_id}")
            print(f"💰 Shipping Cost: ${shipment.cost}")
            print(f"📅 Expected Delivery: {delivery_time}")





#https://www.online-python.com/DAye3BnozI

#     def write(self, data):
#         try:

#             validate_data = convert_to_array(data)
#             file_exists = os.path.exists(self.__file_name)
#             with open(self.__file_name, mode='a', newline='', encoding='utf-8') as csvfile:
#                 writer = csv.writer(csvfile)
#                 if not file_exists or os.path.getsize(self.__file_name) == 0:
#                     writer.writerow(validate_data[2]) 
                
#                 writer.writerow(validate_data[1])   
#             return True 
#         except Exception as e:
#             self.loger.log(str(e))
#             return False
 
 
 
#  from dataclasses import dataclass, asdict
# @dataclass
# class UserData:
#     user_id: int
#     first_name: str
#     last_name: str
#     email: str
#     password: str
#     permission: str
#     login_status: bool
        
# def convert_to_array(data):
#     #conver data class to dict
#     new_data_dict = asdict(data) 
#     new_data_list = list(new_data_dict.values())
#     return new_data_dict, new_data_list, list(new_data_dict.keys())

        