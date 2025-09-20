# Basic Level

# 1. Write a program to handle division by zero using try-except.
print("1. Write a program to handle division by zero using try-except.")
try:
    num1 = float(input("Enter Numerator:"))
    num2 = float(input("Enter Denominator:"))
    result = num1/num2
except ZeroDivisionError:
    print("ERROR: Cannot divide by zero.")
else:
    print(f"Result: {result}")
print("###########################################")

# 2. Write a program to handle invalid user input (string instead of number).
print("2. Write a program to handle invalid user input (string instead of number).")
try:
    num = int(input("Enter a numeric value:"))
except ValueError:
    print("ERROR! Invalid input: please enter a number.")
else:
     print("You entered:", num)
print("###########################################")

# 3. Write a program that catches IndexError when accessing a list element.
print("3. Write a program that catches IndexError when accessing a list element.")
try:
    topics = ["DE", "DS", "GenAI","ML"]
    print(f"Topics: {topics}")
    input_index = int(input("Enter the index of item you want to select(Starts with 0):"))
    print("Item at index:", topics[input_index])
except IndexError:
    print(f"ERROR! Index out of range. Choose between 0 and, {len(topics)-1}")
print("###########################################")

# 4. Write a program to open a file and handle FileNotFoundError.
print("4. Write a program to open a file and handle FileNotFoundError.")
try:
    file_path = "temp.json"
    with open(file_path,"r",encoding="utf-8") as f:
        print(f.read())
except FileNotFoundError:
    print("ERROR! File not found:", file_path)
print("###########################################")

# 5. Write a program that handles multiple exceptions (ZeroDivisionError, ValueError).
print("5. Write a program that handles multiple exceptions (ZeroDivisionError, ValueError).")
try:
    a = int(input("Enter numerator (int): "))
    b = int(input("Enter denominator (int): "))
    print("Division result:", a / b)
except ZeroDivisionError:
    print("ERROR! Cannot divide by zero.")
except ValueError:
    print("ERROR! Please enter a valid number.")
print("###########################################")

# 6. Write a program using try-except-else to check if a number is even.
print("6. Write a program using try-except-else to check if a number is even.")
try:
    num = int(input("Enter a number:"))
except ValueError:
    print("ERROR! Please enter a valid number.")
else:
    if num % 2 == 0:
        print("Number is even")
    else:
        print("Number is odd")
print("###########################################")

# 7. Write a program with finally block to always display "Execution Completed".
print("7. Write a program with finally block to always display 'Execution Completed'.")
try:
    x = int(input("Enter a number: "))
    print(f"Number: {x}")
except ValueError:
    print("ERROR! Please enter a number.")
finally:
    print("Execution Completed.")
print("###########################################")

# 8. Write a program to demonstrate nested try-except blocks.
print("8. Write a program to demonstrate nested try-except blocks.")
try: 
    num1 = int(input("Enter a Numerator: "))
    num2 = int(input("Enter a Denominator: "))
    try:
        result = num1/num2
        print(f"result: {result}")
    except ZeroDivisionError:
        print("ERROR! Cannot divide by zero.")
except:
    print("ERROR! Please enter a number.")
print("###########################################")

# 9. write a program that asks for two numbers and handles both division and conversion errors.
print("9, Write a program that asks for two numbers and handles both division and conversion errors.")
try:
    a = input("Enter first number: ")
    b = input("Enter second number: ")
    a = float(a)  
    b = float(b)  
    print("Result =", a / b)
except ValueError:
    print("Conversion error: please enter valid numbers.")
except ZeroDivisionError:
    print("Division error: denominator cannot be zero.")
print("###########################################")

# 10. Write a program that raises and handles a TypeError.
print("10. Write a program that raises and handles a TypeError.")
try:
    # this wont give error
    m = [1,2,3,4]
    # len expects a sequence; passing an int causes TypeError
    n = 10
    print(len(n))
except TypeError as e:
    print("ERROR! Caught TypeError:", e)