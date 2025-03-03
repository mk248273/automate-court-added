from lib import *


def code_stoper(hour, minute):
    second = 45
    logging.info(f"Started code_stoper for stopping at {hour}:{minute}:{second}.")
    while True:
        now = datetime.now()
        logging.debug(f"Current time: {now}")
        if now.hour == hour and now.minute == minute and now.second == second:
            logging.info("Stopping the code.")
            break

from datetime import datetime, timedelta

def get_next_monday():
    # Convert the input string to a datetime object
    today = datetime.now()
    print(today)
    # Check if today is a Monday
    if today.weekday() != 0:  # 0 is Monday
        raise ValueError("The provided date is not a Monday.")
    
    # Calculate the date 4 weeks (28 days) later
    four_weeks_later = today + timedelta(weeks=4)
    
    return four_weeks_later.strftime('%Y-%m-%d')
