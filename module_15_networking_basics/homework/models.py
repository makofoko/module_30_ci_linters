class Room:
    def __init__(self, roomId, floor, beds, guestNum, price):
        self.roomId = roomId
        self.floor = floor
        self.beds = beds
        self.guestNum = guestNum
        self.price = price

    def to_dict(self):
        return {
            "roomId": self.roomId,
            "floor": self.floor,
            "beds": self.beds,
            "guestNum": self.guestNum,
            "price": self.price
        }