from decoder.parser import Node, Value, Operator, Call, Unary, IncDec, TypeAssignment, Assignment, Compare, Forloop, While, If, FunctionNode
from decoder.lexer import Token
from decoder.enums import TokensTypes, ErrorType
from decoder.utils import Error
from typing import List, Tuple, Optional, Union, Dict


def get_identifier_as_literal_token(token: Token, variables: Dict[str, Tuple[Union[int, str, bool], str]]) -> Tuple[Optional[Token], Error]:
    """
    This function takes in an identifier token and a dictionary with all variables that are in scope and returns the
    a literal token (int, bool, string) with the value that the variable contained with the same name as the identifier
    token pointed to.
    :param token: Token; identifier token
    :param variables: Dict[]; dictionary containing variables. Key is variable name, value a tuple with the value and the type
    :return: Token, Error; Token literal with the value, error object
    """
    if token.type == TokensTypes.IDENTIFIER:
        if token.value in variables:
            var = variables[token.value]
            if var[1] == 'int':
                return Token(TokensTypes.INT, str(var[0]), token.line_nmr), Error(ErrorType.NO_ERROR, '')
            elif var[1] == 'bool':
                return Token(TokensTypes.BOOL, str(var[0]), token.line_nmr), Error(ErrorType.NO_ERROR, '')
            else:
                return Token(TokensTypes.STRING, var[0], token.line_nmr), Error(ErrorType.NO_ERROR, '')
        else:
            return None, Error(ErrorType.UNKNOW_VARIABLE_ERROR, f'Variable {token.value} was not declared in the scope at line {token.line_nmr}')
    else:
        return None, Error(ErrorType.RUNTIME_ERROR, f'Expected IDENTIFIER, but got {token.type.value} at line {token.line_nmr}')


def bool_token_to_bool(token: Token) -> bool:
    """
    This function gets the boolean value of a token-literal
    :param token: Token; boolean literal token
    :return: bool; boolean value in the token
    """
    if token.value.lower() == 'true':
        return True
    return False


def int_token_to_int(token: Token) -> int:
    """
    This function transforms a token with an integer literal to an integer
    :param token: Token; integer literal token
    :return: int; value inside the token
    """
    try:
        result = int(token.value, 0)
        return result
    except Exception:
        pass
    return 0


def execute_unary(variables: Dict[str, Tuple[Union[int, str, bool], str]], functions: Dict[str, FunctionNode], node: Unary) -> Tuple[Dict[str, Tuple[Union[int, str, bool], str]], Error]:
    """
    Execute a Unary node by getting the value for the right side expression and applying this value to the left side
    given by the unary-operation
    :param variables: Dict[str, Tuple(value, type)]; All variables that are in scope
    :param functions: Dict[str, FunctionNode]; All functions that can be called
    :param node: Unary; Node expressing a unary expression
    :return: Dict, Error; Updated variable dictionary, error object containing any errors that might have happend
    """
    if node.left.type != TokensTypes.IDENTIFIER:
        return variables, Error(ErrorType.RUNTIME_ERROR,
                                f'Unary expression needs a identifier at the left side, but got {node.left.type} at line {node.left.line_nmr}')

    # get right side expression
    right_value, right_value_type, error = execute_expression(variables, functions, node.right, node.left.line_nmr)
    if error.type != ErrorType.NO_ERROR:
        return variables, error

    if node.left.value not in variables:
        return variables, Error(ErrorType.UNKNOW_VARIABLE_ERROR,
                                f'Variable {node.left.value} was not yet declared at line {node.left.line_nmr}')

    left_value, left_type = variables[node.left.value]
    if left_type != right_value_type:
        return variables, Error(ErrorType.RUNTIME_ERROR,
                                f'Unary expression can only be done between the same type, but left is {left_type} and right is {right_value_type}')

    if left_type == 'string':
        if node.operator.value.lower() != 'plusis':
            return variables, Error(ErrorType.RUNTIME_ERROR,
                                    f'Invalid unary operator ({node.operator.value}) between two strings at line {node.operator.line_nmr}')
        left_value += right_value
        variables[node.left.value] = (left_value, left_type)
        return variables, Error(ErrorType.NO_ERROR, '')

    elif left_type == 'int':
        int_function_map = {
            'plusis': lambda left, right: left + right,
            'minis': lambda left, right: left - right,
            'mulis': lambda left, right: left * right,
            'divis': lambda left, right: int(left / right),
            'modis': lambda left, right: left % right,
            'andis': lambda left, right: left & right,
            'oris': lambda left, right: left | right,
            'notis': lambda left, right: ~right,
            'xoris': lambda left, right: left ^ right,
            'bicis': lambda left, right: left & (~right),
            'lshiftis': lambda left, right: left << right,
            'rshiftis': lambda left, right: left >> right,
        }

        if node.operator.value.lower() not in int_function_map:
            return variables, Error(ErrorType.RUNTIME_ERROR,
                                    f'Invalid unary operator ({node.operator.value}) between tow ints on line {node.operator.line_nmr}')

        left_value = int_function_map[node.operator.value.lower()](left_value, right_value)
        variables[node.left.value] = (left_value, left_type)
        return variables, Error(ErrorType.NO_ERROR, '')

    elif left_type == 'bool':
        if node.operator.value.lower() == 'andis':
            left_value = left_value and right_value
            variables[node.left.value] = (left_value, left_type)
            return variables, Error(ErrorType.NO_ERROR, '')
        elif node.operator.value.lower() == 'oris':
            left_value = left_value or right_value
            variables[node.left.value] = (left_value, left_type)
            return variables, Error(ErrorType.NO_ERROR, '')
        else:
            return variables, Error(ErrorType.RUNTIME_ERROR,
                                    f'Invalid unary operation ({node.operator.value}) on two bools at line {node.operator.line_nmr}')

    return variables, Error(ErrorType.RUNTIME_ERROR,
                                f'Unvalid type found at line {node.left.line_nmr}: {left_type}')


