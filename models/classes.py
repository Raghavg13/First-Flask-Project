class User:
    def __init__(self, name: str, marks: int, roll_number: int, address: str):
        self.name = name
        self.marks = marks
        self.roll_number = roll_number
        self.address = address

    def to_dict(self):
        return {
            'name': self.name,
            'marks': self.marks,
            'roll_number': self.roll_number,
            'address': self.address
        }

    @staticmethod
    def from_dict(user_dict: dict):
        return User(
            name=str(user_dict.get('name')),
            marks=int(user_dict.get('marks')),
            roll_number=int(user_dict.get('roll_number')),
            address=str(user_dict.get('address'))
        )
