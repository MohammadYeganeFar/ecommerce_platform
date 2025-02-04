"""
purpose:
1- creating varius products


"""
from abc import ABC, abstractmethod
import sys
import csv
from apps.database.managers import product_manager
# from apps.utils.functions import log_order
from setting import DIRS


class Product:
    def __init__(self, name,  cost, inventory=0, ordered=0):
        self.name = name
        self.inventory = inventory
        self.cost = cost
        self.ordered = ordered
        self.add_to_db()

    @product_manager.add_product
    def add_to_db(self):
        return [type(self).__name__,self.name,self.cost,self.inventory,self.ordered]
    
    def get_detail(self):
        pass
    
    @staticmethod
    def display_all_products():
        """Shows all product types and their available products with detailed formatting"""
        try:
            with open(DIRS["PRODUCTS_DATA_PATH"], 'r') as file:
                reader = csv.DictReader(file)
                products_by_type = {}
                
                # Group products by their type
                for row in reader:
                    category = row['categori']
                    if category not in products_by_type:
                        products_by_type[category] = []
                    products_by_type[category].append({
                        'name': row['product'],
                        'cost': float(row['cost']),
                        'inventory': int(row['inventory']),
                        'description': row['description'],
                        'last_update': row['last_update']
                    })

            # Print all product types and their products
            print("\n🏪 Welcome to Our Store! 🏪")
            print("=" * 80)
            from apps.shop.product_factory import ProductFactory
            
            for category in ProductFactory.product_types.keys():
                print(f"\n📦 {category.upper()} PRODUCTS:")
                print("-" * 80)
                if category in products_by_type:
                    for product in products_by_type[category]:
                        print(f"""
  🔸 {product['name']}
     💰 Price: ${product['cost']:,.2f}
     📦 In Stock: {product['inventory']} units
     📝 Description: {product['description']}
     🕒 Last Updated: {product['last_update']}
        """)
                else:
                    print("  • No products available in this category yet")
                print("-" * 80)
                    
        except Exception as e:
            print(f"❌ Error reading products: {e}")

class Clothing(Product):
    """For clothing items like shirts, pants, etc."""
    pass

class Books(Product):
    """For books, magazines, and other reading materials"""
    pass

class Sports(Product):
    """For sports equipment and accessories"""
    pass

class Electronic(Product):
    pass

class FoodStuffs(Product):
    pass

class Detergent(Product):
    pass


