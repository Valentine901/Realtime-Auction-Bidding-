import enum
from datetime import datetime, timezone
from typing import List
from app.db.base import Base
from sqlalchemy import String, Integer, ForeignKey, Boolean, Enum, DateTime, Float
from sqlalchemy.orm import relationship, mapped_column, Mapped

class AuctionStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    fullname: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String)

    products: Mapped[List["Product"]] = relationship(back_populates="seller")
    bids: Mapped[List["Bid"]] = relationship(back_populates="bidder")
    auction: Mapped[List["Auction"]] = relationship( back_populates="winner")
    rooms: Mapped[List["Room"]] = relationship(back_populates="creator") 


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    
    room: Mapped["Room"] = relationship(back_populates="notifications")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    image: Mapped[str] = mapped_column(String)
    desc: Mapped[str] = mapped_column(String) 
    is_sold: Mapped[bool] = mapped_column(Boolean, default=False)

    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    seller: Mapped["User"] = relationship(back_populates="products")
    auction: Mapped["Auction"] = relationship(back_populates="product", uselist=False)


class Auction(Base):
    __tablename__ = "auctions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    min_price: Mapped[float] = mapped_column(Float, default=0.0)
    start_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc)) 
    end_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc)) 
    status: Mapped[AuctionStatus] = mapped_column(Enum(AuctionStatus), default=AuctionStatus.OPEN)

    winner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    winner: Mapped["User"] = relationship(back_populates="auction")
    product: Mapped["Product"] = relationship(back_populates="auction")
    bids: Mapped[List["Bid"]] = relationship(back_populates="auction")
    room: Mapped["Room"] = relationship(back_populates="auctions")

    

class Bid(Base):
    __tablename__ = "bids"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    amount: Mapped[float] = mapped_column()
    placed_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


    auction: Mapped["Auction"] = relationship(back_populates="bids")
    bidder: Mapped["User"] = relationship(back_populates="bids")

    auction_id: Mapped[int] = mapped_column(ForeignKey("auctions.id"))
    bidder_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc)) 

    creator: Mapped["User"] = relationship(back_populates="rooms")
    notifications: Mapped[List["Notification"]] = relationship(back_populates="room")
    auctions: Mapped[List["Auction"]] = relationship(back_populates="room")

    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
