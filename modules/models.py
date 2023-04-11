from sqlalchemy import (create_engine, Column, Integer,
                        String, Date, ForeignKey)
from sqlalchemy.orm import sessionmaker, relationship, declarative_base


engine = create_engine("sqlite:///inventory.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Brand(Base):
    __tablename__ = "brands"

    brand_id = Column(Integer, primary_key=True)
    brand_name = Column(String)
    products = relationship("Product", back_populates="brand",
                            cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"""
        \nBrand ID - {self.brand_id}\r
        Brand name - {self.brand_name}
        """


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    date_updated = Column(Date)
    brand_id = Column(Integer, ForeignKey("brands.brand_id"))
    brand = relationship("Brand", back_populates="products")

    def __repr__(self):
        return f"""
        \nProduct ID - {self.product_id}\r
        Brand ID - {self.brand_id}\r
        Name - {self.product_name}\r
        Quantity - {self.product_quantity}\r
        Price - {self.product_price}\r
        Date Updated - {self.date_updated}
        """
