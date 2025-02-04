from .base_shipment import StandardShipment, ExpressShipment, InternationalShipment

# BY AI      
class ShipmentFactory:
    @staticmethod
    def create_shipment(shipment_type, details):
        if shipment_type == 'Standard':
            return StandardShipment(details)
        elif shipment_type == 'Express':
            return ExpressShipment(details)
        elif shipment_type == 'International':
            return InternationalShipment(details)
        else:
            raise ValueError("Unknown shipment type")