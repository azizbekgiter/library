class CarFactory:
    def create_car(self, car_type):
        if car_type == "sedan":
            return Sedan()
        elif car_type == "pickup":
            return Pickup()


class Sedan:
    def __str__(self):
        return "Sedan avtomobil"


class Pickup:
    def __str__(self):
        return "Pickup avtomobil"


# Zavoddan foydalanish
factory = CarFactory()
car = factory.create_car("pickup")
ca2 = factory.create_car("sedan")
print(car)  # Pickup avtomobil
print(ca2)