def execute_expression(variables: Dict[str, Tuple[Union[int, str, bool], str]], functions: Dict[str, FunctionNode], node: Node, line: int) -> Tuple[Union[int, str, bool], str, Error]:
    """
    This executes a expression node to a value and a type
    :param variables: Dict[str, Tuple(value, type)]; All variables in scope
    :param functions: Dict[str, FunctionNode)]; All callable functions
    :param node: Node; Expression to be executed
    :param line: int; On which line is the expression in the file
    :return: int/str/bool, str, Error; result of the expression, type of the result, Error-object containing any errors.
    """
    if isinstance(node, Value):
        if node.value.type == TokensTypes.IDENTIFIER:
            if node.value.value in variables:
                return variables[node.value.value][0], variables[node.value.value][1], Error(ErrorType.NO_ERROR, '')
            else:
                return 0, 'int', Error(ErrorType.RUNTIME_ERROR, f'Variable {node.value.value} was not yet declared at line {node.value.line_nmr}')
        elif node.value.type == TokensTypes.BOOL:
                return node.value.value.lower() == 'true', 'bool', Error(ErrorType.NO_ERROR, '')
        elif node.value.type == TokensTypes.STRING:
            return node.value.value, 'string', Error(ErrorType.NO_ERROR, '')
        elif node.value.type == TokensTypes.INT:
            return int(node.value.value, 0), 'int', Error(ErrorType.NO_ERROR, '')
        else:
            return 0, 'int', Error(ErrorType.RUNTIME_ERROR, f'Literal couldn\'t be resolved. Gotten type: {node.value.type.value} with value {node.value.value}')

    elif isinstance(node, Operator):
        left = node.left
        right = node.right
        if node.left.type == TokensTypes.IDENTIFIER:
            left, error = get_identifier_as_literal_token(node.left, variables)
            if error.type != ErrorType.NO_ERROR:
                return 0, 'int', error
        if node.right.type == TokensTypes.IDENTIFIER:
            right, error = get_identifier_as_literal_token(node.right, variables)
            if error.type != ErrorType.NO_ERROR:
                return 0, 'int', error

        if left.type == TokensTypes.STRING:
            if right.type == TokensTypes.STRING:
                if node.operator.value.lower() == 'plus':
                    return left.value + right.value, 'string', Error(ErrorType.NO_ERROR, '')
                elif node.operator.value.lower() == 'equals':
                    return left.value == right.value, 'bool', Error(ErrorType.NO_ERROR, '')
                elif node.operator.value.lower() == 'notequals':
                    return left.value != right.value, 'bool', Error(ErrorType.NO_ERROR, '')
                else:
                    return 0, 'int', Error(ErrorType.RUNTIME_ERROR,
                                           f'Invalid operator found: {node.operator.value.lower()} at line {node.operator.line_nmr}')
            else:
                return 0, 'int', Error(ErrorType.RUNTIME_ERROR,
                                       f'At line {left.line_nmr} a operation between a string and not-string is not allowed')
        if left.type == TokensTypes.INT:
            lv = int_token_to_int(left)

            if right.type == TokensTypes.INT:
                rv = int_token_to_int(right)

                int_function_map = {
                    'plus': (lambda left, right: left + right, 'int'),
                    'min': (lambda left, right: left - right, 'int'),
                    'mul': (lambda left, right: left * right, 'int'),
                    'div': (lambda left, right: left / right, 'int'),
                    'mod': (lambda left, right: left % right, 'int'),
                    'and': (lambda left, right: left & right, 'int'),
                    'or': (lambda left, right: left | right, 'int'),
                    'xor': (lambda left, right: left ^ right, 'int'),
                    'bic': (lambda left, right: left & (~right), 'int'),
                    'lshift': (lambda left, right: left << right, 'int'),
                    'rshift': (lambda left, right: left >> right, 'int'),
                    'equals': (lambda left, right: left == right, 'bool'),
                    'lessthan': (lambda left, right: left < right, 'bool'),
                    'greaterthan': (lambda left, right: left > right, 'bool'),
                    'lessthanequals': (lambda left, right: left <= right, 'bool'),
                    'greaterthanequals': (lambda left, right: left >= right, 'bool'),
                    'notequals': (lambda left, right: left != right, 'bool')
                }

                if node.operator.value.lower() not in int_function_map:
                    return 0, 'int', Error(ErrorType.RUNTIME_ERROR,
                                           f'Invalid int operator found: {node.operator.value.lower()} at line {node.operator.line_nmr}')
                if rv == 0 and node.operator.value.lower() == 'div':
                    return 0, 'int', Error(ErrorType.RUNTIME_ERROR, f'Cannot divide by 0 at line {node.operator.line_nmr}')

                operation, type = int_function_map[node.operator.value.lower()]
                return operation(lv, rv), type, Error(ErrorType.NO_ERROR, '')

            else:
                return 0, 'int', Error(ErrorType.RUNTIME_ERROR,
                                       f'At line {left.line_nmr} a operation between a int not-int is not allowed')

        if left.type == TokensTypes.BOOL:
            if right.type == TokensTypes.BOOL:
                if node.operator.value.lower() == 'equals':
                    return left.value.lower() == right.value.lower(), 'bool', Error(ErrorType.NO_ERROR, '')
                elif node.operator.value.lower() == 'notequals':
                    return left.value.lower() != right.value.lower(), 'bool', Error(ErrorType.NO_ERROR, '')
                elif node.operator.value.lower() == 'and':
                    return bool_token_to_bool(left) and bool_token_to_bool(right), 'bool', Error(ErrorType.NO_ERROR, '')
                elif node.operator.value.lower() == 'or':
                    return bool_token_to_bool(left) or bool_token_to_bool(right), 'bool', Error(ErrorType.NO_ERROR, '')
                else:
                    return 0, 'int', Error(ErrorType.RUNTIME_ERROR, f'Invalid bool operator found: {node.operator.value.lower()} at line {node.operator.line_nmr}')
            else:
                return 0, 'int', Error(ErrorType.RUNTIME_ERROR, f'At line {left.line_nmr} a operation between a bool and a not bool is not allowed')

    elif isinstance(node, Compare):
        left = node.left
        right = node.right

        if node.left.type == TokensTypes.IDENTIFIER:
            left, error = get_identifier_as_literal_token(node.left, variables)
            if error.type != ErrorType.NO_ERROR:
                return 0, 'int', error

        if node.right.type == TokensTypes.IDENTIFIER:
            right, error = get_identifier_as_literal_token(node.right, variables)
            if error.type != ErrorType.NO_ERROR:
                return 0, 'int', error

        if left.type != right.type:
            return 0, 'int', Error(ErrorType.RUNTIME_ERROR, f'Can\'t compare between different types (left: {left.type}, right: {right.type}) at line {node.operator.line_nmr}')

        if node.operator.value.lower() == 'equals':
            if left.type == TokensTypes.INT:
                return int_token_to_int(left) == int_token_to_int(right), 'bool', Error(ErrorType.NO_ERROR, '')
            elif left.type == TokensTypes.BOOL:
                return bool_token_to_bool(left) == bool_token_to_bool(right), 'bool', Error(ErrorType.NO_ERROR, '')
            elif left.type == TokensTypes.STRING:
                return left.value == right.value, 'bool', Error(ErrorType.NO_ERROR, '')
            else:
                return 0, 'int', Error(ErrorType.RUNTIME_ERROR, f'Invalid type ({left.type}) found for equals operation at line {left.line_nmr}')
        elif node.operator.value.lower() == 'notequals':
            if left.type == TokensTypes.INT:
                return int_token_to_int(left) != int_token_to_int(right), 'bool', Error(ErrorType.NO_ERROR, '')
            elif left.type == TokensTypes.BOOL:
                return bool_token_to_bool(left) != bool_token_to_bool(right), 'bool', Error(ErrorType.NO_ERROR, '')
            elif left.type == TokensTypes.STRING:
                return left.value != right.value, 'bool', Error(ErrorType.NO_ERROR, '')
            else:
                return 0, 'int', Error(ErrorType.RUNTIME_ERROR, f'Invalid type ({left.type}) found for notequals operation at line {left.line_nmr}')
        elif node.operator.value.lower() == 'lessthan':
            if left.type == TokensTypes.INT:
                return int_token_to_int(left) < int_token_to_int(right), 'bool', Error(ErrorType.NO_ERROR, '')
            else:
                return 0, 'int', Error(ErrorType.RUNTIME_ERROR, f'Invalid type ({left.type}) found for lessthan operation at line {left.line_nmr}')
        elif node.operator.value.lower() == 'greaterthan':
            if left.type == TokensTypes.INT:
                return int_token_to_int(left) > int_token_to_int(right), 'bool', Error(ErrorType.NO_ERROR, '')
            else:
                return 0, 'int', Error(ErrorType.RUNTIME_ERROR, f'Invalid type ({left.type}) found for greaterthan operation at line {left.line_nmr}')
        elif node.operator.value.lower() == 'lessthanequals':
            if left.type == TokensTypes.INT:
                return int_token_to_int(left) <= int_token_to_int(right), 'bool', Error(ErrorType.NO_ERROR, '')
            else:
                return 0, 'int', Error(ErrorType.RUNTIME_ERROR, f'Invalid type ({left.type}) found for lessthanequals operation at line {left.line_nmr}')
            pass
        elif node.operator.value.lower() == 'greaterthanequals':
            if left.type == TokensTypes.INT:
                return int_token_to_int(left) >= int_token_to_int(right), 'bool', Error(ErrorType.NO_ERROR, '')
            else:
                return 0, 'int', Error(ErrorType.RUNTIME_ERROR, f'Invalid type ({left.type}) found for greaterthan operation at line {left.line_nmr}')
        else:
            return 0, 'int', Error(ErrorType.RUNTIME_ERROR, f'Invalid compare operator ({node.operator.value}) found at line {node.operator.line_nmr}')

    elif isinstance(node, Call):
        if node.function.value in functions:
            parameters = map(lambda p: execute_expression(variables, functions, Value(p), p.line_nmr)[0], node.parameters)
            value, error = execute_function_node(functions[node.function.value], list(parameters), functions, node.function.line_nmr)
            if error.type != ErrorType.NO_ERROR:
                return 0, 'string', error
            if value is None:
                value = 0
            result = 0
            if functions[node.function.value].return_type.value == 'string':
                result = value.value.value
            elif functions[node.function.value].return_type.value == 'int':
                result = int(value.value.value, 0)
            elif functions[node.function.value].return_type.value == 'bool':
                if value.value.value.lower() == 'true':
                    result = True
                elif value.value.value.lower() == 'false':
                    result = False
                else:
                    result = bool(value.value.value)
            return result, functions[node.function.value].return_type.value, Error(ErrorType.NO_ERROR, '')
        return 0, 'int', Error(ErrorType.RUNTIME_ERROR, f'Unknow function call to {node.function.value} at line {node.function.line_nmr}')
    else:
        return 0, 'int', Error(ErrorType.RUNTIME_ERROR, f'Tried to execute invalid expression node. Given node type: {node.__class__.__name__} at line { line }')


