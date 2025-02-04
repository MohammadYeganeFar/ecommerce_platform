# https://www.online-python.com/IgJz2iFhTO


import os
import pathlib
import json

# Base directory of the project
# with os module:
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#____

# with pathlib module
BASE_DIR = pathlib.Path(__file__).resolve().parent

DATABASE_DIR = os.path.join(BASE_DIR, "apps", "database")

DATA_DIR = os.path.join(DATABASE_DIR, "data")

USERS_DATA_PATH = os.path.join(DATA_DIR, "users_data.csv")

USERS_CARTS_PATH = os.path.join(DATA_DIR, "users_carts.json")

PRODUCTS_DATA_PATH = os.path.join(DATA_DIR, "products_data.csv")

USERS_LOG_PATH = os.path.join(DATA_DIR, "users_log.log")

SHIPMENT_LOG_PATH = os.path.join(DATA_DIR, "shipment_log.txt")

ERRORS_LOG_PATH = os.path.join(DATA_DIR, "errors_log.txt")

PERFORMANCE_LOG = os.path.join(DATA_DIR, "performance_log.txt")                              

ORDERS_LOG_PATH = os.path.join(DATA_DIR, "orders_log.txt")                              


DIRS = {
    "BASE_DIR" : BASE_DIR,
    "DATABASE_DIR" : DATABASE_DIR,
    "DATA_DIR" : DATA_DIR, 
    "USERS_DATA_PATH" :USERS_DATA_PATH,
    "PRODUCTS_DATA_PATH" : PRODUCTS_DATA_PATH,
    "USERS_LOG_PATH" : USERS_LOG_PATH,
    "SHIPMENT_LOG_PATH" : SHIPMENT_LOG_PATH,
    "ERRORS_LOG_PATH" : ERRORS_LOG_PATH,
    "ERRORS_LOG_PATH" : ERRORS_LOG_PATH,
    "PERFORMANCE_LOG" : PERFORMANCE_LOG,
    "ORDERS_LOG_PATH" : ORDERS_LOG_PATH,
    "USERS_CARTS_PATH" : USERS_CARTS_PATH,











}


# print(f"Base directory: {BASE_DIR}")
# # Path to the 'data/json' folder
# DATA_DIR = os.path.join(BASE_DIR, 'apps', 'database', 'data', 'json')
# print("data dir: ", DATA_DIR)
# # Path to the JSON file
# USERS_DATABASE_FILE = os.path.join(DATA_DIR, 'users_database.json')
# PRODUCTS_DATABASE_FILE = os.path.join(DATA_DIR, 'products_database.json')
# databases = [USERS_DATABASE_FILE, PRODUCTS_DATABASE_FILE]
# # Ensures the data/json folder exists
# os.makedirs(DATA_DIR, exist_ok=True)

# # Ensure the users_database.json exists or initialise an empty dictionary
# for database in databases:
#     if not os.path.exists(database):
#         with open(database, 'w') as file:
#             json.dump({}, file)
