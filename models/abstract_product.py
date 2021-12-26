class AbstractProduct:

    def __init__(self, variety='none', capacity=0, packing='none', producer='none',
                 roasting='none', price=0):
        self.variety = variety
        self.capacity = capacity
        self.packing = packing
        self.producer = producer
        self.roasting = roasting
        self.price = price