def execute_whileloop(variables, functions: Dict[str, FunctionNode], expression: Node, body: List[Node], call_line: int) -> Tuple[Dict[str, Tuple[Union[int, str, bool], str]], Error]:
    """
    This executes a while loop as long as the while-expression is true
    :param variables: Dict[str, Tuple[value, type]]; All variables in scope
    :param functions: Dict[str, FunctionNode]; all callable functions
    :param expression: Node; expression that is gives if the while loop should still run
    :param body: List[Node]; List of nodes that form the body of the whileloop
    :param call_line: int, On which line is the while-loop called
    :return: Dict[str, Tuple[value, type]]; Updated variables, error-object containing any errors.
    """
    still_true = execute_expression(variables, functions, expression, call_line)
    if still_true[2].type != ErrorType.NO_ERROR:
        return variables, still_true[2]
    if still_true[1] == 'bool' or still_true[1] == 'int':
        if still_true[0]:
            variables, error = execute_nodes(variables, functions, body)
            if error.type != ErrorType.NO_ERROR:
                return variables, error
            return execute_whileloop(variables, functions, expression, body, call_line)
        return variables, Error(ErrorType.NO_ERROR, '')
    else:
        return variables, Error(ErrorType.RUNTIME_ERROR, f'While expression resulted in type "{still_true[1]}" at line {call_line}. Valid types are only int and boool.')


