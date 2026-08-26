from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import *
from models import *
from schemes import *


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restaurant Order Management System",
    description=(
        "API for managing restaurant categories, foods, customers, "
        "restaurant tables, orders, order items and payments."
    ),
    version="1.0.0"
)


# ============================================================
# CATEGORIES
# ============================================================

@app.post(
    "/categories",
    response_model=CategoryResponse,
    summary="Create a category",
    description="Creates a new food category in the restaurant system."
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    new_category = Category(
        **category.model_dump()
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@app.get(
    "/categories",
    response_model=List[CategoryResponse],
    summary="Get all categories",
    description="Returns a list of all food categories."
)
def get_categories(
    db: Session = Depends(get_db)
):
    return db.query(Category).all()


@app.get(
    "/categories/{category_id}",
    response_model=CategoryResponse,
    summary="Get category by ID",
    description="Returns detailed information about a specific category."
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category


@app.put(
    "/categories/{category_id}",
    response_model=CategoryResponse,
    summary="Update category",
    description="Updates the information of an existing food category."
)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    for key, value in category_data.model_dump(
        exclude_unset=True
    ).items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)

    return category


@app.delete(
    "/categories/{category_id}",
    summary="Delete category",
    description="Deletes an existing food category."
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    db.delete(category)
    db.commit()

    return {
        "message": "Category deleted"
    }


# ============================================================
# FOODS
# ============================================================

@app.post(
    "/foods",
    response_model=FoodResponse,
    summary="Create food",
    description=(
        "Creates a new food item. "
        "The specified category must exist and the price must be greater than zero."
    )
)
def create_food(
    food: FoodCreate,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == food.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    if food.price <= 0:
        raise HTTPException(
            status_code=400,
            detail="Price must be greater than 0"
        )

    new_food = Food(
        **food.model_dump()
    )

    db.add(new_food)
    db.commit()
    db.refresh(new_food)

    return new_food


@app.get(
    "/food",
    response_model=List[FoodResponse],
    summary="Get all foods",
    description="Returns a list of all food items in the restaurant."
)
def get_foods(
    db: Session = Depends(get_db)
):
    return db.query(Food).all()


@app.get(
    "/foods/{food_id}",
    response_model=FoodResponse,
    summary="Get food by ID",
    description="Returns detailed information about a specific food item."
)
def get_food(
    food_id: int,
    db: Session = Depends(get_db)
):
    food = db.query(Food).filter(
        Food.id == food_id
    ).first()

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Food not found"
        )

    return food


@app.put(
    "/foods/{food_id}",
    response_model=FoodResponse,
    summary="Update food",
    description=(
        "Updates an existing food item. "
        "The selected category must exist and the price must be greater than zero."
    )
)
def update_food(
    food_id: int,
    food_data: FoodUpdate,
    db: Session = Depends(get_db)
):
    food = db.query(Food).filter(
        Food.id == food_id
    ).first()

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Food not found"
        )

    category = db.query(Category).filter(
        Category.id == food_data.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    if food_data.price <= 0:
        raise HTTPException(
            status_code=400,
            detail="Price must be greater than 0"
        )

    for key, value in food_data.model_dump(
        exclude_unset=True
    ).items():
        setattr(food, key, value)

    db.commit()
    db.refresh(food)

    return food


@app.delete(
    "/foods/{food_id}",
    summary="Delete food",
    description="Deletes an existing food item from the restaurant."
)
def delete_food(
    food_id: int,
    db: Session = Depends(get_db)
):
    food = db.query(Food).filter(
        Food.id == food_id
    ).first()

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Food not found"
        )

    db.delete(food)
    db.commit()

    return {
        "message": "Food deleted"
    }


# ============================================================
# CUSTOMERS
# ============================================================

@app.post(
    "/customers",
    response_model=CustomerResponse,
    summary="Create customer",
    description="Creates a new restaurant customer."
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    new_customer = Customer(
        **customer.model_dump()
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


@app.get(
    "/customers",
    response_model=List[CustomerResponse],
    summary="Get all customers",
    description="Returns a list of all registered customers."
)
def get_customers(
    db: Session = Depends(get_db)
):
    return db.query(Customer).all()


@app.get(
    "/customers/{customer_id}",
    response_model=CustomerResponse,
    summary="Get customer by ID",
    description="Returns detailed information about a specific customer."
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


@app.put(
    "/customers/{customer_id}",
    response_model=CustomerResponse,
    summary="Update customer",
    description=(
        "Updates an existing customer's information. "
        "The email address must be unique."
    )
)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    existing_customer = db.query(Customer).filter(
        Customer.email == customer_data.email,
        Customer.id != customer_id
    ).first()

    if existing_customer:
        raise HTTPException(
            status_code=400,
            detail="Customer with this email already exists"
        )

    for key, value in customer_data.model_dump(
        exclude_unset=True
    ).items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)

    return customer


@app.delete(
    "/customers/{customer_id}",
    summary="Delete customer",
    description="Deletes an existing customer."
)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.delete(customer)
    db.commit()

    return {
        "message": "Customer deleted"
    }


# ============================================================
# RESTAURANT TABLES
# ============================================================

@app.post(
    "/restaurant_tables",
    response_model=RestaurantTableResponse,
    summary="Create restaurant table",
    description=(
        "Creates a new restaurant table. "
        "The table number must be unique and capacity must be greater than zero."
    )
)
def create_restaurant_table(
    restaurant_table: RestaurantTableCreate,
    db: Session = Depends(get_db)
):
    existing_table = db.query(RestaurantTable).filter(
        RestaurantTable.table_number ==
        restaurant_table.table_number
    ).first()

    if existing_table:
        raise HTTPException(
            status_code=400,
            detail="Table number already exists"
        )

    if restaurant_table.capacity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Capacity must be greater than 0"
        )

    new_restaurant_table = RestaurantTable(
        **restaurant_table.model_dump()
    )

    db.add(new_restaurant_table)
    db.commit()
    db.refresh(new_restaurant_table)

    return new_restaurant_table


@app.get(
    "/restaurant_tables",
    response_model=List[RestaurantTableResponse],
    summary="Get all restaurant tables",
    description="Returns all restaurant tables and their availability status."
)
def get_restaurant_tables(
    db: Session = Depends(get_db)
):
    return db.query(RestaurantTable).all()


@app.get(
    "/restaurant_tables/{restaurant_table_id}",
    response_model=RestaurantTableResponse,
    summary="Get restaurant table by ID",
    description="Returns detailed information about a specific restaurant table."
)
def get_restaurant_table(
    restaurant_table_id: int,
    db: Session = Depends(get_db)
):
    restaurant_table = db.query(RestaurantTable).filter(
        RestaurantTable.id == restaurant_table_id
    ).first()

    if not restaurant_table:
        raise HTTPException(
            status_code=404,
            detail="Restaurant table not found"
        )

    return restaurant_table


@app.put(
    "/restaurant_tables/{restaurant_table_id}",
    response_model=RestaurantTableResponse,
    summary="Update restaurant table",
    description=(
        "Updates an existing restaurant table. "
        "The table number must remain unique and capacity must be greater than zero."
    )
)
def update_restaurant_table(
    restaurant_table_id: int,
    restaurant_table_data: RestaurantTableUpdate,
    db: Session = Depends(get_db)
):
    restaurant_table = db.query(RestaurantTable).filter(
        RestaurantTable.id == restaurant_table_id
    ).first()

    if not restaurant_table:
        raise HTTPException(
            status_code=404,
            detail="Restaurant table not found"
        )

    existing_restaurant_table = db.query(
        RestaurantTable
    ).filter(
        RestaurantTable.table_number ==
        restaurant_table_data.table_number,
        RestaurantTable.id != restaurant_table_id
    ).first()

    if existing_restaurant_table:
        raise HTTPException(
            status_code=400,
            detail="Table number already exists"
        )

    if restaurant_table_data.capacity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Capacity must be greater than 0"
        )

    for key, value in restaurant_table_data.model_dump(
        exclude_unset=True
    ).items():
        setattr(restaurant_table, key, value)

    db.commit()
    db.refresh(restaurant_table)

    return restaurant_table


@app.delete(
    "/restaurant_tables/{restaurant_table_id}",
    summary="Delete restaurant table",
    description="Deletes an existing restaurant table."
)
def delete_restaurant_table(
    restaurant_table_id: int,
    db: Session = Depends(get_db)
):
    restaurant_table = db.query(RestaurantTable).filter(
        RestaurantTable.id == restaurant_table_id
    ).first()

    if not restaurant_table:
        raise HTTPException(
            status_code=404,
            detail="Restaurant table not found"
        )

    db.delete(restaurant_table)
    db.commit()

    return {
        "message": "Restaurant table deleted"
    }


# ============================================================
# ORDERS
# ============================================================

@app.post(
    "/orders",
    response_model=OrderResponse,
    summary="Create order",
    description=(
        "Creates a new customer order. "
        "The customer and table must exist, and the selected table must be available."
    )
)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == order.customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    restaurant_table = db.query(RestaurantTable).filter(
        RestaurantTable.id == order.table_id
    ).first()

    if not restaurant_table:
        raise HTTPException(
            status_code=404,
            detail="Restaurant table not found"
        )

    if not restaurant_table.is_available:
        raise HTTPException(
            status_code=400,
            detail="Table is not available"
        )

    new_order = Order(
        **order.model_dump()
    )

    restaurant_table.is_available = False

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


@app.get(
    "/orders",
    response_model=List[OrderResponse],
    summary="Get all orders",
    description="Returns a list of all restaurant orders."
)
def get_orders(
    db: Session = Depends(get_db)
):
    return db.query(Order).all()


@app.get(
    "/orders/{order_id}",
    response_model=OrderResponse,
    summary="Get order by ID",
    description="Returns detailed information about a specific order."
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


@app.put(
    "/orders/{order_id}",
    response_model=OrderResponse,
    summary="Update order",
    description="Updates the customer and restaurant table information of an existing order."
)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    customer = db.query(Customer).filter(
        Customer.id == order_data.customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    restaurant_table = db.query(RestaurantTable).filter(
        RestaurantTable.id == order_data.table_id
    ).first()

    if not restaurant_table:
        raise HTTPException(
            status_code=404,
            detail="Table not found"
        )

    for key, value in order_data.model_dump(
        exclude_unset=True
    ).items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)

    return order


@app.delete(
    "/orders/{order_id}",
    summary="Delete order",
    description=(
        "Deletes an order and makes its associated restaurant table "
        "available again."
    )
)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    restaurant_table = db.query(RestaurantTable).filter(
        RestaurantTable.id == order.table_id
    ).first()

    if restaurant_table:
        restaurant_table.is_available = True

    db.delete(order)
    db.commit()

    return {
        "message": "Order deleted"
    }


# ============================================================
# ORDER ITEMS
# ============================================================

@app.post(
    "/order_items",
    response_model=OrderItemResponse,
    summary="Add item to order",
    description=(
        "Adds a food item to an existing order. "
        "The food must be available and quantity must be greater than zero. "
        "The order total price is updated automatically."
    )
)
def create_order_item(
    order_item: OrderItemCreate,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_item.order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    food = db.query(Food).filter(
        Food.id == order_item.food_id
    ).first()

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Food not found"
        )

    if not food.is_available:
        raise HTTPException(
            status_code=400,
            detail="Food is not available"
        )

    if order_item.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    new_order_item = OrderItem(
        order_id=order_item.order_id,
        food_id=order_item.food_id,
        quantity=order_item.quantity,
        price=food.price
    )

    db.add(new_order_item)

    order.total_price += (
        food.price * order_item.quantity
    )

    db.commit()
    db.refresh(new_order_item)

    return new_order_item


@app.get(
    "/order_items",
    response_model=List[OrderItemResponse],
    summary="Get all order items",
    description="Returns all food items belonging to customer orders."
)
def get_order_items(
    db: Session = Depends(get_db)
):
    return db.query(OrderItem).all()


@app.get(
    "/order_items/{order_item_id}",
    response_model=OrderItemResponse,
    summary="Get order item by ID",
    description="Returns detailed information about a specific order item."
)
def get_order_item(
    order_item_id: int,
    db: Session = Depends(get_db)
):
    order_item = db.query(OrderItem).filter(
        OrderItem.id == order_item_id
    ).first()

    if not order_item:
        raise HTTPException(
            status_code=404,
            detail="Order item not found"
        )

    return order_item


@app.put(
    "/order_items/{order_item_id}",
    response_model=OrderItemResponse,
    summary="Update order item",
    description=(
        "Updates the food or quantity of an order item "
        "and recalculates the order total."
    )
)
def update_order_item(
    order_item_id: int,
    order_item_data: OrderItemUpdate,
    db: Session = Depends(get_db)
):
    order_item = db.query(OrderItem).filter(
        OrderItem.id == order_item_id
    ).first()

    if not order_item:
        raise HTTPException(
            status_code=404,
            detail="Order item not found"
        )

    food = db.query(Food).filter(
        Food.id == order_item_data.food_id
    ).first()

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Food not found"
        )

    if not food.is_available:
        raise HTTPException(
            status_code=400,
            detail="Food is not available"
        )

    if order_item_data.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    old_total = (
        order_item.price *
        order_item.quantity
    )

    order_item.food_id = order_item_data.food_id
    order_item.quantity = order_item_data.quantity
    order_item.price = food.price

    new_total = (
        food.price *
        order_item_data.quantity
    )

    order_item.order.total_price -= old_total
    order_item.order.total_price += new_total

    db.commit()
    db.refresh(order_item)

    return order_item


@app.delete(
    "/order-items/{item_id}",
    summary="Delete order item",
    description=(
        "Removes an item from an order "
        "and subtracts its price from the order total."
    )
)
def delete_order_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    item = db.query(OrderItem).filter(
        OrderItem.id == item_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Order item not found"
        )

    item.order.total_price -= (
        item.price * item.quantity
    )

    db.delete(item)
    db.commit()

    return {
        "message": "Order item deleted"
    }


# ============================================================
# PAYMENTS
# ============================================================

@app.post(
    "/payments",
    response_model=PaymentResponse,
    summary="Create payment",
    description=(
        "Creates a payment for an existing order. "
        "The payment amount must be greater than zero."
    )
)
def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == payment.order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if payment.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than 0"
        )

    new_payment = Payment(
        **payment.model_dump()
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return new_payment


@app.get(
    "/payments",
    response_model=List[PaymentResponse],
    summary="Get all payments",
    description="Returns a list of all payments."
)
def get_payments(
    db: Session = Depends(get_db)
):
    return db.query(Payment).all()


@app.get(
    "/payments/{payment_id}",
    response_model=PaymentResponse,
    summary="Get payment by ID",
    description="Returns detailed information about a specific payment."
)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):
    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment


@app.put(
    "/payments/{payment_id}",
    response_model=PaymentResponse,
    summary="Update payment",
    description=(
        "Updates the order, amount, or payment method "
        "of an existing payment."
    )
)
def update_payment(
    payment_id: int,
    payment_data: PaymentUpdate,
    db: Session = Depends(get_db)
):
    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    order = db.query(Order).filter(
        Order.id == payment_data.order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if payment_data.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than 0"
        )

    payment.order_id = payment_data.order_id
    payment.amount = payment_data.amount
    payment.payment_method = payment_data.payment_method

    db.commit()
    db.refresh(payment)

    return payment


@app.delete(
    "/payments/{payment_id}",
    summary="Delete payment",
    description="Deletes an existing payment."
)
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):
    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    db.delete(payment)
    db.commit()

    return {
        "message": "Payment deleted"
    }


