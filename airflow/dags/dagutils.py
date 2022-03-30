from datetime import datetime, timedelta, time
from pytz import timezone
import requests, json

# Check if today is a weekday (Market might be open)
def checkweekday(next_execution_date, typ):
    print('next_execution_date is: {}'.format(next_execution_date))
    date_check = next_execution_date.weekday()
    print('date_check is: {}'.format(date_check))
    isweekday = False
    #Su=0, M=1, Tu=2, W=3, Th=4, F=5, Sa=6
    if typ == 'M-SS' and (date_check in range(0,7)):
        isweekday = True
    elif typ == 'T-SS' and (date_check in range(1,7)):
        isweekday = True
    elif typ == 'T-S' and (date_check in range(1,6)):
        isweekday = True
    elif typ == 'M-F' and (date_check in range(0,5)):
        isweekday = True
    elif (typ == 'M-F' and date_check == 5 and int(next_execution_date.strftime('%H')) < 1):
        isweekday = True        
    else:
        isweekday = False
    print('isweekday?: {}'.format(isweekday))
    return isweekday

# Check if it is within normal market hours
def checkmarkethrs():   
    tz = timezone('US/Eastern')
    if(time(9,30) < datetime.now(tz).time() < time(16,0)):
        return True
    else:
        print("Market is not open at this time!")
        return False  
       
def sendemails(email, subject, html_content):
    print("Emails service needs to be setup")