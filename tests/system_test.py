import unittest


class InterpreterTest(unittest.TestCase):
    """
    Test the full interpreter against a known input and output
    """
    def test_interpreter(self):
        from io import StringIO
        import sys
        from interpreter import interpreter
        sys.stdout = StringIO()

        expected = 'Start reading in file\nStart lexing program\nStart parsing program\n_____________START RUNNING PROGRAM_____________\ngiven value is odd\nProgram exit value: 0\n_________________PROGRAM ENDED_________________\n'

        arguments = ['tests/test_code.txt', 'even_or_odd', '5']
        with self.assertRaises(SystemExit):
            interpreter.interpreter(arguments)

        output = sys.stdout.getvalue()

        sys.stdout = sys.__stdout__

        self.assertEqual(output, expected, 'Interpreter output was not as expected')


if __name__ == '__main__':
    unittest.main()