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
print(p)