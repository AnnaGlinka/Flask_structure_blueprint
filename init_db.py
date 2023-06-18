from app.extensions import db

from app.models.category import Category
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import Order_Item

db.drop_all()
db.create_all()

cat1 = Category(name='Milk products')
cat2 = Category(name='Fruit')
cat3 = Category(name='Vegetables')

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

ord1 = Order(total_price="100", status="Pending")
ord2 = Order(total_price="200", status="Pending")
ord3 = Order(total_price="200", status="Pending")

ord_item_1 = Order_Item(quantity=1, price=1, product_id=1, order_id=1)
ord_item_2 = Order_Item(quantity=2, price=2, product_id=2, order_id=1)

ord_item_3 = Order_Item(quantity=3, price=3, product_id=3, order_id=2)
ord_item_4 = Order_Item(quantity=4, price=4, product_id=4, order_id=2)

db.session.add_all([cat1, cat2, cat3])
db.session.add_all([prod1, prod2, prod3, prod4, prod5])
db.session.add_all([ord1, ord2, ord3])
db.session.add_all([ord_item_1, ord_item_2, ord_item_3, ord_item_4])

db.session.commit()
