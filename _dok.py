from typing import Union
import numpy as np
import re

__doc__ = '''
Functions for reading and writing datasets with Dictionary of Keys format (dok)

Dictionary of Keys formatting:

Matrix
| 0   2   1 |
| 1   0   0 |
| 0   0  -1 |

Conventional
0,2,1
1,0,0
0,0,-1

DOK
1:2,2:1
0:1
2:-1
'''


def desparsify(fn: str, columns: Union[int, str] = "auto", delimiter: str = ' ', dtype: type = float) -> np.ndarray:
	"""

	:param fn:          file name
	:param columns:     number of columns to build
	:param delimiter:   delimiter
	:param dtype:       data type to impose upon the read
	:return:            NumPy array of values
	"""

	with open(fn, 'r') as infile:
		generator = infile.readlines()
		if columns == "auto":
			# Compile regex matcher for values between ':' and the delimiter (eliminates the element)
			non_col_regex = re.compile(f":.*?[0-9]|^:.*:?|\n")
			string = delimiter.join(generator)
			string = non_col_regex.sub(delimiter, string)
			# Get the largest column value, add 1, we have columns to build
			columns = max([int(x) for x in string.split(delimiter) if x]) + 1
		# Generate matrix
		data = np.zeros((len(generator), columns))
		regex = re.compile(f"[^0-9:.{delimiter}]")

		for i, row in enumerate(generator):
			# Strip unrelated characters
			row = regex.sub('', row)
			# Break each line by delimiter
			for pair in row.split(delimiter):
				# If not a null value (e.g. '')
				if pair:
					j, value = pair.split(':')
					data[i][int(j)] = dtype(value)

	return data


def sparsify(data: Union[np.ndarray, list, tuple], fn: str, delimiter: str = ' '):
	"""

	:param matrix:      matrix of data to be written in DOK format
	:param fn:          file name
	:param delimiter:   delimiter
	:return:            None
	"""
	lines = [delimiter.join([f"{j}:{x}" for j, x in enumerate(row) if x]) for row in data]
	with open(fn, 'w') as outfile:
		outfile.writelines(lines)
