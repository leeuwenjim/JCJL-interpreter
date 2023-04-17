import unittest
from decoder import lexer, utils, enums


class TestKeywordToToken(unittest.TestCase):
    """
    Test the decoder.lexer.value_to_token function
    """
    def test_valid_keyword(self):
        """
        Test if the value_to_token can create a valid Token from a keyword
        """
        token = lexer.value_to_token(enums.keywords, 'plusplus', 2)
        expected = lexer.Token(enums.TokensTypes.INCDEC, 'plusplus', 2)
        self.assertEqual(
            token,
            expected,
            "Incorrect keyword token generated"
        )

    def test_invalid_keyword(self):
        """
        Test if the value_to_token returns None if the the given value is not a keyword
        """
        token = lexer.value_to_token(enums.keywords, 'var1', 0)
        self.assertEqual(token,
                         None,
                         "var1 is not a keyword and no token should be given"
                         )


class TestStringLiteral(unittest.TestCase):
    """
    Test the decoder.lexer.check_if_string_literal function
    """
    def test_valid_string_literal(self):
        """
        Test check_if_string_literal against a valid string literal
        """
        string_literal = '"Valid_string"'
        line_nmr = 3
        token = lexer.check_if_string_literal(string_literal, line_nmr)
        expected = lexer.Token(enums.TokensTypes.STRING, string_literal, line_nmr)
        self.assertEqual(
            token,
            expected,
            "String literal was not detected"
        )

    def test_full_invalid_string_literal(self):
        """
        Test check_if_string_literal against a invalid string literal
        """
        string_literal = 'Invalid_string'
        line_nmr = 3
        token = lexer.check_if_string_literal(string_literal, line_nmr)
        self.assertEqual(token,
                         None,
                         'String literal detected when a full invalid string literal was given'
                         )

    def test_start_invalid_string_literal(self):
        """
        Test check_if_string_literal against a string literal with an invalid start
        """
        string_literal = 'Invalid_string"'
        line_nmr = 3
        token = lexer.check_if_string_literal(string_literal, line_nmr)
        self.assertEqual(token,
                         None,
                         'String literal detected with a string literal with an invalid start'
                         )

    def test_end_invalid_string_literal(self):
        """
        Test check_if_string_literal against a string literal with an invalid end
        """
        string_literal = '"Invalid_string'
        line_nmr = 3
        token = lexer.check_if_string_literal(string_literal, line_nmr)
        self.assertEqual(token,
                         None,
                         'String literal detected with a string literal with an invalid end'
                         )


