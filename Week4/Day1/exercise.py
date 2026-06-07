import numpy as np
# 🌟 Exercise 1 : Array Creation and Manipulation
# Create a 1D NumPy array containing numbers from 0 to 9.
x = np.arange(10)
print(x)

# 🌟 Exercise 2 : Type Conversion and Array Operations
# Instructions
# Convert a list [3.14, 2.17, 0, 1, 2] into a NumPy array and convert its data type to integer.
li = [3.14, 2.17, 0, 1, 2]
x = np.array(li, dtype=int)
print(x)

# 🌟 Exercise 3 : Working with Multi-Dimensional Arrays
# Instructions
# Create a 3x3 NumPy array with values ranging from 1 to 9.
a = np.arange(1, 10).reshape(3, 3)
print(a)

# 🌟 Exercise 4 : Creating Multi-Dimensional Array with Random Numbers
# Instructions
# Create a 2D NumPy array of shape (4, 5) filled with random numbers.
b = np.random.rand(4, 5)
print(b)

# 🌟 Exercise 5 : Indexing Arrays
# Instructions
# Select the second row from a given 2D NumPy array.
array = np.array([[21,22,23,22,22],[20, 21, 22, 23, 24],[21,22,23,22,22]])
print(array[1])

# Exercise 6 : Reversing elements
# Instructions
# Reverse the order of elements in a given 1D NumPy array (first element becomes last).
d = np.array([9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
reversed_d = d[::-1]
print(reversed_d)

# 🌟 Exercise 7 : Identity Matrix
# Instructions
# Create a 4x4 identity matrix using NumPy.
matrix = np.zeros((4, 4))
np.fill_diagonal(matrix, 1)
print(matrix)

# 🌟 Exercise 8 : Simple Aggregate Funcs
# Instructions
# Find the sum and average of a given 1D array.
d_sum = d.sum()
d_mean = d.mean()
print(f'sum: {d_sum}, mean:{d_mean}')

# 🌟 Exercise 9 : Create Array and Change its Structure
# Instructions
# Create a NumPy array with elements from 1 to 20; then reshape it into a 4x5 matrix.
f = np.arange(1, 21).reshape(4, 5)
print(f)

# 🌟 Exercise 10 : Conditional Selection of Values
# Instructions
# Extract all odd numbers from a given NumPy array.
print(d[d%2 == 1])