def execute_forloop(variables: Dict[str, Tuple[Union[int, str, bool], str]], functions: Dict[str, FunctionNode], assignment: Optional[TypeAssignment], dowhile: Compare, inc: Node, body: List[Node]) -> Tuple[Dict[str, Tuple[Union[int, str, bool], str]], Error]:
    """
    This function executes a forloop
    :param variables: Dict[str, Tuple[value, type]]; All variables in scope
    :param functions: Dict[str, FunctionNode]; All functions that can be called
    :param assignment: TypeAssignment; With what assignment should the forloop start
    :param dowhile: Compare; Expression that indicates how many times the forloop should run for
    :param inc: Node; How should the data change between iterations
    :param body: List[Node]; List of nodes to execute as the body
    :return: Dict[str, Tuple[value, type]], Error; Updated variables, Error object
    """
    if assignment is not None:
        value, expr_type, error = execute_expression(variables, functions, assignment.expression, assignment.type.line_nmr)
        if error.type != ErrorType.NO_ERROR:
            return variables, error
        if assignment.id.value in variables:
            return variables, Error(ErrorType.RUNTIME_ERROR, f'Variable {assignment.id} already exists and cannot be redefined at line {assignment.id.line_nmr}')
        if expr_type != assignment.type.value.lower():
            return variables, Error(ErrorType.RUNTIME_ERROR, f'Mismatched type assignment. Variable {assignment.id} expected type {assignment.type.value} but the expression gave {expr_type}')
        variables[assignment.id.value] = value, expr_type
    else:
        if isinstance(inc, Unary):
            variables, error = execute_unary(variables, functions, inc)
            if error.type != ErrorType.NO_ERROR:
                return variables, error
        elif isinstance(inc, IncDec):
            if inc.left.value in variables:
                value, vtype = variables[inc.left.value]
                if vtype == 'int':
                    if inc.operator.value.lower() == 'plusplus':
                        value += 1
                    else:
                        value -= 1
                    variables[inc.left.value] = (value, vtype)
                else:
                    return variables, Error(ErrorType.RUNTIME_ERROR,
                                            f'Variable of type {vtype} can not be incremented or decremented at line {inc.left.line_nmr}')
            else:
                return variables, Error(ErrorType.UNKNOW_VARIABLE_ERROR,
                                        f'Variable {inc.left.value} was not yet declared at line {inc.left.line_nmr}')
        else:
            return variables, Error(ErrorType.RUNTIME_ERROR, f'Invalid with operation in forloop at line {dowhile.left.line_nmr}, only unary operations, incrementing and decrementing is allowed')

    dwr = execute_expression(variables, functions, dowhile, dowhile.left.line_nmr)
    if dwr[2].type != ErrorType.NO_ERROR:
        return variables, dwr[2]
    if dwr[0]:
        variables, error = execute_nodes(variables, functions, body)
        if error.type != ErrorType.NO_ERROR:
            return variables, error
        return execute_forloop(variables, functions, None, dowhile, inc, body)

    return variables, Error(ErrorType.NO_ERROR, '')


