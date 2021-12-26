from models.abstract_product import AbstractProduct


class Coffee(AbstractProduct):
    def __init__(self, variety='none', capacity=0, packing='none', producer='none',
                 roasting='none', price=0):
        super().__init__(variety, capacity, packing, producer,
                         roasting, price)


def __str__(self):
    return "Variety of coffee: " + str(self.variety) + "\n" \
           "Capacity in mL: " + str(self.capacity) + "\n" \
           "Packing of coffee: " + str(self.packing) + "\n" \
           "Producer: " + str(self.producer) + "\n" \
           "Type of roasting: " + str(self.roasting) + "\n" \
           "Price in UAH: " + str(self.price) + "\n"
