class Restaurant:
    
    
    
    def __init__(self):
        self.customer_order = []
        self.book_table = []
    
    
    def menu_item(self):
        n = int(input("enter the no of item you want to eat :"))
        print("""enter the dish you want eat here : 
              
              Gujarati Restaurant Menu
                1.Chaas (Buttermilk)
                2.Aam Panna (Raw Mango Drink)
                3.Jaljeera
                4.Fafda with Kadhi
                5.Khaman Dhokla
                6.Patra (Colocasia Leaves Roll)
                7.Methi Na Gota (Fenugreek Fritters)
                8.Handvo (Savory Lentil cake)""")
                       
           
        for i in range(1,n+1):
            a = input(f"enter the item {i} : ")
            self.customer_order.append(a)
            print(self.customer_order)
    
            
            
    def book_table():
     pass

    def customer_order(self):
       pass
   
   
h = Restaurant()
h.menu_item()