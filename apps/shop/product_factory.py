from .product import Electronic, FoodStuffs, Detergent, Clothing, Books, Sports

# by ai
class ProductFactory:
    product_types = {
        'Electronic': Electronic,
        'FoodStuffs': FoodStuffs,
        'Detergent': Detergent,
        'Clothing': Clothing,
        'Books': Books,
        'Sports': Sports
    }

    @staticmethod
    def create_product(product_type, name, cost, inventory=0, ordered=0):
        if product_type in ProductFactory.product_types:
            # by me:
            """
            1-this will return a class, according to the product_type, using the dictionary:
            " ProductFactory.product_types[product_type] "
            2-then we call it with the arguments "name, cost, inventory, ordered"
            3-and it will instantiate a new object of that class
            4-in these classes.__init__ `s, we have the add_to_db method, which will add the product to the database

            """
             
            return ProductFactory.product_types[product_type](name, cost, inventory, ordered)
            
        else:
            raise ValueError("Unknown product type") 
    
    