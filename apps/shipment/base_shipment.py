from abc import  ABC, abstractmethod
from apps.utils.functions import generate_random_code

class Shipment(ABC):
    def __init__(self, delivey_time):
        self.delivery_time = delivey_time
        self.tracking_id = generate_random_code()

    @abstractmethod
    def get_details(self):  
        pass


class ExpressShipment(Shipment):
    cost = 10
    def get_details(self):
        pass

class StandardShipment(Shipment):
    cost = 20
    def get_details(self):
        pass

class InternationalShipment(Shipment):
    cost = 40
    def get_details(self):
        pass






