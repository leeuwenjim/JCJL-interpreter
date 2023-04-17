from enum import Enum


class TokensTypes(Enum):
    TYPE = 'TYPE'
    BOOL = 'BOOL'
    INT = 'INT_LITERAL'
    STRING = 'STRING_LITERAL'
    ASSIGNMENT = 'ASSIGNMENT'
    OPERATOR = 'OPERATOR'
    COMPARE = 'COMPARE'
    UNARY = 'UNARY'
    INCDEC = 'INC_DEC'
    FOR = 'FOR'
    WHILE = 'WHILE'
    WITH = 'WITH'
    ENDFOR = 'ENDFOR'
    ENDWHILE = 'ENDWHILE'
    IF = 'IF'
    ELSE = 'ELSE'
    ENDIF = 'ENDIF'
    FUNCTION = 'FUNCTION'
    RETURN = 'RETURN'
    CALL = 'CALL'
    IDENTIFIER = 'IDENTIFIER'
    ENDLINE = 'END_LINE'
    ERROR = 'ERROR'

    def __str__(self) -> str:
        """
        Get the value of the enum type
        :return: str; value of the enum
        """
        return self.value


identifier_or_literal = [TokensTypes.IDENTIFIER, TokensTypes.BOOL, TokensTypes.STRING, TokensTypes.INT]


keywords = {
    'int': TokensTypes.TYPE,
    'bool': TokensTypes.TYPE,
    'string': TokensTypes.TYPE,
    'true': TokensTypes.BOOL,
    'false': TokensTypes.BOOL,
    'is': TokensTypes.ASSIGNMENT,
    'plus': TokensTypes.OPERATOR,
    'min': TokensTypes.OPERATOR,
    'mul': TokensTypes.OPERATOR,
    'div': TokensTypes.OPERATOR,
    'mod': TokensTypes.OPERATOR,
    'and': TokensTypes.OPERATOR,
    'or': TokensTypes.OPERATOR,
    'xor': TokensTypes.OPERATOR,
    'bic': TokensTypes.OPERATOR,
    'lshift': TokensTypes.OPERATOR,
    'rshift': TokensTypes.OPERATOR,
    'equals': TokensTypes.COMPARE,
    'lessthan': TokensTypes.COMPARE,
    'greaterthan': TokensTypes.COMPARE,
    'lessthanequals': TokensTypes.COMPARE,
    'greaterthanequals': TokensTypes.COMPARE,
    'notequals': TokensTypes.COMPARE,
    'plusis': TokensTypes.UNARY,
    'minis': TokensTypes.UNARY,
    'mulis': TokensTypes.UNARY,
    'divis': TokensTypes.UNARY,
    'modis': TokensTypes.UNARY,
    'andis': TokensTypes.UNARY,
    'oris': TokensTypes.UNARY,
    'notis': TokensTypes.UNARY,
    'xoris': TokensTypes.UNARY,
    'bicis': TokensTypes.UNARY,
    'lshiftis': TokensTypes.UNARY,
    'rshiftis': TokensTypes.UNARY,
    'plusplus': TokensTypes.INCDEC,
    'minmin': TokensTypes.INCDEC,
    'for': TokensTypes.FOR,
    'while': TokensTypes.WHILE,
    'with': TokensTypes.WITH,
    'endfor': TokensTypes.ENDFOR,
    'endwhile': TokensTypes.ENDWHILE,
    'if': TokensTypes.IF,
    'else': TokensTypes.ELSE,
    'endif': TokensTypes.ENDIF,
    'function': TokensTypes.FUNCTION,
    'return': TokensTypes.RETURN,
    'call': TokensTypes.CALL
}

escape_chars = ["'\\\\'", "'\\n'", "'\\t'", "'\\s'", "'\\\''", "'\\\"'"]


class ErrorType(Enum):
    NO_ERROR = 'NO_ERROR'
    FILE_NOT_FOUND_ERROR = 'FILE_NOT_FOUND_ERROR'
    SYNTAX_ERROR = 'SYNTAX_ERROR'
    NO_RETURN_FOUND = 'NO_RETURN_FOUND_ERROR'
    INVALID_NAME_ERROR = 'INVALID_NAME_ERROR'
    UNKNOW_TYPE_ERROR = 'UNKNOW_TYPE_ERROR'
    STATEMENT_ERROR = 'STATEMENT_ERROR'
    PARAMETER_ERROR = 'PARAMETER_ERROR'
    UNKNOW_VARIABLE_ERROR = 'UNKNOW_VARIABLE_ERROR'
    RUNTIME_ERROR = 'RUNTIME_ERROR'

    def __str__(self) -> str:
        """
        Get the value of the enum type
        :return: str; value of the enum
        """
        return self.value