def execute_nodes(variables: Dict[str, Tuple[Union[int, str, bool], str]], functions: Dict[str, FunctionNode], nodes: List[Node]) -> Tuple[Dict[str, Tuple[Union[int, str, bool], str]], Error]:
    """
    Execute a list of nodes
    :param variables: Dict[str, Tuple[value, type]]; Variables in scope of the nodes
    :param functions: Dict[str, FunctionNode]; All callable functions
    :param nodes: List[Nodes]; List of nodes to execute
    :return: Dict[str, Tuple[value, type]], Error; Updated variables, Error object containing errors
    """
    if len(nodes) == 0: return variables, Error(ErrorType.NO_ERROR, '')

    node = nodes[0]
    if isinstance(node, TypeAssignment):
        value, vtype, error = execute_expression(variables, functions, node.expression, node.type.line_nmr)
        if error.type != ErrorType.NO_ERROR:
            return variables, error
        variables[node.id.value] = value, vtype
    elif isinstance(node, Assignment):
        if node.id.value not in variables:
            return variables, Error(ErrorType.UNKNOW_VARIABLE_ERROR, f'Variable {node.id.value} was not yet declared at line {node.id.line_nmr}')
        value, vtype, error = execute_expression(variables, functions, node.expression, node.id.line_nmr)
        if error.type != ErrorType.NO_ERROR:
            return variables, error
        if vtype != variables[node.id.value][1]:
            return variables, Error(ErrorType.RUNTIME_ERROR, f'Variable has type {variables[node.id.value][1]}, but expression gave {vtype} at line {node.id.line_nmr}')
        variables[node.id.value] = value, vtype
    elif isinstance(node, IncDec):
        if node.left.value in variables:
            value, vtype = variables[node.left.value]
            if vtype == 'int':
                if node.operator.value.lower() == 'plusplus':
                    value += 1
                else:
                    value -= 1
                variables[node.left.value] = (value, vtype)
            else:
                return variables, Error(ErrorType.RUNTIME_ERROR, f'Variable of type {vtype} can not be incremented or decremented at line {node.left.line_nmr}')
        else:
            return variables, Error(ErrorType.UNKNOW_VARIABLE_ERROR,
                                    f'Variable {node.left.value} was not yet declared at line {node.left.line_nmr}')
    elif isinstance(node, Unary):
        x = execute_unary(variables, functions, node)
        variables, error = x
        if error.type != ErrorType.NO_ERROR:
            return variables, error
    elif isinstance(node, Call):
        if node.function.value in functions:
            parameters = map(lambda p: execute_expression(variables, functions, Value(p), p.line_nmr)[0], node.parameters)
            _, error = execute_function_node(functions[node.function.value], list(parameters), functions, node.function.line_nmr)
            if error.type != ErrorType.NO_ERROR:
                return variables, error
        else:
            return variables, Error(ErrorType.RUNTIME_ERROR, f'Unknow function call to {node.function.value} at line {node.function.line_nmr}')
    elif isinstance(node, Forloop):
        variables, error = execute_forloop(variables, functions, node.start, node.dowhile, node.inc, node.body)
        if error.type != ErrorType.NO_ERROR:
            return variables, error
    elif isinstance(node, While):
        line = -1
        if isinstance(node.dowhile, Compare):
            line = node.dowhile.left.value
        elif isinstance(node.dowhile, Value):
            line = node.dowhile.value.line_nmr
        elif isinstance(node.dowhile, Operator):
            line = node.dowhile.left.line_nmr
        elif isinstance(node.dowhile, Call):
            line = node.dowhile.function.line_nmr
        else:
            return variables, Error(ErrorType.RUNTIME_ERROR, f'Invalid expression for while loop, line unknow')
        variables, error = execute_whileloop(variables, functions, node.dowhile, node.body, line)
        if error.type != ErrorType.NO_ERROR:
            return variables, error
    elif isinstance(node, If):
        if execute_expression(variables, functions, node.cmp, node.cmp.left.line_nmr)[0]:
            variables, error = execute_nodes(variables, functions, node.body)
        else:
            variables, error = execute_nodes(variables, functions, node.else_body)
        if error.type != ErrorType.NO_ERROR:
            return variables, error
    else:
        return variables, Error(ErrorType.RUNTIME_ERROR, f'Couldn\'t execute node with type {node.__class__.__name__}; Node: {node}')

    return execute_nodes(variables, functions, nodes[1:])


