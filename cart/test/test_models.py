from django.test import TestCase

# Create your tests here.
from cart.models import Cart, CartItem
from product.models import Product

from django.contrib.auth import get_user_model

User = get_user_model()


class TestCartModels(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="dev@gmail.com", password="dev0123")
        self.user2 = User.objects.create_user(email="test@gmail.com", password="test0123")

        self.cart = Cart.objects.create(cart_user=self.user, cart_state = "Pending", complete=False)
        self.cart2 = Cart.objects.create(cart_user=self.user2, cart_state = "Success", complete=True)

        self.product = Product.objects.create(by_user=self.user, name="product_test1", price=200, discount_price='10')
        self.product2 = Product.objects.create(by_user=self.user, name="product_test2", price=100, discount_price=70)
        self.product3 = Product.objects.create(by_user=self.user2, name="product_test3", price=150, discount_price=50)

        self.cartitem = CartItem.objects.create(product=self.product, cart_id=self.cart, product_quantity=10, cart_item_state="Pending")
        self.cartitem2 = CartItem.objects.create(product=self.product2, cart_id=self.cart, product_quantity=10, cart_item_state="Success")
        self.cartitem3 = CartItem.objects.create(product=self.product3, cart_id=self.cart2, product_quantity=1, cart_item_state="Pending")

    
    def test_cart_number(self):
        self.assertEqual(Cart.objects.all().count(), 2)

    def test_cart_user(self):
        self.assertEqual(self.cart.cart_user.email, "dev@gmail.com")

    def test_cart_state(self):
        self.assertFalse(self.cart.complete)
        self.assertTrue(self.cart2.complete)
        

    def test_cart_state_count(self):
        self.assertEqual(Cart.objects.filter(complete = False).count(), 1)
        self.assertEqual(Cart.objects.filter(complete = True).count(), 1)

    
    def test_cartitem_number_relate_to_specifique_cart_count(self):
        cart_item = CartItem.objects.filter(cart_id=self.cart)
        self.assertEqual(cart_item.count(), 2)

    def test_cart_item_relate_to_cart(self):
        cart_item = self.cartitem.cart_id
        self.assertEqual(cart_item, self.cart)

    def test_cart_item_relate_to_cart_reverse_relation(self):
        cart_item =self.cart.cartitem_set.filter(cart_id = self.cart)
        self.assertEqual(cart_item.get(product__name = self.cartitem), self.cartitem)


    def test_cart_item_state(self):
        cart_item_pending = CartItem.objects.filter(cart_item_state = "Pending").count()
        cart_item_success = CartItem.objects.filter(cart_item_state = "Success").count()

        self.assertEqual(cart_item_pending, 2)
        self.assertEqual(cart_item_success, 1)

    
    def test_cart_total_cost(self):
        self.assertEqual(self.cart.cart_total_cost, 2200)

    
    def test_cart_item_products_cost(self):
        self.assertEqual(self.cartitem.cart_item_total_cost, 1500)

    
    def test_product_finally_price(self):
        finally_price = self.product.product_finaly_price
        self.assertNotEqual(self.product2.product_finaly_price, 100)
        self.assertEqual(finally_price, 150)