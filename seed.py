from database import SessionLocal
from models import (
    Category,
    Food,
    Customer,
    RestaurantTable,
    Order,
    OrderItem,
    Payment
)

db = SessionLocal()

# 1. Categories
categories = [
    Category(name="Fast Food", description="Fast food"),
    Category(name="Main Dishes", description="Main dishes"),
    Category(name="Salads", description="Fresh salads"),
    Category(name="Desserts", description="Sweet desserts"),
    Category(name="Drinks", description="Cold drinks"),
]

db.add_all(categories)
db.commit()

# 2. Foods
foods = [
    Food(name="Burger", price=5.99, description="Beef burger", category=categories[0]),
    Food(name="Pizza", price=8.50, description="Cheese pizza", category=categories[1]),
    Food(name="Caesar Salad", price=6.25, description="Chicken salad", category=categories[2]),
    Food(name="Cheesecake", price=4.75, description="Classic cheesecake", category=categories[3]),
    Food(name="Cola", price=2.00, description="Cold drink", category=categories[4]),
]

db.add_all(foods)
db.commit()

# 3. Customers
customers = [
    Customer(fullname="John Smith", phone="+998901111111", email="john@example.com"),
    Customer(fullname="Alex Johnson", phone="+998902222222", email="alex@example.com"),
    Customer(fullname="Michael Brown", phone="+998903333333", email="michael@example.com"),
    Customer(fullname="David Wilson", phone="+998904444444", email="david@example.com"),
    Customer(fullname="Daniel Taylor", phone="+998905555555", email="daniel@example.com"),
]

db.add_all(customers)
db.commit()

# 4. Restaurant Tables
tables = [
    RestaurantTable(table_number=1, capacity=2, is_available=True),
    RestaurantTable(table_number=2, capacity=4, is_available=True),
    RestaurantTable(table_number=3, capacity=4, is_available=False),
    RestaurantTable(table_number=4, capacity=6, is_available=True),
    RestaurantTable(table_number=5, capacity=8, is_available=True),
]

db.add_all(tables)
db.commit()

# 5. Orders
orders = [
    Order(
        customer=customers[0],
        table=tables[0],
        status="completed",
        total_price=5.99
    ),
    Order(
        customer=customers[1],
        table=tables[1],
        status="pending",
        total_price=8.50
    ),
    Order(
        customer=customers[2],
        table=tables[2],
        status="preparing",
        total_price=6.25
    ),
    Order(
        customer=customers[3],
        table=tables[3],
        status="completed",
        total_price=9.50
    ),
    Order(
        customer=customers[4],
        table=tables[4],
        status="pending",
        total_price=2.00
    ),
]

db.add_all(orders)
db.commit()

# 6. Order Items
items = [
    OrderItem(
        order=orders[0],
        food=foods[0],
        quantity=1,
        price=5.99
    ),
    OrderItem(
        order=orders[1],
        food=foods[1],
        quantity=1,
        price=8.50
    ),
    OrderItem(
        order=orders[2],
        food=foods[2],
        quantity=1,
        price=6.25
    ),
    OrderItem(
        order=orders[3],
        food=foods[3],
        quantity=2,
        price=4.75
    ),
    OrderItem(
        order=orders[4],
        food=foods[4],
        quantity=1,
        price=2.00
    ),
]

db.add_all(items)
db.commit()

# 7. Payments
payments = [
    Payment(
        order=orders[0],
        amount=5.99,
        payment_method="cash"
    ),
    Payment(
        order=orders[1],
        amount=8.50,
        payment_method="card"
    ),
    Payment(
        order=orders[2],
        amount=6.25,
        payment_method="card"
    ),
    Payment(
        order=orders[3],
        amount=9.50,
        payment_method="cash"
    ),
    Payment(
        order=orders[4],
        amount=2.00,
        payment_method="card"
    ),
]

db.add_all(payments)
db.commit()

print("5 ta Category yaratildi")
print("5 ta Food yaratildi")
print("5 ta Customer yaratildi")
print("5 ta RestaurantTable yaratildi")
print("5 ta Order yaratildi")
print("5 ta OrderItem yaratildi")
print("5 ta Payment yaratildi")
print("Jami: 35 ta object yaratildi!")

db.close()