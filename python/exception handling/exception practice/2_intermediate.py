import re
import math
import json
import logging

# Intermediate Level

# 11. Write a function to withdraw money and raise an exception if balance < withdrawal.
print("11. Write a function to withdraw money and raise an exception if balance < withdrawal.")
def withdraw(balance, amount):
    if amount > balance:
        raise ValueError(f"Insufficient balance: tried to withdraw {amount}, balance is {balance}")
    return balance - amount
try:
    bal = 1000
    amt = 1500
    new_bal = withdraw(bal, amt)
except ValueError as e:
    print("ERROR:", e)
else:
    print("New balance:", new_bal)
print("###########################################")

# 12. Write a function that validates age and raises an exception if age < 18.
print("12. Write a function that validates age and raises an exception if age < 18.")
def validate_age(age):
    if age < 18:
        raise ValueError("Age must be 18 or more.")
    return True
try:
    validate_age(16)
except ValueError as e:
    print("Age validation failed:", e)
else:
    print("Age is valid.")
print("###########################################")

# 13. Write a program to validate email format and raise a custom exception.
print("13. Write a program to validate email format and raise a custom exception.")
class InvalidEmailError(Exception):
    pass
def validate_email(email):
    # ^ Means start of the String
    # [^@\s]+ -> ^ means Not @ and Not whitespaces; + -> one and more (all except whitespace and @)
    # \. escaped dot
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"  # simple: local@domain.tld
    if not re.match(pattern, email):
        raise InvalidEmailError(f"Invalid email: {email}")
    return True
try:
    validate_email(input("Enter a Valid email:"))
except InvalidEmailError as e:
    print("Email error:", e)
else:
    print("Email is valid.")
print("###########################################")

# 14. Write a custom exception NegativeNumberError and use it in a square root function.
print("14. Write a custom exception NegativeNumberError and use it in a square root function.")
class NegativeNumberError(Exception):
    pass
def safe_sqrt(x):
    if x < 0:
        raise NegativeNumberError("Cannot compute square root of negative number.")
    return math.sqrt(x)
try:
    print(safe_sqrt(-4))
except NegativeNumberError as e:
    print("ERROR:", e)
print("###########################################")

# 15. Write a custom exception for InsufficientFundsError in a banking system.
print("15. Write a custom exception for InsufficientFundsError in a banking system.")
class InsufficientFundsError(Exception):
    pass

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(f"Insufficient funds: tried to withdraw {amount}, balance {balance}")
    return balance - amount

# Example usage
balance = 100.0
amount = 200.0
try:
    balance = withdraw(balance, amount)
except InsufficientFundsError as e:
    print("Transaction failed:", e)
else:
    print("New balance:", balance)
print("###########################################")

# 16. Write a program that handles exceptions while parsing JSON.
print("16. Write a program that handles exceptions while parsing JSON.")
data_str = '{"name": "Alice", "age": 30'  # malformed JSON
try:
    obj = json.loads(data_str)
except json.JSONDecodeError as e:
    print("JSON parsing failed:", e)
except TypeError as e:
    # json.loads(None) would raise TypeError
    print("Type error while parsing JSON:", e)
else:
    print("Parsed object:", obj)
print("###########################################")

# 17. Write a program to retry dividing two numbers 3 times if an error occurs.
print("17. Write a program to retry dividing two numbers 3 times if an error occurs.")
def retry_divide(a_str, b_str, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            a = float(a_str)
            b = float(b_str)
            return a / b
        except ValueError:
            raise ValueError("Inputs must be numbers.")
        except ZeroDivisionError:
            attempt += 1
            if attempt < retries:
                print(f"Attempt {attempt}/{retries}: denominator was zero — Retrying...")
            else:
                print(f"Attempt {attempt}/{retries}: denominator was zero — Tries finished.")
                # re-raise the original ZeroDivisionError
                raise  
a_str = input("Enter numerator: ")
b_str = input("Enter denominator: ")
try:
    print(retry_divide(a_str, b_str, 3))
except Exception as e:
    print("Final error:", e)
print("###########################################")

# 18. Write a program that uses assert to validate positive numbers and handle AssertionError.
print("18. Write a program that uses assert to validate positive numbers and handle AssertionError.")
def process_positive(n):
    # assert raises AssertionError when the condition is false
    assert n > 0, "n must be positive"
    return n * 2
try:
    print(process_positive(-5))
except AssertionError as e:
    print("Assertion failed:", e)
print("###########################################")

# 19. Write a program that logs exceptions to a file using logging module.
print("19. Write a program that logs exceptions to a file using logging module.")
# configure logger to write exceptions to a file with traceback
logging.basicConfig(
    filename="errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
try:
    a = int(input("Enter numerator (int): "))
    b = int(input("Enter denominator (int): "))
    print("Division result:", a / b)
except Exception as e:
    # logs the exception with stack trace
    logging.exception("An error occurred while dividing!")
    print("An error was logged to errors.log")
print("###########################################")

# 20. Write a program that raises multiple custom exceptions (InvalidPasswordError, InvalidUsernameError).
print("20. Write a program that raises multiple custom exceptions (InvalidPasswordError, InvalidUsernameError).")
class InvalidUsernameError(Exception):
    pass
class InvalidPasswordError(Exception):
    pass
def validate_credentials(username, password):
    if not username or len(username) < 3:
        raise InvalidUsernameError("Username must be at least 3 characters long.")
    if len(password) < 8:
        raise InvalidPasswordError("Password must be >=8 chars.")
    return True
try:
    validate_credentials("ab", "weakpass")
except InvalidUsernameError as e:
    print("Username error:", e)
except InvalidPasswordError as e:
    print("Password error:", e)
else:
    print("Credentials are valid.")