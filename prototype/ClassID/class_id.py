class ID:
    number = 0

    def __init__(self):
        self.id = ID.number
        ID.number += 1

    def appropriation_id(self):
        return self.id
