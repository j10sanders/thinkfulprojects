from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

    
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    items_sold = Column(Integer, ForeignKey('item.id'), nullable=False)
    place_bid = relationship("Bid", backref="user_bid")

class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    seller = relationship("User", backref="seller")
    bid = Column(Integer, ForeignKey('bid.id'), nullable=False)
    item_bid = relationship("Bid", backref="item_price")

class Bid(Base):
    __tablename__ = "bid"
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    
    bid_on_item = relationship("Item", backref="bid_price")
    bidder = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __repr__ (self):
        #return "Bid(price=" + str(self.price)+ ")"
        return "{} Bid(price={})".format(self.bidder.username, self.price)
    
#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
    
def main():    
    
    beyonce = User(username="bknowles", password="uhohuhohuhohohnana")
    jonathan = User(username="jsanders", password="password")
    tester = User(username="test", password="test123")
    
    baseball = Item(name="curveball", description ="cool", seller=jonathan)
    
    session.add_all([baseball, beyonce, jonathan, tester])
    session.commit()

    #x = sorted(bids_total(Bid.price())
    
    #highest_bid = session.query(bids_total).order_by(Bid.price).all()
    #print(session.query(Bid).all())
    
    
if __name__ == "__main__":
    main()