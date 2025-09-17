# Write a function sum_all(*args) that returns the sum of all numbers passed.

# Write a function concat_strings(*args) that joins all string arguments into one string.

# Write a function max_number(*args) that returns the maximum value passed.
# Write a function unpack_args(*args) that takes nested lists/tuples and flattens them.

# What happens if you pass a list directly vs. using unpacking (*list) when calling a function with *args? 
# Show with an example.

# Write a function reverse_args(*args) that prints arguments in reverse order.

# What will be the output?



#### 1
def sum_all(*args):
    return sum(args)

#### 2
def concat_strings(*args):
    return ''.join(args)

#### 3
def max_number(*args):
    return max(args)

#### 4
def unpack_args(*args):
    flattened = []
    for i in args:
        #flattened.append(i)
        flattened.extend(i)
    return flattened

def unpack_args(*args):
    """Recursively flatten arbitrarily nested lists/tuples passed via *args into one list."""
    flattened = []
    for a in args:
        if isinstance(a, (list, tuple)):
            flattened.extend(unpack_args(*a))   # recursive call
        else:
            flattened.append(a)
    return flattened

#### 5
def func5_1(*args):
    return args

def func5_2(argsList):
    return argsList

#### 6
def reverse_args(*args):
    return args[::-1]


#1
sum_result = sum_all(5,6,7,8)
print(f"Sum: {sum_result}")

#2
concat_result = concat_strings("Hello", " ", "Udit", "!")
print(f"Concatenated String: {concat_result}")  

#3
max_result = max_number(5,6,7,8)
print(f"Max Number: {max_result}")

#4
unpacked_list = unpack_args([1,2], (3,4), [5,6])
print(f"Unpacked Args: {unpacked_list}")

#5
func5_1_result = func5_1([1,2,3])
func5_2_result = func5_2([1,2,3])
print(f"func5_1 with list: {func5_1_result}") 
print(f"func5_2 with list: {func5_2_result}")  

#6
reversed_args = reverse_args(1,2,3,4,5)
print(f"Reversed Args: {reversed_args}")
