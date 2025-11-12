# %% [markdown]
# # Python Fundamentals
# 
# This notebook covers the essential concepts of Python programming, including:
# - Variables and Data Types
# - Operators
# - Control Flow (if/else, loops)
# - Functions
# - Data Structures (lists, tuples, dictionaries, sets)
# - Basic Object-Oriented Programming

# %% [markdown]
# ## 1. Variables and Data Types
# 
# Python has several built-in data types:
# - **int**: Integer numbers
# - **float**: Decimal numbers
# - **str**: Text/strings
# - **bool**: True/False values

# %%
# Variables and basic data types
name = "Alice"  # string
age = 25  # integer
height = 5.6  # float
is_student = True  # boolean

print(f"Name: {name}, Type: {type(name)}")
print(f"Age: {age}, Type: {type(age)}")
print(f"Height: {height}, Type: {type(height)}")
print(f"Is Student: {is_student}, Type: {type(is_student)}")

# %% [markdown]
# ## 2. Operators
# 
# Python supports various operators for performing operations on variables.

# %%
# Arithmetic operators
a = 10
b = 3

print("Arithmetic Operators:")
print(f"Addition: {a} + {b} = {a + b}")
print(f"Subtraction: {a} - {b} = {a - b}")
print(f"Multiplication: {a} * {b} = {a * b}")
print(f"Division: {a} / {b} = {a / b}")
print(f"Floor Division: {a} // {b} = {a // b}")
print(f"Modulus: {a} % {b} = {a % b}")
print(f"Exponentiation: {a} ** {b} = {a ** b}")

# %%
# Comparison operators
x = 5
y = 10

print("\nComparison Operators:")
print(f"{x} == {y}: {x == y}")
print(f"{x} != {y}: {x != y}")
print(f"{x} < {y}: {x < y}")
print(f"{x} > {y}: {x > y}")
print(f"{x} <= {y}: {x <= y}")
print(f"{x} >= {y}: {x >= y}")

# %%
# Logical operators
print("\nLogical Operators:")
print(f"True and False: {True and False}")
print(f"True or False: {True or False}")
print(f"not True: {not True}")

# %% [markdown]
# ## 3. Control Flow
# 
# ### If-Else Statements

# %%
# If-else statements
temperature = 25

if temperature > 30:
    print("It's hot outside!")
elif temperature > 20:
    print("It's a pleasant day!")
elif temperature > 10:
    print("It's a bit cool.")
else:
    print("It's cold outside!")

# %% [markdown]
# ### Loops
# 
# **For loops** iterate over sequences, while **while loops** continue until a condition is false.

# %%
# For loop
print("For loop example:")
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(f"I like {fruit}")

# For loop with range
print("\nCounting from 1 to 5:")
for i in range(1, 6):
    print(i)

# %%
# While loop
print("While loop example:")
count = 0

while count < 5:
    print(f"Count is: {count}")
    count += 1

print("Loop finished!")

# %% [markdown]
# ## 4. Functions
# 
# Functions are reusable blocks of code that perform specific tasks.

# %%
# Basic function
def greet(name):
    """Function to greet a person"""
    return f"Hello, {name}!"

# Function with multiple parameters
def add_numbers(a, b):
    """Function to add two numbers"""
    return a + b

# Function with default parameter
def power(base, exponent=2):
    """Function to calculate power with default exponent of 2"""
    return base ** exponent

# Testing functions
print(greet("Bob"))
print(f"5 + 3 = {add_numbers(5, 3)}")
print(f"4^2 = {power(4)}")
print(f"2^5 = {power(2, 5)}")

# %% [markdown]
# ## 5. Data Structures
# 
# ### Lists
# Lists are ordered, mutable collections that can contain items of different types.

# %%
# Lists
my_list = [1, 2, 3, 4, 5]
print(f"Original list: {my_list}")

# List operations
my_list.append(6)  # Add to end
print(f"After append(6): {my_list}")

my_list.insert(0, 0)  # Insert at position
print(f"After insert(0, 0): {my_list}")

my_list.remove(3)  # Remove specific value
print(f"After remove(3): {my_list}")

popped = my_list.pop()  # Remove and return last item
print(f"Popped value: {popped}")
print(f"After pop(): {my_list}")

# List slicing
print(f"First 3 elements: {my_list[:3]}")
print(f"Last 2 elements: {my_list[-2:]}")
print(f"Every other element: {my_list[::2]}")

# %% [markdown]
# ### Tuples
# Tuples are ordered, immutable collections.

# %%
# Tuples
my_tuple = (1, 2, 3, 4, 5)
print(f"Tuple: {my_tuple}")
print(f"First element: {my_tuple[0]}")
print(f"Length: {len(my_tuple)}")

# Tuple unpacking
x, y, z, *rest = my_tuple
print(f"x={x}, y={y}, z={z}, rest={rest}")

# %% [markdown]
# ### Dictionaries
# Dictionaries store key-value pairs.