# ============================================================
# RELATIONSHIP / EXTRA ENDPOINTS
# ============================================================

@app.get(
    "/categories/{category_id}/foods",
    summary="Get foods by category",
    description="Returns all food items that belong to a specific category."
)
def get_category_foods(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category.foods


@app.get(
    "/customers/{customer_id}/orders",
    summary="Get customer orders",
    description="Returns all orders created by a specific customer."
)
def get_customers_orders(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer.orders


@app.get(
    "/orders/{order_id}/items",
    summary="Get order items",
    description="Returns all food items included in a specific order."
)
def get_order_items_by_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order.items


@app.get(
    "/foods/available",
    summary="Get available foods",
    description="Returns only food items that are currently available."
)
def get_available_foods(
    db: Session = Depends(get_db)
):
    foods = db.query(Food).filter(
        Food.is_available == True
    ).all()

    return foods


@app.get(
    "/tables/available",
    summary="Get available tables",
    description="Returns only restaurant tables that are currently available."
)
def get_available_tables(
    db: Session = Depends(get_db)
):
    tables = db.query(RestaurantTable).filter(
        RestaurantTable.is_available == True
    ).all()

    return tables


@app.get(
    "/orders/{order_id}/total",
    summary="Calculate order total",
    description=(
        "Calculates the total price of all items in an order "
        "and updates the order total_price field."
    )
)
def get_order_total(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    total = 0

    for item in order.items:
        total += float(item.price) * item.quantity

    order.total_price = total

    db.commit()

    return {
        "order_id": order.id,
        "total_price": total
    }


@app.put(
    "/orders/{order_id}/status",
    summary="Update order status",
    description=(
        "Changes the status of an order. "
        "Allowed statuses are pending, preparing, completed and cancelled."
    )
)
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    allowed_statuses = [
        "pending",
        "preparing",
        "completed",
        "cancelled"
    ]

    if status_data.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    order.status = status_data.status

    db.commit()
    db.refresh(order)

    return order


@app.put(
    "/orders/{order_id}/complete",
    summary="Complete order",
    description=(
        "Marks an order as completed and makes its restaurant table "
        "available again."
    )
)
def complete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.status == "completed":
        raise HTTPException(
            status_code=400,
            detail="Order is already completed"
        )

    order.status = "completed"

    table = db.query(RestaurantTable).filter(
        RestaurantTable.id == order.table_id
    ).first()

    if table:
        table.is_available = True

    db.commit()
    db.refresh(order)

    return {
        "message": "Order completed successfully"
    }


@app.get(
    "/orders/{order_id}/payments",
    summary="Get order payments",
    description="Returns all payments associated with a specific order."
)
def get_order_payments(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order.payments


@app.get(
    "/orders/{order_id}/paid",
    summary="Get total paid amount",
    description=(
        "Calculates and returns the total amount of money "
        "already paid for a specific order."
    )
)
def get_order_paid(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    total_paid = 0

    for payment in order.payments:
        total_paid += float(payment.amount)

    return {
        "order_id": order.id,
        "paid": total_paid
    }