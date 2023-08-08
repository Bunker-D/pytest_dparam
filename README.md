# Dictionary-based test parametrization for `pytest`

The decorator `@d_parametrize` (defined in `pytest_dparam`) offers an arguably more readable alternative to `@pytest.mark.parametrize`.

Test cases are configured through a dictionary so that:
- The name for each test case *precedes* its definition (the list of values to be used),
- The name for each argument/value is repeated in the test case definition.

Additionally, test cases covering the same topic can be bundled under the same name.

## Syntax

`d_parametrize` takes as its input a dictionary, whose items are the different test cases or sets of test cases. As an example:

```python
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
```

The keys are the names given to each test case or set of test cases.

### Defining an isolated test case

Each test case is described by a dictionary where the keys are the name of the arguments to be defined
(which would be the first argument of `pytest.mark.parametrize`),
and the values are the values to be given to said arguments.

For example, to ensure that our `square` function returns `1` for both `1` and `-1`:

```python
@d_parametrize(
    {
        "trivial_case": {"input": 1, "expected": 1},
        "negative_trivial_case": {"input": -1, "expected": 1},
    }
)
def test_square(input: int, expected: int):
    assert square(input) == expected
```

⚠ **All test cases must include the same keys in the same order.**
Otherwise, exception `pytest_dparam.InvalidParametrizedArgument` will be raised.

### Bundling cases together

It can be useful to provide several test cases to cover similar situations, calling for a same name.
In such a case, a list of test-case-describing dictionaries (or actually, any iterable of such dictionaries) can be provided instead of a single dictionary.

For example, if we want to test `square` with different negative numbers just to be sure:
```python
@d_parametrize(
    {
        # ...
        "negative_integers": [
            {"input": -2, "expected": 4},
            {"input": -3, "expected": 9},
        ],
    }
)
def test_square(input: int, expected: int):
    assert square(input) == expected
```

The name given to the set of test cases will be used for each included test case, with a numbered suffix (e.g., `negative_integers_0` and `negative_integers_1` in the previous example).

### Pseudo-bundling isolated cases for readability

For readability, you might appreciate having one line for the test case name, followed by a single-line test case description.
However, a code formatter such as Black can get in the way.

Or you might appreciate using lists all the time for consistency.

In any case, you can put an isolated test cases within a list. If it is alone in the list, its name will not be affected:
```python
@d_parametrize(
    {
        "trivial_case": [
            {"input": 1, "expected": 1},
        ],
        "negative_trivial_case": [
            {"input": -1, "expected": 1},
        ],
    }
)
def test_square(input: int, expected: int):
    assert square(input) == expected
```


## Under the hood

`d_parametrize(…)` actually just calls `pytest.mark.parametrize(…)` with the proper arguments,
based on the provided parametrization-describing dictionary,
and after asserting that the included test cases are compatible and valid.

Ultimately:
```python
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
```
is literally equivalent to:
```python
@pytest.mark.parametrize(
    ("input", "expected"),
    [
        pytest.mark.parametrize( 1, 1, id="trivial_case"),
        pytest.mark.parametrize(-1, 1, id="negative_trivial_case"),
        pytest.mark.parametrize( 2, 4, id="positive_integers_"),
        pytest.mark.parametrize( 3, 9, id="positive_integers_"),
        pytest.mark.parametrize(-2, 4, id="negative_integers_"),
        pytest.mark.parametrize(-3, 9, id="negative_integers_"),
    ]
)
def test_square(input: int, expected: int):
    assert square(input) == expected
```
