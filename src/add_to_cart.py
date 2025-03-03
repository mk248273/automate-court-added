from lib import *

def click_specific_court_buttons(driver, court_numbers):
    """
    Click 'Add to Cart' buttons for specific court numbers.

    Args:
        driver: Selenium WebDriver instance
        court_numbers: List of court numbers to select (e.g., [7, 21])

    Returns:
        tuple: (success_bool, message_string)
    """
    try:
        # Wait for the container with courts to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "flex.flex-col.gap-4.divide-y"))
        )

        # Find all court containers
        court_containers = driver.find_elements(By.CLASS_NAME, "flex.flex-col.gap-4.divide-y")

        clicked_courts = []
        for container in court_containers:
            try:
                # Get court number from the container
                court_name = container.find_element(By.CLASS_NAME, "font-bold").text
                court_num = int(court_name.split()[1])  # Extract number from "Court X"

                # Check if this is one of our target courts
                if court_num in court_numbers:
                    # Get court details before clicking
                    court_type = container.find_element(By.CLASS_NAME, "text-blue-grey-400").text
                    price = container.find_elements(By.CLASS_NAME, "text-blue-grey-400")[1].text

                    # Find and click the Add to Cart button
                    add_button = container.find_element(By.TAG_NAME, "button")
                    add_button.click()

                    clicked_courts.append(court_num)
                    logger.info(f"Added Court {court_num} ({court_type}) - {price} to cart")

                    # Brief wait to allow the click to register
                    time.sleep(5)
            except Exception as inner_e:
                print(f"Error processing court container: {inner_e}")

        # Check if any courts were added
        if clicked_courts:
            # Try to find and click the checkout button
            try:
                checkout_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Checkout')]"))
                )
                checkout_button.click()
                logger.info("Clicked on Checkout button")
            except TimeoutException:
                print("Checkout button not found or not clickable")

            return True, f"Successfully added courts {clicked_courts} to cart"
        else:
            return False, "No matching courts were found to add to the cart"

    except TimeoutException as e:
        return False, f"Timeout waiting for court elements: {str(e)}"
    except Exception as e:
        return False, f"Operation failed: {str(e)}"



def click_card_payment(driver):
    try:
        # Wait for the payment method element to be clickable
        card_payment = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-attr='mastercard-payment-method']"))
        )

        # Click the element
        card_payment.click()
        print("Successfully clicked on Visa/Mastercard payment option")

        # Brief wait to allow for any animations or state changes
        time.sleep(2)

        return True, "Successfully selected card payment method"

    except TimeoutException:
        return False, "Timeout waiting for card payment element to be clickable"
    except Exception as e:
        return False, f"Failed to click card payment: {str(e)}"
    

    
def click_proceed_to_payment(driver):
    try:
        # Wait for the proceed to payment button to be clickable
        proceed_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, 
                "button[data-attr='initiate-external-payment']"
            ))
        )
        
        # Click the proceed button
        proceed_button.click()
        print("Successfully clicked Proceed to Payment button")
        
        # Wait briefly to allow for redirect or loading
        
        return True, "Successfully initiated payment process"
        
    except TimeoutException:
        return False, "Timeout waiting for proceed to payment button"
    except Exception as e:
        return False, f"Failed to proceed to payment: {str(e)}"
