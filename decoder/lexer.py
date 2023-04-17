import re
from functools import reduce
from typing import List, Tuple, Union, Optional
from decoder.enums import TokensTypes, keywords, escape_chars, ErrorType
from decoder import utils
from decoder.io import jcjlreader
from decoder.utils import Error, status_logger


class Token():
    def __init__(self, type: TokensTypes, value: str, line_nmr: int):
        """
        Initialize a Token object
        :param type: TokenTypes; Type of token
        :param value: str; Value of the token
        :param line_nmr: int; Line number where the token exists
        """
        self.type = type
        self.value = value
        self.line_nmr = line_nmr

    def __str__(self):
        """
        Get the token as a string
        :return: str; Representation of the token
        """
        return f'(Token; Type: {self.type}, value: {self.value}, at line: {str(self.line_nmr)})'

    def __repr__(self):
        """
        Get the reprecentation of the string
        :return: str; Representation of the token
        """
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return self.type == other.type and self.value == other.value and self.line_nmr == other.line_nmr


def value_to_token(keyword_list: List[str], value: str, line_nmr: int) -> Optional[Token]:
    """
    Matches a value to list of keywords, and if found returns the token of the keyword. Otherwise this function
    returns None
    :param keyword_list: List[str]; List of keywords to match to
    :param value: str; value that might be a keyword
    :param line_nmr: int; Line number on which the value is found
    :return: Token | None; if the value is a keyword, the token is returned
    """
    if len(keyword_list) == 0:
        return None
    head, *tail = keyword_list
    if head == value.lower():
        return Token(keywords[head], value, line_nmr)
    return value_to_token(tail, value, line_nmr)


def check_if_string_literal(value: str, line_nmr: int) -> Optional[Token]:
    """
    Check if the given value is a string literal. If it is, a Token-object is returned
    :param value: str, value to be checked
    :param line_nmr: int, line number on which the value is
    :return: Token | None; Returns token if value is a string literal
    """
    if value.startswith('"') and value.endswith('"'):
        return Token(TokensTypes.STRING, value, line_nmr)
    return None


def check_if_int_literal(value: str, line_nmr: int) -> Optional[Token]:
    """
    Checks if the given value is a base-10 or hexadecimal number. If it is, a Token-object is returned
    :param value: str, value to be checked
    :param line_nmr: int; line number on which the value is
    :return: Token | None; Returns token if value is an integer
    """
    hex_regex = r'^0x[0-9a-fA-F]{1,16}$'
    #hex_regex = r'^0x[0-9A-F]{1, 16}$'
    if re.match(hex_regex, value):
        return Token(TokensTypes.INT, value, line_nmr)
    else:
        try:
            converted = int(value)
            return Token(TokensTypes.INT, value, line_nmr)
        except:
            pass
    return None


def check_if_valid_identifier(value: str, line_nmr: int) -> Optional[Token]:
    """
    Checks if the given value is a valid identifier. If it is, a Token-object is returned
    :param value: str, value to be checked
    :param line_nmr: int; line number on which the value is
    :return: Token | None; Returns token if value is an identifier
    """
    identifier_regex = r'^[a-z]([a-zA-Z0-9_]?)*$'
    if re.match(identifier_regex, value):
        return Token(TokensTypes.IDENTIFIER, value, line_nmr)
    return None


def lex_token(word: str, line_nmr: int) -> Token:
    """
    Create a token from a word.
    :param word: str; word to be tokenized
    :param line_nmr: int; line number in which the word is
    :return: Token; The token for the word
    """

    # Check if word is a keyword
    result = value_to_token([*keywords.keys()], word, line_nmr)

    if result is None:
        # Check if word is a string literal, integer or identifier
        functions = [check_if_string_literal, check_if_int_literal, check_if_valid_identifier]
        result = utils.literal_identifier_function_looper(functions, word, line_nmr)

    if result is None:
        # Create error token if word is not a keyword, identifier or literal
        result = Token(TokensTypes.ERROR, word, line_nmr)

    return result


def lex_splitted_line(line: List[str], line_nmr: int) -> List[Token]:
    """
    Turn a list of words to a list of tokens
    :param line: List[str]; list of words
    :param line_nmr: int; line number on which the words are
    :return: List[Token]; List of tokens for the given list of words
    """
    if len(line) == 0:
        return []
    if len(line) == 1:
        return [lex_token(line[0], line_nmr), ]

    head, *tail = line
    return [lex_token(head, line_nmr), ] + lex_splitted_line(tail, line_nmr)


def string_split_by_whitespace_rec(to_split: str, word: str = '', in_string: bool = False) -> List[str]:
    """
    This function splits a string by whitespace. The exception is that expected string literals are kept as a whole.
    :param to_split: str; The string that yet needs to be splitted
    :param word: str; what characters are already collected in a word
    :param in_string: bool; is the current 'to_split' inside an expected string literal
    :return: List[str]; List of splitted words to be tokenized
    """
    if len(to_split) == 0:
        return []
    if len(to_split) == 1:
        word = word + to_split
        word = word.strip()
        if word:
            return [word, ]
        return list()

    head = to_split[0]
    tail = to_split[1:]
    if head.isspace():
        if in_string:
            if word.endswith('"'):
                return [word, ] + string_split_by_whitespace_rec(tail)
        elif not word.startswith('"'):
            return [word, ] + string_split_by_whitespace_rec(tail)
        else:
            in_string = True
    word = word + head
    return string_split_by_whitespace_rec(tail, word, in_string)


def format_syntax_error(value: str, line_nmr: int) -> str:
    """
    This function formats a syntax error
    :param value: str; value that could not be defined
    :param line_nmr: int; line on which the value can be found
    :return: str; formatted error
    """
    return f'On line {str(line_nmr)} the symbol: {value} couldn\'t be defined'


@status_logger('Start lexing program')
def lex_lines(lines: List[Tuple[str, int]]) -> Tuple[List[Token], Error]:
    program = map(lambda x: (string_split_by_whitespace_rec(x[0]), x[1]), lines)
    # remove empty lines
    program = filter(lambda x: len(x) > 0, program)

    # tokenize the lines
    tokenized_lines = map(lambda x: lex_splitted_line(x[0], x[1]), program)

    # put all tokens in a single list
    tokens: List[Token] = reduce(lambda a, b: a + b + [Token(TokensTypes.ENDLINE, '\n', b[0].line_nmr), ],
                                 tokenized_lines, [])

    # check for any error tokens
    error_tokens = list(filter(lambda x: x.type == TokensTypes.ERROR, tokens))

    # If errors are found, format them and return the errors
    if len(error_tokens) > 0:
        formatted_errors = map(lambda x: format_syntax_error(x.value, x.line_nmr), error_tokens)
        errors = reduce(lambda x, y: x + '\n' + y, formatted_errors)
        return tokens, Error(ErrorType.SYNTAX_ERROR, errors)

    # return tokens with no error
    return tokens, Error(ErrorType.NO_ERROR, '')


def lexer(file: str) -> Tuple[List[Token], Error]:
    """
    This function takes in a file path, reads the given file and tokenizes the program in the file
    :param file: str; file path to file
    :return: List[Token], Error; A list with token and an Error object depicting the error or no error
    """
    # read the file
    lines_or_error = jcjlreader.read_program(file)
    if isinstance(lines_or_error, Error):
        return [], lines_or_error

    return lex_lines(lines_or_error)







