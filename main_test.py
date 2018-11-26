import unittest
from main import flatten

class TestFlattenDict(unittest.TestCase):

    def test_flatten(self):
        input = {
            "foo": {
                "bar": {
                    "one": 1,
                    "two": 2,
                }
            },
            "bar": {
                "one": 1,
                "two": 2,
            }
        }
        expected = {
            "foo.bar.one": 1,
            "foo.bar.two": 2,
            "bar.one": 1,
            "bar.two": 2,
        }
        out = flatten(input)
        self.assertEqual(out, expected)



if __name__ == '__main__':
    unittest.main()