"""
CS 4660 - Lab 1
Chelle Cruz
"""
#1. Import the numpy package with the alias np
import numpy as np

#2. Create a vector of zeros of size 10 but the fifth value which is 1
zeroes = np.zeros(10, dtype=int)
zeroes[4] = 1
print(zeroes)

#3. Create a 3 X 3 array of any values. Add a column of ones to the end
a = np.arange(10, 19).reshape((3,3))
a[:, -1:] = 1
print(a)

#4. Create a vector with values ranging from 10 to 49
b = np.arange(10, 50)
print(b)

#5. Reverse the above vector (first element becomes last)
b = b[::-1]
print(b)

#6. Create a 4x4 matrix with values ranging from 0 to 15
c = np.arange(16).reshape((4,4))
print(c)

#7. Create a 3x3x3 array with random values
d = np.floor(50 * np.random.random((3,3,3))).astype(int)
print(d)

#8. Create a 10x10 array with random values and find the minimum and maximum values
random_array = np.floor(50 * np.random.random((10,10))).astype(int)
print(random_array)
print("Min:", random_array.min())
print("Max:", random_array.max())

#9. Create a random vector of size 30 and find the mean value
e = np.floor(50 * np.random.random((30,))).astype(int)
print(e)
print("Mean:", np.mean(e))

#10. What does NaN mean? Submit in a comment
#NaN = not a number

#11. Write a function that takes 1D array and negates all elements which are between 3 and 8, in place. Demo it with an array of your choosing
# Negate elements between 3 and 8 on array
def negate(array):
    array[(3 <= array) & (array <= 8)] *= -1

negate(e)
print(e)