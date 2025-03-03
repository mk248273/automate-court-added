from lib import *


def login(driver, email, password):
    try:
        # Wait for and click the Login button to open login form
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Log In']"))
        )
        login_button.click()

        # Wait for and find email input field
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='email']"))
        )
        email_field.clear()
        email_field.send_keys(email)

        # Find and fill password field
        password_field = driver.find_element(By.XPATH, "//input[@id='password']")
        password_field.clear()
        password_field.send_keys(password)

        # Find and click the login submit button
        submit_button = driver.find_element(By.XPATH, "//button[normalize-space()='Log In']")
        submit_button.click()

        time.sleep(5)     
        
        return True, "Login successful"

    except TimeoutException as e:
        return False, f"Timeout waiting for element: {str(e)}"
    except Exception as e:
        return False, f"Login failed: {str(e)}"