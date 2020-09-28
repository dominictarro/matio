from numpy import ndarray
from typing import Union, List, NewType
import _coo
import _dok

_FORMATS = {
	'dok': _dok,
	'coo': _coo
}

__doc__ = '''matio.sparse provides simple io callables for sparse matrix formats'''


def read(fn: str, method: str = 'dok', delimiter: str = ' ', dtype: type = float, **kwargs) -> ndarray:
	"""
	Read a sparse-formatted file into a NumPy array

	:param fn:          file name
	:param cols:        dimensions of NumPy array (rows, cols)
	:param method:      sparsity format
	:param delimiter:   delimiter
	:param dtype:       data type to impose upon the read
	:return:            NumPy array of values
	"""

	try:
		return _FORMATS[method].desparsify(fn=fn, delimiter=delimiter, dtype=dtype, **kwargs)
	except KeyError:
		raise LookupError(f"unknown method: {method}")


def write(data: Union[ndarray, list], fn: str, method: str = 'dok', delimiter: str = ' '):
	"""

	:param data:        data to be saved in sparse formaat
	:param fn:          file name
	:param method:      sparsity format
	:param delimiter:   delimiter
	:return:
	"""
	try:
		return _FORMATS[method].sparsify(data=data, fn=fn, delimiter=delimiter)
	except KeyError:
		raise LookupError(f"unknown method: {method}")

