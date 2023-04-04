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
        
        for existing_order in session.query(Order).all():
            if order_obj.sell_amount * existing_order.sell_amount >= order_obj.buy_amount * existing_order.buy_amount and existing_order.buy_currency == order.sell_currency and existing_order.sell_currency == order.buy_currency and existing_order.filled == None:
                order_obj.filled = func.now()
                existing_order.filled = func.now()
                order_obj.counterparty_id = existing_order.id
                existing_order.counterparty_id = order_obj.id
                if order_obj['buy_amount']>existing_order['sell_amount']:
                    order_r = {}
                    order_r['filled'] = None
                    order_r['creator_id'] = order_obj['id']
                    order_r['sender_pk'] = order_obj['sender_pk']
                    order_r['receiver_pk'] = order_obj['receiver_pk']
                    order_r['buy_currency'] = order_obj['buy_currency']
                    order_r['sell_currency'] = order_obj['sell_currency']
                    order_r['buy_amount'] = order_obj['buy_amount']-existing_order['sell_amount']
                    order_r['sell_amount'] = order_obj['sell_amount']-existing_order['buy_amount']
                    session.add(order_r)
                    session.add(order_obj)
                elif existing_order['buy_amount']>order_obj['sell_amount']:
                    order_r = {}
                    order_r['filled'] = None
                    order_r['creator_id'] = existing_order['id']
                    order_r['sender_pk'] = existing_order['sender_pk']
                    order_r['receiver_pk'] = existing_order['receiver_pk']
                    order_r['buy_currency'] = existing_order['buy_currency']
                    order_r['sell_currency'] = existing_order['sell_currency']
                    order_r['buy_amount'] = existing_order['buy_amount']-order_obj['sell_amount']
                    order_r['sell_amount'] = existing_order['sell_amount']-order_obj['buy_amount']
                    session.add(order_r)
                    session.add(order_obj)
                break
        session.commit()
    else:    
        print('!!! Following order does not contain required fields:')
        print( order)
        pass

