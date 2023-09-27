from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  # Import thêm By
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_failed():
    # Thư mục chứa test
    test_folder = r'C:\Users\httoa\OneDrive\Desktop\ecommerce\ec\test\selenium_tests'

    # Đường dẫn tới thư mục evidences
    evidence_folder = os.path.join(test_folder, "evidences")

    driver = webdriver.Chrome()  # Không cần chỉ định đường dẫn đầy đủ
    driver.get('http://127.0.0.1:8000/login')  # Thay đổi URL đến trang đăng nhập của ứng dụng của bạn

    # Tìm phần tử username_input bằng id
    username_input = driver.find_element(By.ID, 'loginName')  # Sử dụng By.ID
    password_input = driver.find_element(By.ID, 'password')  # Sử dụng By.ID

    username_input.send_keys('incorrect_username')
    password_input.send_keys('incorrect_password')
    screenshot_path1 = os.path.join(evidence_folder, "login_input1.png")
    driver.save_screenshot(screenshot_path1)
    login_button = driver.find_element(By.ID, 'login-button')  # Sử dụng By.ID
    login_button.click()


    wait = WebDriverWait(driver, 10)
    error_messages = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'li')))
    # Kiểm tra xem thông báo lỗi đã hiển thị
    expected_error_messages = 'Username, email, or password is incorrect'
    if expected_error_messages in error_messages.text:
        screenshot_path2 = os.path.join(evidence_folder, "login_failed.png")
        driver.save_screenshot(screenshot_path2)  # Chụp ảnh nếu tìm thấy lỗi
    else:
        raise AssertionError("Không tìm thấy thông báo lỗi mong đợi")

    # Thêm đoạn mã kiểm tra đăng nhập thành công
    test_login_success(driver)  # Gọi hàm kiểm tra đăng nhập thành công

    driver.quit()



def test_login_success(driver):
    # Thư mục chứa test
    test_folder = r'C:\Users\httoa\OneDrive\Desktop\ecommerce\ec\test\selenium_tests'

    # Đường dẫn tới thư mục evidences
    evidence_folder = os.path.join(test_folder, "evidences")

    # Tìm phần tử username_input bằng id
    username_input = driver.find_element(By.ID, 'loginName')  # Sử dụng By.ID
    password_input = driver.find_element(By.ID, 'password')  # Sử dụng By.ID

    username_input.clear()  # Xóa trường nhập liệu
    password_input.clear()  # Xóa trường nhập liệu

    username_input.send_keys('toan')
    password_input.send_keys('angellove12')
    screenshot_path1 = os.path.join(evidence_folder, "login_input2.png")
    driver.save_screenshot(screenshot_path1)
    
    login_button = driver.find_element(By.ID, 'login-button')  # Sử dụng By.ID
    login_button.click()

    # Kiểm tra xem đăng nhập có thành công bằng cách xác định một phần tử sau đăng nhập
    assert 'http://127.0.0.1:8000/' in driver.current_url
    screenshot_path2 = os.path.join(evidence_folder, "login_success.png")
    driver.save_screenshot(screenshot_path2)

test_login_failed()

