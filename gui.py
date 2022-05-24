from cgitb import enable
import PySimpleGUI as sg
from main import *
from yahoo_fin import stock_info


sg.theme('DarkAmber')   


login_section = [  [sg.Text('Login to Trading Simulator')],
            [sg.Text('ID', size=(15,1)), sg.InputText(enable_events=True, key='USERID')],
            [sg.Button('Login', enable_events=True, key='LOGINBUTTON')],
            [sg.Text('_'  * 100, size=(65, 1))]
]

register_section = [
    [sg.Text('Don\'t have an account? Enter your new ID here.')],
    [sg.Text('ID', size=(15,1)), sg.InputText(enable_events=True, key='REGISTERID')],
    [sg.Text('Starting balance', size=(15,1)), sg.InputText(enable_events=True, key='STARTBAL')],
    [sg.Button('Register', enable_events=True, key='REGISTERBUTTON')],
    [sg.Text('_'  * 100, size=(65, 1))]
]

# Main section where the user can buy, sell, view summary
btn_size = (9,1)
buy_button = sg.Button('Buy', size=btn_size, enable_events=True, key='ACTION_BUY')
sell_button = sg.Button('Sell', size=btn_size, enable_events=True, key='ACTION_SELL')
sell_all_button = sg.Button('Sell All', size=btn_size, enable_events=True, key='ACTION_SELLALL')
summary_button = sg.Button('Summary', size=btn_size, enable_events=True, key='ACTION_SUMMARY')
help_button = sg.Button('Help', size=btn_size, enable_events=True, key='ACTION_HELP')
help_message = 'To buy a stock, enter the amount you want to buy and enter the stock ticker in their respective fields, and click the Buy button.\n\nTo sell a stock, enter the NUMBER OF SHARE you want to sell and the stock ticker in their respective fields, and click the Sell button.\n\nTo sell all share(s) of a stock you own, enter the stock ticker in its field, and click the Sell All button.\n\nTo get a summary of your portfolio, click the Summary button.'


action_section = [
    [sg.Text('Enter value', size=(15,1)), sg.InputText(enable_events=True, key='ACTION_VALUE')],
    [sg.Text('Enter stock name', size=(15,1)), sg.InputText(enable_events=True, key='ACTION_NAME')],
    [buy_button, sell_button, sell_all_button, summary_button, help_button]
]

output_section = [sg.Output(size=(60,20), key='OUTPUTBOX')]
main_layout = [login_section, register_section, action_section, output_section]
# Create the Window
window = sg.Window('Trading Simulator', main_layout, margins=(50, 50))
# Event Loop to process "events" and get the "values" of the inputs

current_user_id = None
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED: 
        break
    
    # User login under existing ID
    if event == 'LOGINBUTTON':
        if check_user_existed(values['USERID']):
            window['OUTPUTBOX'].update('Login successful.')
            current_user_id = values['USERID']
        else:
            window['OUTPUTBOX'].update('User does not exist. Please register.')
        

    # User register under a new ID
    if event == 'REGISTERBUTTON':
        # Check if balance is a number
        if not values['STARTBAL'].isdigit():
            window['OUTPUTBOX'].update('Invalid value for AMOUNT. Please try again.')
        else:
            message = create_profile(values['REGISTERID'], int(values['STARTBAL']))
            if message == 'Successful.':
                output_msg = 'Successfully created profile. Your id is \'' + values['REGISTERID'] + '\'.'
                output_msg += '\nYour starting balance is $' + values['STARTBAL'] + '.'
            if message == 'ID existed':
                output_msg = 'ID already existed. Please choose a different ID.'
            window['OUTPUTBOX'].update(output_msg)

    if event == 'ACTION_BUY':
        if current_user_id == None:
            window['OUTPUTBOX'].update('You need to login first.')
        else:
            try:
                stock_ticker = values['ACTION_NAME'].upper()
                amount = float(values['ACTION_VALUE'])
                output_msg = buy_stock(current_user_id, stock_ticker, amount)

                if output_msg == 'Insufficient balance.':
                    window['OUTPUTBOX'].update(output_msg)
                else:
                    window['OUTPUTBOX'].update('Successfully purchased '+str(output_msg)+' '+stock_ticker+' share(s).')
            except:
                window['OUTPUTBOX'].update('Invalid values. Try again.')
    
    if event == 'ACTION_SELL':
        if current_user_id == None:
            window['OUTPUTBOX'].update('You need to login first.')
        else:
            try:
                stock_ticker = values['ACTION_NAME'].upper()
                amount = float(values['ACTION_VALUE'])
                output_msg = sell_stock(current_user_id, stock_ticker, amount)

                if output_msg == 'Insufficient amount.':
                    window['OUTPUTBOX'].update(output_msg)
                elif output_msg == 'You don\'t own any share of this company.':
                    window['OUTPUTBOX'].update(output_msg)
                else:
                    window['OUTPUTBOX'].update('Successfully sold '+str(output_msg)+' '+stock_ticker+' share(s).')
            except:
                window['OUTPUTBOX'].update('Invalid values. Try again.')

    if event == 'ACTION_SELLALL':
        if current_user_id == None:
            window['OUTPUTBOX'].update('You need to login first.')
        else:
            try:
                stock_ticker = values['ACTION_NAME'].upper()
                output_msg = sell_all_stock(current_user_id, stock_ticker)

                if output_msg == 'You don\'t own any share of this company.':
                    window['OUTPUTBOX'].update(output_msg)
                else:
                    window['OUTPUTBOX'].update('Successfully sold all '+stock_ticker+' share(s).')
            except:
                window['OUTPUTBOX'].update('Invalid values. Try again.')

    if event == 'ACTION_SUMMARY':
        if current_user_id == None:
            window['OUTPUTBOX'].update('You need to login first.')
        else:
            summary = get_summary(current_user_id)
            user_balance = float(summary[0])
            holdings = summary[1]
            start_bal = summary[2]
            capital = user_balance

            output = 'PORTFOLIO SUMMARY\n\n'
            output += '{:<20}| {:<10} | {:<10} | {:<10}\n'.format('    Company name', '  Symbol', 'Share owned', 'Current value')
            output += '-'*80 + '\n'
            for symbol in holdings:
                company_name = yf.Ticker(symbol.upper()).info['longName']
                if len(company_name) >= 15:
                    company_name = company_name[:12]
                
                current_price = stock_info.get_live_price(symbol)
                current_value = current_price*holdings[symbol]
                capital += current_value
                line = '{:<20}| {:<10} | {:<10.2f}  | {:<10.2f}\n'.format(company_name, symbol.upper(), holdings[symbol], current_value)
                output += line
            
            output += '-'*80 + '\n\n'
            output += 'WALLET          : ${:.2f}\n'.format(user_balance)
            output += 'CAPITAL         : ${:.2f}\n'.format(capital, 2)
            output += 'TOTAL GAIN   : {}%'.format(round((capital/start_bal - 1)*100))
            window['OUTPUTBOX'].update(output)


    if event == 'ACTION_HELP':
        window['OUTPUTBOX'].update(help_message)

    
    
    
window.close()