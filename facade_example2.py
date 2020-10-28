class Hotel:

    def get_available_hotels(self):
        print("Hotels available at the moment: Hitlon, Best Western")


class Flight:

    def get_flights(self):
        print("Flights every day at 06:00 and 20:00")


class Transfer:
    
    def get_transfers(self):
       print("Not Available")

class TravelFacade:

    def __init__(self):
        self.hotel = Hotel()
        self.flight = Flight() 
        self.trasnfer = Transfer()

    def check_availability(self):
        self.hotel.get_available_hotels()
        self.flight.get_flights()
        self.trasnfer.get_transfers()
        print("Search Completed")


def main():
    travel = TravelFacade()
    travel.check_availability()

main()