def execute_function_node(function: FunctionNode, parameters: List[Union[int, str, bool]], functions: Dict[str, FunctionNode], call_line: int) -> Tuple[Optional[Value], Error]:
    if function.name == 'print':
        if len(parameters) == 1:
            if isinstance(parameters[0], str):
                print(parameters[0].replace('\\n', '\n')[1:-1])
            else:
                print(parameters[0])
            return Value(Token(TokensTypes.INT, '0', 0)), Error(ErrorType.NO_ERROR, f'')
        return None, Error(ErrorType.PARAMETER_ERROR, f'Print function only takes 1 parameter, not {len(parameters)}')

    if function.name == 'size':
        if len(parameters) == 1:
            if isinstance(parameters[0], str):
                return Value(Token(TokensTypes.INT, str(len(parameters[0].strip('"'))), 0)), Error(ErrorType.NO_ERROR, f'')
            return None, Error(ErrorType.PARAMETER_ERROR, f'Size function only takes a string as parameter, not { "int" if isinstance(parameters[0], int) else "bool" }')
        return None, Error(ErrorType.PARAMETER_ERROR, f'Size function only takes 1 parameter, not {len(parameters)}')

    if function.name == 'input':
        if len(parameters) == 1:
            read_from_console = input(parameters[0].strip('"'))
            return Value(Token(TokensTypes.STRING, f'"{read_from_console}"', 0)), Error(ErrorType.NO_ERROR, f'')
        return None, Error(ErrorType.PARAMETER_ERROR, f'Print function only takes 1 parameter, not {len(parameters)}')

    if len(parameters) != len(function.parameters):
        return None, Error(ErrorType.PARAMETER_ERROR, f'Function call with mis matched parameter amount at line {call_line}')

    variables = dict()
    matched_parameters = zip(function.parameters, parameters)
    for mp in matched_parameters:
        given_type = ''
        if isinstance(mp[1], bool):
            given_type = 'bool'
        elif isinstance(mp[1], int):
            given_type = 'int'
        elif isinstance(mp[1], str):
            given_type = 'string'

        if mp[0].type.value.lower() == given_type:
            variables[mp[0].name] = (mp[1], given_type)
        else:
            return None, Error(ErrorType.PARAMETER_ERROR, f'Parameter type mismatch in function call to {function.name} at line {call_line}. Expected {mp[0].type.value} but got {given_type}')

    variables, error = execute_nodes(variables, functions, function.body)

    if error.type != ErrorType.NO_ERROR:
        call_line = f'Error while executing {function.name}. Function called at line: {call_line}\n'
        error.message = call_line + error.message
        return None, error

    if function.return_statement:
        value, return_type, error = execute_expression(variables, functions, function.return_statement, function.return_line)

        if error.type != ErrorType.NO_ERROR:
            return None, error

        if return_type != function.return_type.value:
            return None, Error(ErrorType.RUNTIME_ERROR, f'Function {function.name} called at line {call_line} did not return the defined type. Expected {function.return_type.value} but got {return_type}')

        if return_type == 'string':
            token = Token(TokensTypes.STRING, value, function.return_line)
        elif return_type == 'bool':
            token = Token(TokensTypes.BOOL, str(value), function.return_line)
        elif return_type == 'int':
            token = Token(TokensTypes.INT, str(value), function.return_line)
        else:
            return None, Error(ErrorType.RUNTIME_ERROR,
                               f'Invalid return type ({return_type}) after function at line {function.return_line}')

        return Value(token), Error(ErrorType.NO_ERROR, '')

    return None, Error(ErrorType.RUNTIME_ERROR, f'Expected return statement after function at line {function.return_line}')
