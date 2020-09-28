from typing import Union
import numpy as np
import re
from _utils import cast_rcv

__doc__ = '''
Functions for reading and writing datasets with Coordinate List format (COO)

COO formatting:

Matrix
|   0   1   2   0   0   |
|   3   0   0   1   0   |
|   0   0   0   0   2   |

Conventional
0,2,1
1,0,0
0,0,-1

COO
0,0,1,1,2
1,2,0,3,4
1,2,3,1,2
'''


def desparsify(fn: str, delimiter: str = ' ', dtype: type = float) -> np.ndarray:
	"""

	:param fn:          file name
	:param delimiter:   delimiter
	:param dtype:       data type to impose upon the read
	:return:            NumPy array of values
	"""
	regex = re.compile(f"[^0-9.{delimiter}]")
	with open(fn, 'r') as infile:
		generator = infile.readlines()[:3]

		# Strip unrelated characters
		for i, indices in enumerate(generator):
			indices = regex.sub('', indices)
			generator[i] = [dtype(x) for x in indices.split(delimiter)]

		# Row length should usually be the last index
		n = int(max(generator[0])) + 1
		m = int(max(generator[1])) + 1

		data = np.zeros((n, m), dtype=dtype)

		# Extract indices for row and column and use them to place value in 'data'
		for pointer, i in enumerate(generator[0]):
			i = int(i)
			j, val = int(generator[1][pointer]), int(generator[2][pointer])
			data[i][j] = val

	return data


def sparsify(data: Union[np.ndarray, list, tuple], fn: str, delimiter: str = ' '):
	"""

	:param matrix:      matrix of data to be written in DOK format
	:param fn:          file name
	:param delimiter:   delimiter
	:return:            None
	"""
	rcv = cast_rcv(data)

	with open(fn, 'w') as f:
		f.write("\n".join([delimiter.join(x.astype(str)) for x in rcv]))