# %%
# Dictionaries
person = {
    "name": "John",
    "age": 30,
    "city": "New York",
    "hobbies": ["reading", "gaming"]
}

print(f"Person: {person}")
print(f"Name: {person['name']}")
print(f"Age: {person.get('age')}")

# Adding/modifying entries
person["email"] = "john@example.com"
person["age"] = 31
print(f"\nUpdated person: {person}")

# Dictionary methods
print(f"\nKeys: {list(person.keys())}")
print(f"Values: {list(person.values())}")
print(f"Items: {list(person.items())}")

# Iterating through dictionary
print("\nIterating through dictionary:")
for key, value in person.items():
    print(f"{key}: {value}")

# %% [markdown]
# ### Sets
# Sets are unordered collections of unique elements.

# %%
# Sets
my_set = {1, 2, 3, 4, 5}
print(f"Set: {my_set}")

# Adding elements
my_set.add(6)
print(f"After add(6): {my_set}")

# Set operations
set_a = {1, 2, 3, 4}
set_b = {3, 4, 5, 6}

print(f"\nSet A: {set_a}")
print(f"Set B: {set_b}")
print(f"Union: {set_a | set_b}")
print(f"Intersection: {set_a & set_b}")
print(f"Difference (A - B): {set_a - set_b}")
print(f"Symmetric Difference: {set_a ^ set_b}")

# %% [markdown]
# ## 6. List Comprehensions
# 
# List comprehensions provide a concise way to create lists.

# %%
# List comprehensions
squares = [x**2 for x in range(1, 11)]
print(f"Squares: {squares}")

# With condition
even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
print(f"Even squares: {even_squares}")

# Nested list comprehension
matrix = [[i*j for j in range(1, 4)] for i in range(1, 4)]
print(f"\nMultiplication table:")
for row in matrix:
    print(row)

# %% [markdown]
# ## 7. Basic Object-Oriented Programming
# 
# Classes allow you to create custom objects with attributes and methods.

# %%
# Class definition
class Dog:
    """A simple Dog class"""
    
    # Class variable
    species = "Canis familiaris"
    
    # Constructor
    def __init__(self, name, age):
        self.name = name  # Instance variable
        self.age = age
    
    # Instance method
    def bark(self):
        return f"{self.name} says Woof!"
    
    def description(self):
        return f"{self.name} is {self.age} years old"
    
    # String representation
    def __str__(self):
        return f"Dog(name={self.name}, age={self.age})"

# Creating objects
dog1 = Dog("Buddy", 3)
dog2 = Dog("Max", 5)

print(dog1)
print(dog2)
print(f"\n{dog1.bark()}")
print(dog1.description())
print(f"\nSpecies: {Dog.species}")

# %% [markdown]
# ## 8. Exception Handling
# 
# Handle errors gracefully using try-except blocks.

# %%
# Exception handling
def divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "Error: Cannot divide by zero!"
    except TypeError:
        return "Error: Invalid input types!"
    finally:
        print("Division operation attempted")

print(divide(10, 2))
print(divide(10, 0))
print(divide(10, "2"))

# %% [markdown]
# ## 9. File Operations
# 
# Reading and writing files in Python.

# %%
# Writing to a file
with open('example.txt', 'w') as file:
    file.write("Hello, Python!\n")
    file.write("This is a test file.\n")
    file.write("Learning Python fundamentals.")

print("File written successfully!")

# Reading from a file
with open('example.txt', 'r') as file:
    content = file.read()
    print("\nFile content:")
    print(content)

# Reading line by line
print("\nReading line by line:")
with open('example.txt', 'r') as file:
    for line_number, line in enumerate(file, 1):
        print(f"Line {line_number}: {line.strip()}")

# %% [markdown]
# ## 10. Lambda Functions and Map/Filter/Reduce
# 
# Lambda functions are small anonymous functions.

# %%
# Lambda functions
square = lambda x: x**2
print(f"Square of 5: {square(5)}")

# Map - apply function to all items
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(f"\nOriginal: {numbers}")
print(f"Squared: {squared}")

# Filter - filter items based on condition
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Even numbers: {even_numbers}")

# Reduce - reduce sequence to single value
from functools import reduce
sum_all = reduce(lambda x, y: x + y, numbers)
print(f"Sum of all numbers: {sum_all}")

# %% [markdown]
# ## Summary
# 
# You've now learned the fundamental concepts of Python:
# 
# ✅ Variables and data types
# ✅ Operators (arithmetic, comparison, logical)
# ✅ Control flow (if-else, for, while)
# ✅ Functions and lambda expressions
# ✅ Data structures (lists, tuples, dictionaries, sets)
# ✅ List comprehensions
# ✅ Object-oriented programming basics
# ✅ Exception handling
# ✅ File operations
# ✅ Functional programming concepts (map, filter, reduce)
# 
# Keep practicing these concepts to build a strong foundation in Python! 🐍

