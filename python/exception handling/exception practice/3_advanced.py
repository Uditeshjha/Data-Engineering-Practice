import csv
import requests
import tracemalloc

# Advanced Level

# 21. Write a program that demonstrates exception propagation across multiple functions.
print("21. Write a program that demonstrates exception propagation across multiple functions.")
def level_three():
    raise ValueError("Bad value caught at level_three() method")
def level_two():
    level_three()
def level_one():
    level_two()
try:
    level_one()
except ValueError as e:
    print("Top-level caught:", type(e).__name__, "-", e)
print("###########################################")

# 22. Write a program using exception chaining (raise ... from ...).
print("22. Write a program using exception chaining (raise ... from ...).")
class InvalidAmountError(Exception):
    pass

def parse_amount(s):
    try:
        return float(s)
    except ValueError as e:
        # chain the low-level ValueError into a domain-specific exception
        raise InvalidAmountError(f"Cannot parse amount from '{s}'") from e

try:
    amt = parse_amount("12.3.4") 
except InvalidAmountError as e:
    print("Chained exception:", e)
    # show original exception via __cause__
    print("Original cause:", type(e.__cause__).__name__, "-", e.__cause__)
print("###########################################")

# 23. Write a program that simulates database connection and raises custom exceptions.
print("23. Write a program that simulates database connection and raises custom exceptions.")
class DatabaseConnectionError(Exception):
    pass

class QueryExecutionError(Exception):
    pass

try:
    connected = False  # simulate DB is not connected
    if not connected:
        raise DatabaseConnectionError("ERROR! Unable to connect to DB")
    query = "DROP TABLE users"
    if "DROP" in query.upper():
        raise QueryExecutionError("ERROR! Dangerous query detected")
    print("Query executed successfully!")

except (DatabaseConnectionError, QueryExecutionError) as e:
    print("DB error:", e)
print("###########################################")

# 24. Write a program that reads from a file using with statement and handles errors.
print("24. Write a program that reads from a file using with statement and handles errors.")
filename = "data.txt"
try:
    with open(filename, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            print(i, line.strip())
except FileNotFoundError:
    print("File not found:", filename)
except UnicodeDecodeError:
    print("Could not decode file (wrong encoding).")
except Exception as e:
    print("Unexpected error while reading file:", type(e).__name__, e)
print("###########################################")

# 25. Write a program that skips bad data rows in a CSV file using exception handling.
print("25. Write a program that skips bad data rows in a CSV file using exception handling.")
good_rows = []
bad_count = 0
try:
    with open("people.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                if not row["name"].strip():
                    raise ValueError("Name is empty")
                row["age"] = int(row["age"])
                row["salary"] = float(row["salary"])
                good_rows.append(row)
            except Exception:
                bad_count += 1
                print("Skipping bad row:", row)
except FileNotFoundError:
    print("ERROR! Csv file not found")

print("Good rows:", good_rows)
print("Skipped rows:", bad_count)
print("###########################################")

# 26. Write a program that handles timeout error when connecting to a server (use requests).
print("26. Write a program that handles timeout error when connecting to a server (use requests).")

# HTTPBin is an open source application for testing and is commonly used for web debugging. 
url = "https://httpbin.org/delay/5"  # endpoint that delays response for demo
try:
    # `timeout` is (connect_timeout, read_timeout) or a single float
    resp = requests.get(url, timeout=0.5)  # Half second
    resp.raise_for_status()
    print("Response length:", len(resp.text))
except requests.Timeout:
    print("Request timed out (server too slow).")
except requests.HTTPError as e:
    print("HTTP error:", e)
except requests.RequestException as e:
    print("Other requests error:", e)
print("###########################################")

# 27. Write a program that handles exceptions in a recursive factorial function.
print("27. Write a program that handles exceptions in a recursive factorial function.")
def factorial(n):
    if not isinstance(n, int):
        raise TypeError("factorial expects an integer")
    if n < 0:
        raise ValueError("factorial not defined for negative numbers")
    if n == 0:
        return 1
    return n * factorial(n - 1)

# Caller handles possible recursion depth problems or invalid input
try:
    print(factorial(4))    
    print(factorial(-1))     

    # Uncomment to see RecursionError for very large n (e.g., factorial(1000000))
    # print(factorial(10**6))
except (ValueError, TypeError) as e:
    print("Input error:", e)
except RecursionError as e:
    print("Recursion error (too deep):", e)
print("###########################################")

# 28. Write a program that simulates transaction rollback in a banking system using exceptions.
print("28. Write a program that simulates transaction rollback in a banking system using exceptions.")
class TransactionError(Exception):
    pass
# Initial account balance
balance = 100
print("balance at start:", balance)
# Take a "snapshot" of balance before transaction
snapshot = balance
try:
    # Start transaction
    # withdraw 80
    balance -= 80  
    print("During transaction, Balance:", balance)
    # Simulate a problem
    raise TransactionError("Something went wrong during withdrawal!") 
except TransactionError as e:
    # Rollback to snapshot if error occurs
    print("Error occurred:", e)
    # rollback
    balance = snapshot  
    print("Transaction rolled back")
print("After:", balance)
print("###########################################")

# 29. Write a program to validate credit card numbers and raise exceptions for invalid inputs.
print("29. Write a program to validate credit card numbers and raise exceptions for invalid inputs.")
class InvalidCardError(Exception):
    pass

def validate_card(number):
    # check digits only
    if not number.isdigit():
        raise InvalidCardError("Card must contain only digits.")
    # check length
    if len(number) not in (13, 15, 16, 19):
        raise InvalidCardError("Invalid card length.")
    # simple Luhn check
    # digits = [int(d) for d in number[::-1]]
    # total = 0
    # for i, d in enumerate(digits):
    #     if i % 2 == 1:
    #         d *= 2
    #         if d > 9:
    #             d -= 9
    #     total += d
    # if total % 10 != 0:
    #     raise InvalidCardError("Failed Luhn check.")
    # return True

cards = ["4242424242424242", "1234567890123456"]
for card in cards:
    try:
        validate_card(card)
        print(card, "is valid!")
    except InvalidCardError as e:
        print(card, "is invalid:", e)
print("###########################################")

# 30. Write a program that raises an exception if memory usage goes beyond a threshold.
print("30. Write a program that raises an exception if memory usage goes beyond a threshold.")
class MemoryThresholdExceeded(Exception):
    pass

THRESHOLD_MB = 10  # small for demo

# tracemalloc is a built-in Python module that tracks memory allocations inside Python objects.
# USEFUL : for debugging memory leaks or monitoring memory in a program.
# start tracking memory
tracemalloc.start()

# simulate memory usage by creating a large list
data = [0] * 5_000_000

# tracemalloc.get_traced_memory() returns two values (in bytes)
current, peak = tracemalloc.get_traced_memory()
current_mb = peak / (1024 * 1024)

print(f"Current memory usage: {current_mb:.2f} MB (threshold {THRESHOLD_MB} MB)")

if current_mb > THRESHOLD_MB:
    raise MemoryThresholdExceeded(f"Memory {current_mb:.2f} MB exceeded {THRESHOLD_MB} MB")
tracemalloc.stop()