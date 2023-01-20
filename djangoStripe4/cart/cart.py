"""Create a cart class here with methods add, update and remove"""


from core.models import Product

from django.conf import settings

class Cart(object):
    """Creating a cart class"""
    def __init__(self, request):
        """Initializing a cart session for this object"""
        self.session = request.session # a session for cart object
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            """If cart does not exist we create a cart session"""
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def __iter__(self):
        """Loop through the product whenever the cart oject is accessed"""
        for pk in self.cart.keys():
            self.cart[str(pk)]['product'] = Product.objects.get(pk=pk)
        for item in self.cart.values():
            item['total_price'] = int(item['product'].price * item['quantity']) / 100
            print(item)
            yield item


    def __len__(self):
        """returns the total numbers of items in the cart"""
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        """Saving the cart session"""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    

    def add(self, product_id, quantity=1):
        """Adding or updating the products to the cart in index or product detail page only"""
        product_id = str(product_id) # converting into string to ease its use 

        if product_id not in self.cart:
            """If items is not in the cart then add item to cart"""
            self.cart[product_id] = {'quantity':1, 'id':product_id}
            self.save()
            return

        if product_id in self.cart:
            """adding the quantity of items if alreadly exist"""
            self.cart[product_id]['quantity'] += int(quantity)
        self.save()
    
    def update(self, product_id, quantity=1, update_quantity=False):
        """Update item in cart view only"""
        product_id = str(product_id)
        if product_id in self.cart:
            if update_quantity:
                self.cart[product_id]['quantity'] += int(quantity)

                if self.cart[product_id]['quantity'] == 0:
                    self.remove(product_id)
            self.save()
    
    def remove(self, product_id):
        """This method is to remove the products from the cart"""
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def get_total_amount(self):
        """Returns total amount of prices"""
        for pk in self.cart.keys():
            self.cart[str(pk)]['product'] = Product.objects.get(id=pk)
        
        return int(sum(item['product'].price * item['quantity'] for item in self.cart.values()))
