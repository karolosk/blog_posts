class Inventory:

    def check_inventory(self):
        print("Inventory Checked")

class Payment:

    def proccess_payment(self):
        print("Payment completed")


class OrderFacade:

    def __init__(self):
        self.inventory = Inventory()
        self.payment = Payment() 

    def procces_order(self):
        self.inventory.check_inventory()
        self.payment.proccess_payment()
        print("Order completed")




def main():
    order = OrderFacade()
    order.procces_order()

main()