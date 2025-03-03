from lib import *
from src.time_func import *
from src.setup_driver import *
from src.login import *
from src.add_to_cart import *
from src.dialog import *
from src.payment import *


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/home/u357245303/Automate_Court_Added/booking_log.log", mode="a"),  # Log to file in append mode
        # Run on own pc
        # logging.FileHandler("booking_log.log", mode="a"),  # Log to file in append mode
        logging.StreamHandler()  # Log to console
    ]
)



# Load configuration
config = configparser.ConfigParser()
config.read("/home/u357245303/Automate_Court_Added/config.ini")

# Run on own pc
#config.read("config.ini")

def main():
    driver = None
    try:
        driver = setup_driver()
        
        # Navigate to the website
        driver.get("https://www.courtsite.my/")
        
        # Retrieve login credentials from config
        email = config.get("login", "email")
        password = config.get("login", "password")
        
        # Attempt login
        success, message = login(driver, email, password)
        logger.info(message)
        time.sleep(5)

        
        if success:
            # Retrieve booking details from config

            Date = get_next_monday()

            # Run on own pc
            # Date = "2025-03-30"
            logger.info(Date)

            Time = config.get("date", "Time")
            Meridiem = config.get("date", "Meridiem")
            Duration = config.get("date", "Duration")
            
            # Generate booking URL
            code_stoper(16,0)

            from_search = f"https://www.courtsite.my/centre/222%20Sports%20Centre%20PJ/ckwgez18r013u067o7j1hp29q/select?date={Date}&time={Time}&meridiem={Meridiem}&duration={Duration}"

            driver.get(from_search)
            logger.info(f"from_search: {from_search}")

            # Retrieve court numbers from config
            court_numbers = [int(x.strip()) for x in config.get("booking", "court_numbers").split(",")]
            logger.info(f"Courts to be booked: {court_numbers}")
            
            # Execute the clicking operation
            time.sleep(8)

            success, message = click_specific_court_buttons(driver, court_numbers)
            logger.info(message)
            time.sleep(15)

            success, message = click_card_payment(driver)
            time.sleep(5)

            if success:
                logger.info("Payment method selected successfully")
            else:
                logger.error(f"Failed to select payment method: {message}")
            
            success, message = click_proceed_to_payment(driver)
            if success:
                logger.info("Proceeding to payment gateway")
            else:
                logger.error(f"Failed to proceed payment : {message}")
            
            time.sleep(10)
            
            # Retrieve payment details from config
            card_details = {
                "number": config.get("payment_method", "card_number"),
                "expiry": config.get("payment_method", "card_expiry"),
                "cvv": config.get("payment_method", "card_cvv"),
            }
            
            success, message = process_payment(driver, card_details)
            time.sleep(600)

            if success:
                logger.info("Complete payment Method")
            else:
                logger.error(f"Failed payment Method : {message}")
            
            
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
