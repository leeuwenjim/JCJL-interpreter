from decoder.lexer import lexer, Token
from decoder.parser import parse, Value
from decoder.utils import Error
from decoder.enums import ErrorType
from interpreter.execute import execute_function_node
import sys
from typing import List, Union, Any


def parse_parameters(rawp: List[str]) -> List[Union[int, bool, str]]:
    if len(rawp) == 0:
        return []
    current = rawp[0]
    if rawp[0] == 'true':
        current = True
    elif rawp[0] == 'false':
        current = False
    else:
        try:
            intc = int(rawp[0], 0)
            current = intc
        except:
            pass
    return [current, ] + parse_parameters(rawp[1:])


def interpreter(arguments: List[Any]):
    if len(arguments) < 2:
        print(Error(ErrorType.SYNTAX_ERROR, f'At least file and function name are required, but not given'))
        exit(2)

    tokens, error = lexer(arguments[0])
    if error.type != ErrorType.NO_ERROR:
        print(error)
        exit(3)

    functions, error = parse(tokens)
    if error.type != ErrorType.NO_ERROR:
        print(error)
        exit(4)

    parameters = parse_parameters(arguments[2:])

    print('_____________START RUNNING PROGRAM_____________')
    return_value, error = execute_function_node(functions[arguments[1]], parameters, functions, 0)
    if error.type != ErrorType.NO_ERROR:
        print(error)
        exit(5)

    if return_value is not None and isinstance(return_value, Value):
        # Print exit value
        value = return_value.value
        if isinstance(return_value.value, Token):
            value = return_value.value.value

        print(f'Program exit value: {value}')

    print('_________________PROGRAM ENDED_________________')
    exit(0)
