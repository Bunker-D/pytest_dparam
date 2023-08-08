from pytest_dparam import d_parametrize


def square(x: int) -> int:
	return x * x


@d_parametrize(
	{
		"trivial_case": {"input": 1, "expected": 1},  # test_square[trivial_case]
		"negative_trivial_case": [
			{"input": -1, "expected": 1},  # test_square[negative_trivial_case]
		],
		"positive_integers": [
			{"input": 2, "expected": 4},  # test_square[positive_integers_0]
			{"input": 3, "expected": 9},  # test_square[positive_integers_1]
		],
		"negative_integers": [
			{"input": -2, "expected": 4},  # test_square[negative_integers_0]
			{"input": -3, "expected": 9},  # test_square[negative_integers_1]
		],
	}
)
def test_square(input: int, expected: int):
	assert square(input) == expected
