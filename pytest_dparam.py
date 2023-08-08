from typing import Any
from collections.abc import Iterable
import pytest


class InvalidParametrizedArgument(BaseException):
	pass


class MismatchedParametrizedArguments(BaseException):
	pass


def __assert_matching_arguments(
	ref_args: tuple[str, ...],
	other_args: tuple[str, ...],
) -> None:
	if ref_args != other_args:
		raise MismatchedParametrizedArguments(
			f"Mismatch in argument lists for parametrized tests: {ref_args} vs {other_args}"
		)


def d_parametrize(test_cases: dict[str, dict[str, Any] | Iterable[dict[str, Any]]]):
	"""
	The decorator @d_parametrize(…) can be used in lieu of @pytest.mark.parametrize(…).
	Parametrized test cases are provided as an input as a dictionary of cases.
	```
	@d_parametrize(
	  {
	    <case_name>: {<arg1>: <value>, <arg2>: <value>, …},
	    <case_name>: {<arg1>: <value>, <arg2>: <value>, …},
	    <case_name>: [
	      {<arg1>: <value>, <arg2>: <value>, …},
	      {<arg1>: <value>, <arg2>: <value>, …},
	    ],
	    …
	  }
	)
	def test_function(…): …
	```
	See: https://github.com/Bunker-D/pytest-dict-parammetrized.
	"""
	arguments = None
	cases = []
	for case_name, case_descr in test_cases.items():
		if isinstance(case_descr, dict):
			case_descr = (case_descr,)
		else:
			case_descr = tuple(case_descr)
			if len(case_descr) > 1:
				case_name += "_"
		for single_case in case_descr:
			args = tuple(single_case.keys())
			if arguments is None:
				arguments = args
			else:
				__assert_matching_arguments(arguments, args)
			cases.append(pytest.param(*single_case.values(), id=case_name))
	return pytest.mark.parametrize(arguments, cases)