class TestIntLiteral(unittest.TestCase):
    """
    Test the decoder.lexer.check_if_int_literal function
    """
    def test_valid_decimal_int(self):
        """
        Test if a valid decimal value is seen as a decimal
        """
        int_literal = '123'
        line_nmr = 4
        token = lexer.check_if_int_literal(int_literal, line_nmr)
        expected = lexer.Token(enums.TokensTypes.INT, int_literal, line_nmr)
        self.assertEqual(token,
                         expected,
                         "Positive decimal int literal was not detected")

    def test_valid_negative_decimal_int(self):
        """
        Test if a valid negative decimal value is seen as a decimal
        """
        int_literal = '-123'
        line_nmr = 4
        token = lexer.check_if_int_literal(int_literal, line_nmr)
        expected = lexer.Token(enums.TokensTypes.INT, int_literal, line_nmr)
        self.assertEqual(
            token,
            expected,
            "Negative decimal in literal was not detected"
        )

    def test_invalid_int_literal(self):
        """
        Test if a invalid decimal value is seen as a decimal
        """
        int_literal = '-1a23'
        line_nmr = 4
        token = lexer.check_if_int_literal(int_literal, line_nmr)
        self.assertEqual(
            token,
            None,
            "Invalid decimal int literal was seen as an integer"
        )

    def test_valid_hex_int(self):
        """
        Test if a valid hexadecimal value is seen as a int, also case-test
        """
        int_literal = '0xffFF'
        line_nmr = 4
        token = lexer.check_if_int_literal(int_literal, line_nmr)
        expected = lexer.Token(enums.TokensTypes.INT, int_literal, line_nmr)
        self.assertEqual(
            token,
            expected,
            "Valid hexadecimal int literal was not detected"
        )

    def test_invalid_short_hex_int(self):
        """
        Test if hexadecimal int has at least one character for the value
        """
        int_literal = '0x'
        line_nmr = 4
        token = lexer.check_if_int_literal(int_literal, line_nmr)
        self.assertEqual(
            token,
            None,
            "To short hexadecimal int literal was seen as an integer"
        )

    def test_invalid_hex_int(self):
        """
        Test if hexadecimal int only consist with chars from 0-9 and a-f
        """
        int_literal = '0x3g1'
        line_nmr = 4
        token = lexer.check_if_int_literal(int_literal, line_nmr)
        self.assertEqual(
            token,
            None,
            "Invalid hexadecimal int literal was seen as an integer"
        )

    def test_invalid_long_hex_int(self):
        """
        Maximum length for a 32-bit hex decimal is 16 characters after 0x. Test if this is detected
        """
        int_literal = '0x0123456789abcdeff'
        line_nmr = 4
        token = lexer.check_if_int_literal(int_literal, line_nmr)
        self.assertEqual(
            token,
            None,
            "To long hexadecimal int literal was seen as an integer"
        )


class TestIdentifier(unittest.TestCase):
    """
    Test the decoder.lexer.check_if_valid_identifier function
    """
    def test_valid_identifier(self):
        """
        Test if a valid identifier can be recognized
        """
        identifier = 'var_Int'
        line_nmr = 5
        token = lexer.check_if_valid_identifier(identifier, line_nmr)
        expected = lexer.Token(enums.TokensTypes.IDENTIFIER, identifier, line_nmr)
        self.assertEqual(
            token,
            expected,
            "Valid identifier was not detected"
        )

    def test_invalid_identifier_with_int_start(self):
        """
        Test if an identifier can not start with a integer
        """
        identifier = '1var_int'
        line_nmr = 5
        token = lexer.check_if_valid_identifier(identifier, line_nmr)
        self.assertEqual(
            token,
            None,
            "Identifier can not start with a integer"
        )

    def test_invalid_identifier_with_uppercase_start(self):
        """
        Test if an identifier can not start with a uppercase character
        """
        identifier = 'Var_int'
        line_nmr = 5
        token = lexer.check_if_valid_identifier(identifier, line_nmr)
        self.assertEqual(
            token,
            None,
            "Identifier can not start with a uppercase character"
        )


