import numpy as np
from numpy.linalg import det, inv


C = ((10, 5), (5, 10))
C = np.array(C)
D = ((-10, -5), (-1, -10))
D = np.array(D)
h = np.array((100, 50))
h.shape = 2, 1  # Convert h into 2 by 1 vector
A = C - D
det(A)
A_inv = inv(A)
p = A_inv @ h
# print(p)

# Exercise 1
e = (-10, -15, -5)
e = np.array(e)
e.shape = 3, 1
h = (90, 60, 50)
h = np.array(h)
h.shape = 3, 1
C = ((20, 0, 0), (0, 15, 0), (0, 0, 10))
C = np.array(C)
D = ((-15, 5, 5), (5, -10, 10), (5, 5, -5))
D = np.array(D)
A = C - D
b = h - e
det(A)
A_inv = inv(A)
p = A_inv @ b
# print(p)

# Exercise 2
A = ((1, -9), (1, -7), (1, -3))
A = np.array(A)
b = np.array((1, 3, 8))
b.shape = 3, 1
A_transpose = A.transpose()
x_hat = inv((A_transpose @ A))@A_transpose@b
print(x_hat)
