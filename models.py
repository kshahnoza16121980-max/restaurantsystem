from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime,
    DECIMAL
)
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String(255))

    foods = relationship(
        "Food",
        back_populates="category",
        cascade="all, delete"
    )


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    price = Column(DECIMAL(10, 2))
    description = Column(String(255))
    is_available = Column(Boolean, default=True)

    category_id = Column(
        Integer,
        ForeignKey("categories.id")
    )

    category = relationship(
        "Category",
        back_populates="foods"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="food",
        cascade="all, delete"
    )


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100), unique=True)

    orders = relationship(
        "Order",
        back_populates="customer",
        cascade="all, delete"
    )


class RestaurantTable(Base):
    __tablename__ = "restaurant_tables"

    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(Integer)
    capacity = Column(Integer)
    is_available = Column(Boolean, default=True)

    orders = relationship(
        "Order",
        back_populates="table",
        cascade="all, delete"
    )


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id")
    )

    table_id = Column(
        Integer,
        ForeignKey("restaurant_tables.id")
    )

    order_date = Column(
        DateTime,
        default=datetime.utcnow
    )

    status = Column(
        String(30),
        default="pending"
    )

    total_price = Column(
        DECIMAL(10, 2),
        default=0
    )

    customer = relationship(
        "Customer",
        back_populates="orders"
    )

    table = relationship(
        "RestaurantTable",
        back_populates="orders"
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete"
    )

    payments = relationship(
        "Payment",
        back_populates="order",
        cascade="all, delete"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id")
    )

    food_id = Column(
        Integer,
        ForeignKey("foods.id")
    )

    quantity = Column(Integer)

    price = Column(
        DECIMAL(10, 2)
    )

    order = relationship(
        "Order",
        back_populates="items"
    )

    food = relationship(
        "Food",
        back_populates="order_items"
    )


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id")
    )

    amount = Column(
        DECIMAL(10, 2)
    )

    payment_date = Column(
        DateTime,
        default=datetime.utcnow
    )

    payment_method = Column(
        String(30)
    )

    order = relationship(
        "Order",
        back_populates="payments"
    )
