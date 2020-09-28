import numpy as np


def cast_rcv(data: np.ndarray) -> np.ndarray:
	"""
	Takes a NumPy 2D matrix and returns an index matrix of non-zero values
		ndarray([
		[row indices],
		[column indices],
		[elements])

	:param matrix: NumPy 2D array
	:return: NumPy 2D array
	"""
	# Determine number of values to be included
	non_zero = np.count_nonzero(data)
	# Create (3, non_zero) sized matrix
	row_col_val = np.zeros((3, non_zero))
	pointer = 0
	# Row values are ordered
	# Iterate through and for each indexing array, insert the appropriate values
	for i, row in enumerate(data):
		for j, val in enumerate(row):
			if val != 0:
				row_col_val[0][pointer] = i
				row_col_val[1][pointer] = j
				row_col_val[2][pointer] = val
				pointer += 1

	return row_col_val
