from lib import *



def click_ok_button_in_dialog(driver):
    try:
        # Wait for the dialog to be visible
        dialog = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'radix-125'))
        )
        
        # If the dialog is found, proceed to scroll
        print("Dialog is visible.")

        # Scroll down within the dialog until the OK button is visible
        while True:
            try:
                # Attempt to find the OK button
                ok_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Ok, got it!')]")
                
                # If the OK button is visible, break the loop
                if ok_button.is_displayed():
                    break
            except:
                # Scroll down if the button is not found
                ActionChains(driver).move_to_element(dialog).send_keys(Keys.PAGE_DOWN).perform()

        # Click the OK button
        ok_button.click()

        # Optional: wait for a bit to observe the result before closing the browser
        # time.sleep(10)

    except Exception as e:
        # Print message if the dialog is not visible
        print("Dialog is not visible.")
        print(f"Error: {e}")