from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Float, Integer, Boolean, DateTime
from flask_login import UserMixin
from typing import List
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    user_email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    pass_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default='customer')  # New field
    confirmed: Mapped[bool] = mapped_column(default=False)
    salts: Mapped[str] = mapped_column(String(320))  # Store all salts as single string
    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    # Relationships
    stalls: Mapped[List['Stall']] = relationship(back_populates="owner")
    orders: Mapped[List['Order']] = relationship(back_populates="user")
    cart_items: Mapped[List['CartItem']] = relationship(back_populates="user")

class Stall(Base):
    __tablename__ = "stalls"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    image_url: Mapped[str] = mapped_column(String(200))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    # Relationships
    owner: Mapped['User'] = relationship(back_populates="stalls")
    foods: Mapped[List['Food']] = relationship(back_populates="stall")
    orders: Mapped[List['OrderItem']] = relationship(back_populates="stall")

class Food(Base):
    __tablename__ = "foods"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    image_url: Mapped[str] = mapped_column(String(200))
    stall_id: Mapped[int] = mapped_column(ForeignKey("stalls.id"))
    
    # Relationships
    stall: Mapped['Stall'] = relationship(back_populates="foods")
    order_items: Mapped[List['OrderItem']] = relationship(back_populates="food")

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    total: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(20), default='pending')
    payment_id: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    # Relationships
    user: Mapped['User'] = relationship(back_populates="orders")
    items: Mapped[List['OrderItem']] = relationship(back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    price_at_order: Mapped[float] = mapped_column(Float)
    
    # Relationships
    order: Mapped['Order'] = relationship(back_populates="items")
    food: Mapped['Food'] = relationship(back_populates="order_items")
    stall: Mapped['Stall'] = relationship(back_populates="orders")

class CartItem(Base):
    __tablename__ = "cart_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    
    # Relationships
    user: Mapped['User'] = relationship(back_populates="cart_items")
    food: Mapped['Food'] = relationship()