class TestWordLexing(unittest.TestCase):
    """
    Test the decoder.lexer.lex_token function
    """
    def test_valid_keyword_word(self):
        """
        Test if a keyword is tokenized correctly
        """
        line_nmr = 9
        word = 'if'
        token = lexer.lex_token(word, line_nmr)
        expected = lexer.Token(enums.TokensTypes.IF, 'if', line_nmr)
        self.assertEqual(
            token,
            expected,
            "Could not tokenize a valid keyword"
        )

    def test_valid_string_literal(self):
        """
        Test if a string literal is tokenized correctly
        """
        line_nmr = 9
        word = '"Test deze literal"'
        token = lexer.lex_token(word, line_nmr)
        expected = lexer.Token(enums.TokensTypes.STRING, word, line_nmr)
        self.assertEqual(
            token,
            expected,
            "Could not tokenize a valid string literal"
        )

    def test_valid_decimal_int_literal(self):
        """
        Test if a decimal integer literal is tokenized correctly
        """
        line_nmr = 9
        word = '-556'
        token = lexer.lex_token(word, line_nmr)
        expected = lexer.Token(enums.TokensTypes.INT, word, line_nmr)
        self.assertEqual(
            token,
            expected,
            "Could not tokenize a valid decimal integer literal"
        )

    def test_valid_hexadecimal_int_literal(self):
        """
        Test if a hexadecimal integer literal is tokenized correctly
        """
        line_nmr = 9
        word = '0xF0F0'
        token = lexer.lex_token(word, line_nmr)
        expected = lexer.Token(enums.TokensTypes.INT, word, line_nmr)
        self.assertEqual(
            token,
            expected,
            "Could not tokenize a valid hexadecimal integer literal"
        )

    def test_valid_identifier(self):
        """
        Test if an identifier is tokenized correctly
        """
        line_nmr = 9
        word = 'var_for_test'
        token = lexer.lex_token(word, line_nmr)
        expected = lexer.Token(enums.TokensTypes.IDENTIFIER, word, line_nmr)
        self.assertEqual(
            token,
            expected,
            "Could not tokenize a valid identifier"
        )

    def test_invalid_word(self):
        """
        Test if an invalid word is tokenized correctly
        """
        line_nmr = 9
        word = 'var-for-test'
        token = lexer.lex_token(word, line_nmr)
        expected = lexer.Token(enums.TokensTypes.ERROR, word, line_nmr)
        self.assertEqual(
            token,
            expected,
            "Invalid word was tokenized incorrectly"
        )


class TestWordListLexer(unittest.TestCase):
    """
    Test the decoder.lexer.lex_splitted_line function
    """
    def test_valid_word_list(self):
        """
        Test if a list with valid words is correctly tokenized
        """
        word_list = ['int', 'var1', 'is', '6']
        line_nmr = 8
        tokens = lexer.lex_splitted_line(word_list, line_nmr)
        expected = [
            lexer.Token(enums.TokensTypes.TYPE, 'int', line_nmr),
            lexer.Token(enums.TokensTypes.IDENTIFIER, 'var1', line_nmr),
            lexer.Token(enums.TokensTypes.ASSIGNMENT, 'is', line_nmr),
            lexer.Token(enums.TokensTypes.INT, '6', line_nmr),
        ]
        self.assertEqual(
            tokens,
            expected,
            'Valid word list could not be correctly tokenized'
        )

    def test_word_list_with_invalid_word(self):
        """
        Test if a list of words with an invalid word is correctly tokenized
        """
        word_list = ['int', 'Var1', 'is', '6']
        line_nmr = 8
        tokens = lexer.lex_splitted_line(word_list, line_nmr)
        expected = [
            lexer.Token(enums.TokensTypes.TYPE, 'int', line_nmr),
            lexer.Token(enums.TokensTypes.ERROR, 'Var1', line_nmr),
            lexer.Token(enums.TokensTypes.ASSIGNMENT, 'is', line_nmr),
            lexer.Token(enums.TokensTypes.INT, '6', line_nmr),
        ]
        self.assertEqual(
            tokens,
            expected,
            'Invalid word list could not be correctly tokenized'
        )


class TestSplitLineToWords(unittest.TestCase):
    """
    Test the decoder.lexer.string_split_by_whitespace_rec
    """
    def test_simple_line(self):
        """
        Test if a line can be splitted on whitespace
        """
        line = 'int var1 is 6'
        splitted = lexer.string_split_by_whitespace_rec(line)
        self.assertEqual(
            splitted,
            ['int', 'var1', 'is', '6'],
            'Line was not splitted correctly'
        )

    def test_line_with_two_string_literals(self):
        """
        Test if a line with two string literals is splitted correctly
        """
        line = 'var1 is "hello world" plus " from JCJL"'
        splitted = lexer.string_split_by_whitespace_rec(line)
        self.assertEqual(
            splitted,
            ['var1', 'is', '"hello world"', 'plus', '" from JCJL"'],
            'Line with 2 string literals could not be splitted'
        )


if __name__ == '__main__':
    unittest.main()
