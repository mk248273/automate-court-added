from lib import *


def wait_for_element(driver, locator, timeout=10):
    """Wait for an element to be present and return it."""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))

def switch_to_iframe(driver):
    """Switch to the Razorpay iframe."""
    try:
        # Wait for iframe to be present
        iframe = wait_for_element(
            driver,
            (By.CSS_SELECTOR, "iframe[class='razorpay-checkout-frame']")
        )
        driver.switch_to.frame(iframe)
        print("Successfully switched to Razorpay iframe")
    except Exception as e:
        print(f"Error switching to iframe: {str(e)}")

def fill_card_details(driver, card_number, expiry, cvv):
    """Fill in the card details in the payment form."""
    try:
        # Wait for and fill card number
        card_number_field = wait_for_element(
            driver,
            (By.CSS_SELECTOR, "input[name='card[number]']")
        )
        card_number_field.send_keys(card_number)

        # Fill expiry date
        expiry_field = wait_for_element(
            driver,
            (By.CSS_SELECTOR, "input[name='card[expiry]']")
        )
        expiry_field.send_keys(expiry)

        # Fill CVV
        cvv_field = wait_for_element(
            driver,
            (By.CSS_SELECTOR, "input[name='card[cvv]']")
        )
        cvv_field.send_keys(cvv)

        return True
    except TimeoutException as e:
        print(f"Error filling card details: {str(e)}")
        return False





def click_pay_button(driver):
    """Click the Pay Now button inside the Razorpay iframe."""
    try:

        # Wait for the container to be visible first, if needed
        cta_container = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "cta-container"))
        )
        
        # Wait for the "Pay Now" button and ensure it's clickable
        pay_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='redesign-v15-cta' and contains(@class, 'svelte-1milfy7')]"))
        )
        
        # Click the "Pay Now" button
        pay_button.click()
        print("Clicked the Pay Now button.")


    except TimeoutException as e:
        print(f"Error clicking the Pay Now button: {str(e)}")

def process_payment(driver, card_details):
    """Main function to process the payment."""
    try:
        # Initial wait for page load
        
        # Switch to Razorpay iframe
        switch_to_iframe(driver)

        # Wait for the form to load

        # Select card payment method if needed
        # try:
        #     card_method = wait_for_element(
        #         driver,
        #         (By.CSS_SELECTOR, "div[data-testid='card-method-block']")
        #     )
        #     card_method.click()

        # except TimeoutException:
        #     print("Card form might be already visible")
        #     pass

        # Fill in card details
        success = fill_card_details(
            driver,
            card_details['number'],
            card_details['expiry'],
            card_details['cvv']
        )

        if success:
            time.sleep(5)

            # Click pay button
            click_pay_button(driver)
            
            # Wait for potential redirect or confirmation
            
            # Switch back to default content,
            time.sleep(1)
            
            print("Payment process completed")
            return True, f"Successfully Payment process completed"

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False, f"Error in Payment process"
