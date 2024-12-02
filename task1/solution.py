import unittest


def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        param_types = {k: v for k, v in annotations.items() if k != 'return'}

        if len(args) != len(param_types):
            raise TypeError("Количество переданных аргументов не соответствует прототипу функции.")

        for value, (param, expected_type) in zip(args, param_types.items()):
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"Аргумент '{param}' должен быть типа {expected_type.__name__}, но получен {type(value).__name__}.")

        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


@strict
def concat_strings(a: str, b: str) -> str:
    return a + b


@strict
def is_equal(a: bool, b: bool) -> bool:
    return a == b


class TestStrictDecorator(unittest.TestCase):

    def test_sum_two_correct(self):
        self.assertEqual(sum_two(1, 2), 3)

    def test_sum_two_incorrect_type(self):
        with self.assertRaises(TypeError) as context:
            sum_two(1, 2.4)
        self.assertIn("Аргумент 'b' должен быть типа int", str(context.exception))

    def test_concat_strings_correct(self):
        self.assertEqual(concat_strings("hello", " world"), "hello world")

    def test_concat_strings_incorrect_type(self):
        with self.assertRaises(TypeError) as context:
            concat_strings("hello", 5)
        self.assertIn("Аргумент 'b' должен быть типа str", str(context.exception))

    def test_is_equal_correct(self):
        self.assertTrue(is_equal(True, True))
        self.assertFalse(is_equal(True, False))

    def test_is_equal_incorrect_type(self):
        with self.assertRaises(TypeError) as context:
            is_equal(True, 1)
        self.assertIn("Аргумент 'b' должен быть типа bool", str(context.exception))

    def test_wrong_argument_count(self):
        with self.assertRaises(TypeError) as context:
            sum_two(1)
        self.assertIn("Количество переданных аргументов не соответствует прототипу функции", str(context.exception))


if __name__ == "__main__":
    unittest.main()
