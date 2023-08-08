from typing import Any
from pytest_dparam import *
import pytest


def case(*kargs, id: str = None) -> tuple[Any, ...]:
	return (id, *kargs)


def parametrize_mock(inputs, cases):
	return (inputs, tuple(cases))


class Test_pytest_parametrize:
	def test_split_cases(_, monkeypatch: pytest.MonkeyPatch):
		monkeypatch.setattr("pytest.mark.parametrize", parametrize_mock)
		monkeypatch.setattr("pytest.param", case)
		dict_config = {
			"empty_inputs": {"a": "", "b": "", "expected": ""},
			"sgl_char_inputs": {"a": "a", "b": "b", "expected": "ab"},
			"none_input": {"a": None, "b": "b", "expected": None},
		}
		std_parametrize_input_equivalent = (
			("a", "b", "expected"),
			(
				pytest.param("", "", "", id="empty_inputs"),
				pytest.param("a", "b", "ab", id="sgl_char_inputs"),
				pytest.param(None, "b", None, id="none_input"),
			),
		)
		assert d_parametrize(dict_config) == std_parametrize_input_equivalent

	def test_with_arg_named_id(_, monkeypatch: pytest.MonkeyPatch):
		monkeypatch.setattr("pytest.mark.parametrize", parametrize_mock)
		monkeypatch.setattr("pytest.param", case)
		dict_config = {
			"empty_inputs": {"id": "", "b": "", "expected": ""},
			"sgl_char_inputs": {"id": "a", "b": "b", "expected": "ab"},
			"none_input": {"id": None, "b": "b", "expected": None},
		}
		std_parametrize_input_equivalent = (
			("id", "b", "expected"),
			(
				pytest.param("", "", "", id="empty_inputs"),
				pytest.param("a", "b", "ab", id="sgl_char_inputs"),
				pytest.param(None, "b", None, id="none_input"),
			),
		)
		assert d_parametrize(dict_config) == std_parametrize_input_equivalent

	def test_with_bundled_cases_as_list(_, monkeypatch: pytest.MonkeyPatch):
		monkeypatch.setattr("pytest.mark.parametrize", parametrize_mock)
		monkeypatch.setattr("pytest.param", case)
		dict_config = {
			"with_none": {"input": None, "times_ten": 0},
			"with_int": [
				{"input": 0, "times_ten": 0},
				{"input": 3, "times_ten": 30},
			],
			"with_str": [
				{"input": "", "times_ten": 0},
				{"input": "7", "times_ten": 70},
			],
		}
		std_parametrize_input_equivalent = (
			("input", "times_ten"),
			(
				pytest.param(None, 0, id="with_none"),
				pytest.param(0, 0, id="with_int_"),
				pytest.param(3, 30, id="with_int_"),
				pytest.param("", 0, id="with_str_"),
				pytest.param("7", 70, id="with_str_"),
			),
		)
		assert d_parametrize(dict_config) == std_parametrize_input_equivalent

	def test_with_bundled_cases_as_tuple(_, monkeypatch: pytest.MonkeyPatch):
		monkeypatch.setattr("pytest.mark.parametrize", parametrize_mock)
		monkeypatch.setattr("pytest.param", case)
		dict_config = {
			"with_none": {"input": None, "times_ten": 0},
			"with_int": (
				{"input": 0, "times_ten": 0},
				{"input": 3, "times_ten": 30},
			),
			"with_str": (
				{"input": "", "times_ten": 0},
				{"input": "7", "times_ten": 70},
			),
		}
		std_parametrize_input_equivalent = (
			("input", "times_ten"),
			(
				pytest.param(None, 0, id="with_none"),
				pytest.param(0, 0, id="with_int_"),
				pytest.param(3, 30, id="with_int_"),
				pytest.param("", 0, id="with_str_"),
				pytest.param("7", 70, id="with_str_"),
			),
		)
		assert d_parametrize(dict_config) == std_parametrize_input_equivalent

	def test_with_bundled_cases_as_iter(_, monkeypatch: pytest.MonkeyPatch):
		monkeypatch.setattr("pytest.mark.parametrize", parametrize_mock)
		monkeypatch.setattr("pytest.param", case)
		dict_config = {
			"with_none": {"input": None, "times_ten": 0},
			"with_int": (
				c
				for c in (
					{"input": 0, "times_ten": 0},
					{"input": 3, "times_ten": 30},
				)
			),
			"with_str": (
				c
				for c in (
					{"input": "", "times_ten": 0},
					{"input": "7", "times_ten": 70},
				)
			),
		}
		std_parametrize_input_equivalent = (
			("input", "times_ten"),
			(
				pytest.param(None, 0, id="with_none"),
				pytest.param(0, 0, id="with_int_"),
				pytest.param(3, 30, id="with_int_"),
				pytest.param("", 0, id="with_str_"),
				pytest.param("7", 70, id="with_str_"),
			),
		)
		assert d_parametrize(dict_config) == std_parametrize_input_equivalent

	def test_dont_change_single_case_bundle_name(_, monkeypatch: pytest.MonkeyPatch):
		monkeypatch.setattr("pytest.mark.parametrize", parametrize_mock)
		monkeypatch.setattr("pytest.param", case)
		dict_config = {
			"with_none": {"input": None, "times_ten": 0},
			"with_int": [
				{"input": 3, "times_ten": 30},
			],
			"with_str": [
				{"input": "", "times_ten": 0},
				{"input": "7", "times_ten": 70},
			],
		}
		std_parametrize_input_equivalent = (
			("input", "times_ten"),
			(
				pytest.param(None, 0, id="with_none"),
				pytest.param(3, 30, id="with_int"),
				pytest.param("", 0, id="with_str_"),
				pytest.param("7", 70, id="with_str_"),
			),
		)
		assert d_parametrize(dict_config) == std_parametrize_input_equivalent

	@pytest.mark.parametrize(
		("error_case"),
		(  # ok would be {'a': …,'b':…,'c':…}
			pytest.param({"a": 0, "b": 0, "c": 0, "d": 0}, id="one_too_many"),
			pytest.param({"a": 0, "c": 0}, id="one_too_few"),
			pytest.param({"b": 0, "a": 0, "c": 0}, id="wrong_order"),
		),
	)
	def test_error_for_keys_mismatch(_, error_case):
		dict_config = {
			"valid": {"a": 1, "b": 1, "c": 1},
			"ok": {"a": 2, "b": 2, "c": 2},
			"error": error_case,
			"can_do": {"a": 3, "b": 3, "c": 3},
		}
		with pytest.raises(MismatchedParametrizedArguments):
			d_parametrize(dict_config)

	@pytest.mark.parametrize(
		("error_case"),
		(  # ok would be {'a': …,'b':…,'c':…}
			pytest.param({"a": 0, "b": 0, "c": 0, "d": 0}, id="one_too_many"),
			pytest.param({"a": 0, "c": 0}, id="one_too_few"),
			pytest.param({"b": 0, "a": 0, "c": 0}, id="wrong_order"),
		),
	)
	def test_error_for_keys_mismatch_in_bundle(_, error_case):
		dict_config = {
			"valid": {"a": 1, "b": 1, "c": 1},
			"ok": [
				{"a": 2, "b": 2, "c": 2},
				{"a": -2, "b": -2, "c": -2},
			],
			"error": [
				{"a": 0, "b": 0, "c": 0},
				error_case,
			],
			"can_do": {"a": 3, "b": 3, "c": 3},
		}
		with pytest.raises(MismatchedParametrizedArguments):
			d_parametrize(dict_config)
