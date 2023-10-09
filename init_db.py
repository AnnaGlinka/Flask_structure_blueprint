
# flask shell

from app.extensions import db
from app.models.category import Category
from app.models.product import Product
from app.models.customer import Customer
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.payment import Payment
from app.models.shipment import Shipment
from app.models.cart import Cart

db.drop_all()
db.create_all()

# Create Product Categories ------------------------------------------------
cat1 = Category(name='Milk products', description='Lorem ipsum dolor sit amet, '
                                                  'consetetur sadipscing elitr, '
                                                  'sed diam nonumy eirmod tempor invidunt ut '
                                                  'labore et dolore magna aliquyam erat, '
                                                  'sed diam voluptua.')

cat2 = Category(name='Fruit', description='Lorem ipsum dolor sit amet, '
                                                  'consetetur sadipscing elitr, '
                                                  'sed diam nonumy eirmod tempor invidunt ut '
                                                  'labore et dolore magna aliquyam erat, '
                                                  'sed diam voluptua.')
cat3 = Category(name='Vegetables', description='Lorem ipsum dolor sit amet, '
                                                  'consetetur sadipscing elitr, '
                                                  'sed diam nonumy eirmod tempor invidunt ut '
                                                  'labore et dolore magna aliquyam erat, '
                                                  'sed diam voluptua.')

# Create Products ----------------------------------------------------
prod1 = Product(name="strawberry yogurt",
                description="strawberry yogurt with fresh strawberries",
                price=10,
                stock=10,
                category_id=1)
prod2 = Product(name="Milk",
                description="UHT milk",
                price=10,
                stock=10,
                category_id=1)

prod3 = Product(name="Orange ",
                description="Fresh orange",
                price=10,
                stock=10,
                category_id=2)

prod4 = Product(name="Apple",
                description="Fresh apple",
                price=10,
                stock=10,
                category_id=2)

prod5 = Product(name="Cabbage",
                description="Fresh cabbage",
                price=10,
                stock=10,
                category_id=3)

# Create Customers ----------------------------------------------------
cust1 = Customer(first_name="Maria",
                 last_name="Cortes",
                 email="maria@gmail.com",
                 address="Cin City",
                 phone_number="124343344")

cust2 = Customer(first_name="Gloria",
                 last_name="Ramirez",
                 email="gloria@gmail.com",
                 address="Warsaw, Sloneczna 2/3",
                 phone_number="7330344")

cust3 = Customer(first_name="Marek",
                 last_name="Turing",
                 email="marek@gmail.com",
                 address="Cracow, Milkowskigo 3",
                 phone_number="15343344")

cust4 = Customer(first_name="Michal",
                 last_name="Turing",
                 email="Michal@gmail.com",
                 address="Cracow, Leya 3",
                 phone_number="1534334444")

# Create Payments ----------------------------------------------------
payment1 = Payment(payment_method="cash", amount=100, status="Pending", customer_id=1)
payment2 = Payment(payment_method="credit card", amount=200, status="Pending", customer_id=2)
payment3 = Payment(payment_method="credit card", amount=200, status="Pending", customer_id=4)

# Create Shipment ----------------------------------------------------------

ship1 = Shipment(country="Poland", city="Cracow", postal_code="30-313",
                 street="Makowskiego", house_number=23, apartment_number=4,
                 shipment_cost=10, status="Pending",
                 customer_id=1)

ship2 = Shipment(country="Poland", city="Warsaw", postal_code="10-113",
                 street="Warszawska", house_number=123, apartment_number=66,
                 shipment_cost=10, status="Pre-Transit",
                 customer_id=2)

ship3 = Shipment(country="Germany", city="Hamburg", postal_code="100-13",
                 street="Havelstrasse", house_number=13, apartment_number=76,
                 shipment_cost=10, status="Out for deliver",
                 customer_id=3)

ship4 = Shipment(country="Poland", city="Warsaw", postal_code="100-13",
                 street="Kolorowa", house_number=123, apartment_number=676,
                 shipment_cost=10, status="In Transit",
                 customer_id=4)


# Create Orders ----------------------------------------------------
ord1 = Order(total_price="100", status="Pending", customer_id=1, payment_id=1, shipment_id=1)
ord2 = Order(total_price="200", status="Pending", customer_id=2, payment_id=2, shipment_id=2)
ord3 = Order(total_price="200", status="Pending", customer_id=4, payment_id=3, shipment_id=3)

# Create Order Items ----------------------------------------------------

ord_item_1 = OrderItem(quantity=1, price=1, product_id=1, order_id=1)
ord_item_2 = OrderItem(quantity=2, price=2, product_id=2, order_id=1)
ord_item_3 = OrderItem(quantity=3, price=3, product_id=3, order_id=2)
ord_item_4 = OrderItem(quantity=4, price=4, product_id=4, order_id=2)

# Create Carts ----------------------------------------------------
cart1 = Cart(quantity=1, customer_id=1, product_id=1)
cart2 = Cart(quantity=2, customer_id=2, product_id=2)
cart3 = Cart(quantity=3, customer_id=3, product_id=3)

db.session.add_all([cat1, cat2, cat3])
db.session.add_all([prod1, prod2, prod3, prod4, prod5])
db.session.add_all([cust1, cust2, cust3, cust4])
db.session.add_all([payment1, payment2, payment3])
db.session.add_all([ord1, ord2, ord3])
db.session.add_all([ord_item_1, ord_item_2, ord_item_3, ord_item_4])
db.session.add_all([ship1, ship2, ship3, ship4])
db.session.add_all([cart1, cart2, cart3])


db.session.commit()
