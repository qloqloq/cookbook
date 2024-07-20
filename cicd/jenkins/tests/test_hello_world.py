import unittest
from unittest import TestCase

from main.hello_world import HelloWorld


class TestHelloWorld(TestCase):
    def test_should_output_hello_world(self):
        actual_output = HelloWorld().hello()
        expected_output = 'Hello World.'
        self.assertEqual(expected_output, actual_output)


if __name__ == '__main__':
    unittest.main()
