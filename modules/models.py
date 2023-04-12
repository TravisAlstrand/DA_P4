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
        \nBrand ID - {self.brand_id}
        \nBrand name - {self.brand_name}
        """


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_price = Column(Integer)
    product_quantity = Column(Integer)
    date_updated = Column(Date)
    brand_id = Column(Integer, ForeignKey("brands.brand_id"))
    brand = relationship("Brand", back_populates="products")

    def __repr__(self):
        return f"""
        \nProduct ID - {self.product_id}
        \nBrand ID - {self.brand_id}
        \nName - {self.product_name}
        \nQuantity - {self.product_quantity}
        \nPrice - {self.product_price}
        \nDate Updated - {self.date_updated}
        """
