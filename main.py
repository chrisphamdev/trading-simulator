from Stock import *
import json

# This function get all user and their id and return them as a dict(id:name)
def get_holdings_db():
    with open('db/holdingsdb.json', 'r') as f:
        data = json.load(f)
        return data

# This function update the users db
def update_holdings_db(users_dict):
    with open('db/holdingsdb.json', 'w') as f:
        json.dump(users_dict, f)

# This functionc create an entry for the user in the database
def create_profile(user_id, bal):
    holdings_db = get_holdings_db()
    all_user_ids = holdings_db.keys()
    start_bal = float(bal)

    if str(user_id) in all_user_ids:
        return 'ID existed.'
    
    holdings_db[user_id] = [bal, {}, start_bal]
    update_holdings_db(holdings_db)
    return 'Successful.'



def check_user_existed(user_id):
    holdings_db = get_holdings_db()
    all_user_ids = holdings_db.keys()

    if str(user_id) in all_user_ids:
        return True
    else:
        return False


def buy_stock(buyer_id, symbol, amount):
    buyer_id = str(buyer_id)
    all_holdings = get_holdings_db()
    if buyer_id not in all_holdings.keys():
        return 'User does not exist.'

    user = all_holdings[buyer_id]
    user_balance = user[0]
    user_holdings = user[1]
    start_balance = user[2]


    if user_balance < amount:
        return 'Insufficient balance.'
    else:
        stock = Stock(symbol)
        current_price = stock.current_price()
        amount_in_shares = amount/current_price

        if stock.symbol in user_holdings.keys():
            user_balance -= current_price*amount_in_shares # did not use amount because of rounding
            user_holdings[stock.symbol] += amount_in_shares
        else:
            user_balance -= current_price*amount_in_shares # did not use amount because of rounding
            user_holdings[stock.symbol] = amount_in_shares
        
    updated_user = [round(user_balance, 2), user_holdings, start_balance]
    all_holdings[buyer_id] = updated_user
    update_holdings_db(all_holdings)
    return round(amount_in_shares, 2)
    
    
def sell_stock(buyer_id, symbol, amount):
    buyer_id = str(buyer_id)
    amount = round(amount, 2)
    all_holdings = get_holdings_db()
    if buyer_id not in all_holdings.keys():
        return 'User does not exist.'

    user = all_holdings[buyer_id]
    user_balance = user[0]
    user_holdings = user[1]
    start_balance = user[2]

    if symbol.upper() in user_holdings.keys():
        stock = Stock(symbol)
        if amount <= user_holdings[stock.symbol]:
            user_holdings[stock.symbol] -= amount
            user_balance += amount*stock.current_price()
        else:
            return  'Insufficient amount.'
    else:
        return 'You don\'t own any share of this company.'
    
    if user_holdings[stock.symbol] == 0:
        user_holdings.pop(stock.symbol)
    
    updated_user = [user_balance, user_holdings, start_balance]
    all_holdings[buyer_id] = updated_user
    update_holdings_db(all_holdings)
    return amount

def sell_all_stock(buyer_id, symbol):
    buyer_id = str(buyer_id)
    all_holdings = get_holdings_db()
    if buyer_id not in all_holdings.keys():
        return 'User does not exist.'

    user = all_holdings[buyer_id]
    user_balance = user[0]
    user_holdings = user[1]
    start_balance = user[2]

    if symbol.upper() in user_holdings.keys():
        stock = Stock(symbol)
        user_balance += user_holdings[stock.symbol]*stock.current_price()
        user_holdings.pop(stock.symbol)
    else:
        return 'You don\'t own any share of this company.'
          
    updated_user = [user_balance, user_holdings, start_balance]
    all_holdings[buyer_id] = updated_user
    update_holdings_db(all_holdings)
    return 'Successful.'

def calculate_capital(user_id):
    user_id = str(user_id)
    all_holdings = get_holdings_db()
    if user_id not in all_holdings.keys():
        return 'User does not exist.'
    
    user = all_holdings[user_id]
    user_balance = user[0]
    user_holdings = user[1]
    capital = user_balance

    for symbol in user_holdings.keys():
        stock = Stock(symbol)
        value = stock.current_price() * user_holdings[symbol]
        capital += value
        print('This is how fast this code is compiling')

    return capital

def get_summary(user_id):
    user_id = str(user_id)
    all_holdings = get_holdings_db()
    if user_id not in all_holdings.keys():
        return 'User does not exist.'

    user = all_holdings[user_id]
    user_balance = user[0]
    user_holdings = user[1]
    start_balance = user[2]
    return [user_balance, user_holdings, start_balance]