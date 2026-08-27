from pydantic import BaseModel
from datetime import datetime


class CategoryCreate(BaseModel):
    name: str
    description: str


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class FoodCreate(BaseModel):
    name: str
    price: float
    description: str
    is_available: bool = True
    category_id: int


class FoodUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None
    is_available: bool | None = None
    category_id: int | None = None


class FoodResponse(BaseModel):
    id: int
    name: str
    price: float
    description: str
    is_available: bool
    category_id: int

    class Config:
        from_attributes = True


class CustomerCreate(BaseModel):
    fullname: str
    phone: str
    email: str


class CustomerUpdate(BaseModel):
    fullname: str | None = None
    phone: str | None = None
    email: str | None = None


class CustomerResponse(BaseModel):
    id: int
    fullname: str
    phone: str
    email: str

    class Config:
        from_attributes = True


class RestaurantTableCreate(BaseModel):
    table_number: int
    capacity: int
    is_available: bool = True


class RestaurantTableUpdate(BaseModel):
    table_number: int | None = None
    capacity: int | None = None
    is_available: bool | None = None


class RestaurantTableResponse(BaseModel):
    id: int
    table_number: int
    capacity: int
    is_available: bool

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    customer_id: int
    table_id: int
    status: str = "pending"


class OrderUpdate(BaseModel):
    customer_id: int | None = None
    table_id: int | None = None
    status: str | None = None


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    table_id: int
    order_date: datetime
    status: str
    total_price: float

    class Config:
        from_attributes = True


class OrderItemCreate(BaseModel):
    order_id: int
    food_id: int
    quantity: int


class OrderItemUpdate(BaseModel):
    food_id: int | None = None
    quantity: int | None = None


class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    food_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    payment_method: str


class PaymentUpdate(BaseModel):
    order_id: int | None = None
    amount: float | None = None
    payment_method: str | None = None


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    payment_date: datetime
    payment_method: str

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str


class RegisterScheme(BaseModel):
    username: str
    email: str
    password: str

class LoginScheme(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True

class ChangePasswordScheme(BaseModel):
    old_password: str
    new_password: str

class UserUpdateScheme(BaseModel):
    username: str | None = None
    email: str | None = None