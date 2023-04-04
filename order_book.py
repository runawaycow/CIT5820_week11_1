from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, Order
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def process_order(order):
    #Your code here
    if all(key in order for key in ['sender_pk','buy_amount','sell_amount', 'receiver_pk', 'buy_currency', 'sell_currency']):
        order_obj = Order( filled = None, sender_pk=order['sender_pk'],receiver_pk=order['receiver_pk'], buy_currency=order['buy_currency'], sell_currency=order['sell_currency'], buy_amount=order['buy_amount'], sell_amount=order['sell_amount'] )
        for existing_order in session.query(existing_order).all():
            if order_obj.sell_amount * existing_order.sell_amount >= order_obj.buy_amount * existing_order.buy_amount:
                if order_obj.sell_amount>order_obj.buy_amount:
                    

            break



        session.add(order_obj)
        session.commit()
    else:    
        print('!!! Following order does not contain required fields:')
        print( order)
        pass

