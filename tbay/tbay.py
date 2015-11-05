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


'''user_item_table = Table('user_item_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('item_id', Integer, ForeignKey('items.id'))
)

bid_item_table = Table('bid_item_association', Base.metadata,
    Column('bid_id', Integer, ForeignKey('bid.id')),
    Column('item_id', Integer, ForeignKey('items.id'))
)

bid_user_table = Table('bid_user_association', Base.metadata,
    Column('bid_id', Integer, ForeignKey('bid.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)'''


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    seller_id = Column(Integer, ForeignKey('user.id'), nullable = False)
    auction_item = relationship("Bid", backref="auction_item")
    
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    sell_items = relationship("Item", backref="owner")
    placebid = relationship("Bid", backref="buyer")
    
class Bid(Base):
    __tablename__ = "bid"
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    
    bid_on_item = Column(Integer, ForeignKey('items.id'))
    bid_placed = Column(Integer, ForeignKey('user.id'), nullable = False)
    
    
    
#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
    
def main():    
    baseball = Item(name="Baseball")
    
    beyonce = User(username="bknowles", password="uhohuhohuhohohnana")
    jonathan = User(username="jsanders", password="password", sell_items=[baseball])
    tester = User(username="test", password="test123")
    
    bid1 = Bid(price=1.00, bid_placed="tester", bid_on_item="baseball")
    bid2 = Bid(price=2.00, bid_placed="beyonce", bid_on_item="baseball")
    bid3 = Bid(price=3.00, bid_placed="tester", bid_on_item="baseball")
    bid4 = Bid(price=4.00, bid_placed="beyonce", bid_on_item="baseball")
    
    
    bids_total = [bid1, bid2, bid3, bid4]
    #x = sorted(bids_total(Bid.price())
    #print(x)
    
    session.add_all([baseball, beyonce, jonathan, tester, bids_total])
    session.commit()
    
    
    x = session.query(bids_total).order_by(Bid.price).all()
    print(x)
    
if __name__ == "__main__":
    main()