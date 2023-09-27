def validate_email(value):
    if value == '':
        return "Vui lòng nhập email"
    if not value.endswith('@gmail.com'):
        return "Email không hợp lệ"

def validate_phone_number(value):
    if value == '':
        return 'Vui lòng nhập số điện thoại'
    if not value.isdigit() or len(value) < 10:
        return "Số điện thoại không hợp lệ"

def validate_shipping_address(value):
    if value == '':
        return "Vui lòng nhập địa chỉ giao hàng"
    if len(value) < 5:
        return "Địa chỉ giao hàng không hợp lệ"

def validate_payment_method(value):
    if value is None:
        return "Vui lòng chọn phương thức thanh toán"

def validates(email, phone_number, shipping_address, payment_method):
    errors = {}

    # Kiểm tra email
    email_error = validate_email(email)
    if email_error:
        errors['email'] = email_error

    # Kiểm tra số điện thoại
    phone_error = validate_phone_number(phone_number)
    if phone_error:
        errors['phone_number'] = phone_error

    # Kiểm tra địa chỉ giao hàng
    address_error = validate_shipping_address(shipping_address)
    if address_error:
        errors['shipping_address'] = address_error

    payment_method_error = validate_payment_method(payment_method)
    if payment_method_error:
        errors[''] = payment_method_error

    return errors