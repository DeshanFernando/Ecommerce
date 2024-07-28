from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        # get request for user identification
        self.request = request

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #make sure cart is available in all pages
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)


        if product_id not in self.cart:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            # convert cart dictionary to str cause old_cart field is type of str
            carty = str(self.cart)
            carty = carty.replace("'", "\"")

            # update profile with cart
            current_user.update(old_cart=carty)




    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0

        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += (product.sale_price * value)
                    else:
                        total += (product.price * value)

        return total


    def __len__(self):
        return len(self.cart)
    

    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products
    

    def get_quants(self):
        quantities = self.cart
        return quantities
    

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        self.cart[product_id] = int(product_qty)

        self.session.modified = True

    
    def delete(self, product):
        product_id = str(product)

        if  product_id in self.cart:
            self.cart.pop(product_id)

        self.session.modified = True


    

    




    
