from decoder.lexer import Token
from decoder.enums import TokensTypes, ErrorType, identifier_or_literal
from typing import List, Tuple, Union, Dict, Optional
from decoder.utils import Error, status_logger
from decoder.nodes import (
    Node,
    Value,
    Operator,
    Call,
    Unary,
    IncDec,
    TypeAssignment,
    Assignment,
    Compare,
    Forloop,
    While,
    If,
    Parameter,
    FunctionNode
)


def check_parameters(tokens: List[Token]) -> Error:
    """
    This function checks if a list of tokens are valid identifiers or literals
    :param tokens: List[Token]; Tokens that must be checked
    :return: Error; Object that indicated if there is an error or not
    """
    if len(tokens) == 0:
        return Error(ErrorType.NO_ERROR, '')
    lower_error = check_parameters(tokens[1:])
    if lower_error.type == ErrorType.NO_ERROR:
        if tokens[0].type in identifier_or_literal:
            return Error(ErrorType.NO_ERROR, '')
        return Error(ErrorType.SYNTAX_ERROR, f'Invalid parameter: {tokens[0].value} at line {tokens[0].line_nmr}')
    return lower_error


def get_parameter_list(tokens: List[Token]) -> Tuple[List[Parameter], List[Token], Error]:
    """
    This functions gets a list of parameters for a function definition.
    Any errors will be given through the error-object
    :param tokens: Tokens that must be parsed
    :return: List[Parameter], List[Token], Error; Parameter list, left over tokens and an error-object
    """
    if tokens[0].type == TokensTypes.ENDLINE:
        return [], tokens[1:], Error(ErrorType.NO_ERROR, '')
    if tokens[0].type == TokensTypes.TYPE:
        if tokens[1].type == TokensTypes.IDENTIFIER:
            next_parameters, left_over, error = get_parameter_list(tokens[2:])
            return [Parameter(type=tokens[0], name=tokens[1].value), ] + next_parameters, left_over, error
        else:
            return [], tokens[1:], Error(ErrorType.UNKNOW_TYPE_ERROR, f'Name \'{tokens[1].value}\' at line {str(tokens[1].line_nmr)} is not a valid name')
    else:
        return [], tokens[1:], Error(ErrorType.UNKNOW_TYPE_ERROR, f'Type \'{tokens[0].value}\' at line {str(tokens[0].line_nmr)} is not valid')


def find_until(tokens: List[Token], until: TokensTypes) -> Tuple[List[Token], List[Token]]:
    """
    This function will get all tokens until a given type. The token that is search for will no be in the
    found tokens or the left-over (basically omitted)
    :param tokens: List[Token]; List in which must be searched
    :param until: TokensTypes; Type of token for which must be searched
    :return: List[Token], List[Token]; List of tokens before and a list of tokens after the search-type
    """
    if len(tokens) > 0:
        head, *tail = tokens
        if head.type == until:
            return [], tail
        found, left_over = find_until(tail, until)
        return [head, ] + found, left_over
    return tokens, []


def find_end(tokens: List[Token], start_type: TokensTypes, end_type: TokensTypes, inner_start: int = 0, inner_end: int = 0) -> Tuple[List[Token], List[Token]]:
    """
    This function finds the body of a statement (for-loop, whileloop, etc)
    The end-token will not be returned in the body or leftover tokens. This function
    can handle nested statements
    :param tokens: List[Token]; Tokens in which must be searched
    :param start_type: TokensType; What is the start-type of the statement
    :param end_type: TokensType; What is the endtype of the statement
    :param inner_start: int; How many times has the start-type been found
    :param inner_end: int; How many times has the end-type been found
    :return: List[Token], List[Token]; List of tokens inside the body and List of tokens that are after the body
    """
    if len(tokens) == 0:
        return [], []
    if len(tokens) == 1:
        head = tokens[0]
        tail = []
    else:
        head, *tail = tokens
    if head.type == start_type:
        body, left_over = find_end(tail, start_type, end_type, inner_start + 1, inner_end)
        return [head, ] + body, left_over
    if head.type == end_type:
        if inner_start == inner_end:
            return [], tail
        body, left_over = find_end(tail, start_type, end_type, inner_start, inner_end + 1)
        return [head, ] + body, left_over
    body, left_over = find_end(tail, start_type, end_type, inner_start, inner_end)
    return [head, ] + body, left_over


def find_if_else_bodies(tokens: List[Token], inner_start: int = 0, inner_end: int = 0) -> Tuple[List[Token], List[Token]]:
    """
    This function slits a list of tokens that are part of an if-statement in the if-body and else-body
    :param tokens: List[Token]; List of tokens that are part of the if-statement
    :param inner_start: int; How many times is the if-token type found
    :param inner_end: int; How many times is the endif-token type found
    :return: List[Token], List[Token]; List of token for the if-body and a List of token for the else body
    """
    if len(tokens) == 0:
        return [], []
    head, *tail = tokens
    if head.type == TokensTypes.IF:
        if_body, else_body = find_if_else_bodies(tail, inner_start + 1, inner_end)
        return [head, ] + if_body, else_body
    if head.type == TokensTypes.ENDIF:
        if_body, else_body = find_if_else_bodies(tail, inner_start, inner_end + 1)
        return [head, ] + if_body, else_body
    if head.type == TokensTypes.ELSE:
        if inner_start == inner_end:
            if tail[0].type == TokensTypes.ENDLINE:
                tail = tail[1:]
            return [], tail
        if_body, else_body = find_if_else_bodies(tail, inner_start, inner_end)
        return [head, ] + if_body, else_body
    if_body, else_body = find_if_else_bodies(tail, inner_start, inner_end)
    return [head, ] + if_body, else_body



def get_expression(tokens: List[Token]) -> Tuple[Union[Node, None], Error]:
    """
    This function parses one or more tokens to an expression. If an error is generated, the given node is None
    :param tokens: List[Token]; list of tokens that form an expression
    :return: Node, Error; Node that contains an expression and an error-object
    """
    if len(tokens) == 0:
        # No expression can be formed from 0 tokens
        return None, Error(ErrorType.STATEMENT_ERROR, f'No expression found. Cant find line number')

    elif len(tokens) == 1:
        # Token must be and identifier or literal
        if tokens[0].type in identifier_or_literal:
            return Value(tokens[0]), Error(ErrorType.NO_ERROR, '')
        else:
            return None, Error(ErrorType.STATEMENT_ERROR, f'"{tokens[0].value}" at line {tokens[0].line_nmr} is no identifier or literal as expected.')

    # Check if the expression is an function call
    elif tokens[0].type == TokensTypes.CALL:
        # Check if the function name is given
        if tokens[1].type == TokensTypes.IDENTIFIER:
            # check the parameters
            parameter_tokens = tokens[2:]
            parameter_error = check_parameters(parameter_tokens)
            if parameter_error.type != ErrorType.NO_ERROR:
                return None, parameter_error
            call = Call(tokens[1], parameter_tokens)
            return call, Error(ErrorType.NO_ERROR, '')
        else:
            # No function name found
            return None, Error(ErrorType.SYNTAX_ERROR, f'Expected function name at line {tokens[1].line_nmr} but got {tokens[1].value}')

    elif len(tokens) == 2:
        # Two tokens can only be increment or decrement, or not-operation
        if tokens[0].type is TokensTypes.IDENTIFIER:
            if tokens[1].type is TokensTypes.INCDEC:
                return IncDec(tokens[0], tokens[1]), Error(ErrorType.NO_ERROR, '')
            return None, Error(ErrorType.SYNTAX_ERROR, f'Invalid operater. Expected increment or decrement but got {tokens[1].value} at line {tokens[1].line_nmr}')
        elif tokens[0].value is 'not':
            pass
        return None, Error(ErrorType.SYNTAX_ERROR, f'Expected identifier at line {tokens[0].line_nmr} but got {tokens[0].value}')

    elif len(tokens) == 3:
        # With 3 token an operation or compare is the option.

        # Guard clauses to check the type of the tokens
        if tokens[0].type not in identifier_or_literal:
            return None, Error(ErrorType.SYNTAX_ERROR, f'Invalid token: {tokens[0].value} at line {tokens[0].line_nmr}')
        if tokens[1].type not in {TokensTypes.OPERATOR, TokensTypes.UNARY, TokensTypes.COMPARE}:
            return None, Error(ErrorType.SYNTAX_ERROR, f'Invalid operator: {tokens[1].value} at line {tokens[1].line_nmr}')
        if tokens[2].type not in identifier_or_literal:
            return None, Error(ErrorType.SYNTAX_ERROR, f'Invalid token: {tokens[2].value} at line {tokens[2].line_nmr}')

        # Format the correct Node-type
        if tokens[1].type == TokensTypes.COMPARE:
            return Compare(tokens[0], tokens[1], tokens[2]), Error(ErrorType.NO_ERROR, '')
        elif tokens[1].type == TokensTypes.UNARY:
            if tokens[0].type != TokensTypes.IDENTIFIER:
                return None, Error(ErrorType.SYNTAX_ERROR, f'Expected identifier for lefthand of unary, but got {tokens[0].value} at line {tokens[0].line_nmr}')
            return Unary(tokens[0], tokens[1], Value(tokens[2])), Error(ErrorType.NO_ERROR, '')
        else:
            return Operator(tokens[0], tokens[1], tokens[2]), Error(ErrorType.NO_ERROR, '')

    return None, Error(ErrorType.SYNTAX_ERROR, f'Invalid expression at line {tokens[0].line_nmr}')


def get_type_assignment(tokens: List[Token]) -> Tuple[Union[TypeAssignment, None], Error]:
    """
    Parse a type assignment from tokens. If an error is generated, the given node will be None
    :param tokens: List[Token]; Tokens that form the type assignment
    :return: TypeAssignment, Error; Node with the type assignment and an error-object
    """
    if tokens[0].type != TokensTypes.TYPE:
        return None, Error(ErrorType.STATEMENT_ERROR, f'Expected type at line {tokens[0].line_nmr} instead of {tokens[0].value}')

    if tokens[1].type != TokensTypes.IDENTIFIER:
        return None, Error(ErrorType.STATEMENT_ERROR,
                           f'Expected identifier at line {tokens[1].line_nmr} instead of {tokens[1].value}')

    if tokens[2].type != TokensTypes.ASSIGNMENT:
        return None, Error(ErrorType.STATEMENT_ERROR,
                           f'Expected \'is\' instead of {tokens[2].value} at line {tokens[2].line_nmr}')

    expression, error = get_expression(tokens[3:])
    if error.type == ErrorType.NO_ERROR:
        return TypeAssignment(tokens[0], tokens[1], expression), Error(ErrorType.NO_ERROR, '')
    return None, error


def get_compare(tokens: List[Token]) -> Tuple[Union[Compare, None], Error]:
    """
    Parse a compare node from tokens. If an error occures, the node will be None
    :param tokens: List[Token]; Tokens that form an compare statement
    :return: Compare, Error; compare node and an error-object
    """
    if len(tokens) != 3:
        return None, Error(ErrorType.STATEMENT_ERROR, f'Couldn\'t form a compare at line {tokens[0].line_nmr}')

    if tokens[1].type != TokensTypes.COMPARE:
        return None, Error(ErrorType.STATEMENT_ERROR, f'{tokens[1].value} is not a valid compare operator')

    if tokens[0].type not in identifier_or_literal:
        return None, Error(ErrorType.STATEMENT_ERROR,
                           f'Compare left hand side is not an variable or literal at line {tokens[0].line_nmr}')

    if tokens[2].type not in identifier_or_literal:
        return None, Error(ErrorType.STATEMENT_ERROR,
                           f'Compare right hand side is not an variable or literal at line {tokens[2].line_nmr}')

    return Compare(tokens[0], tokens[1], tokens[2]), Error(ErrorType.NO_ERROR, '')


def parse_for_loop(tokens: List[Token]) -> Tuple[Optional[Node], List[Token], Error]:
    """
    Parse tokens to a forloop-node and left-over tokens. When an error occures, the returned node and left-over tokens
    will be None and an empty list.
    :param tokens: List[Token]; Tokens that form a for loop with optional extra tokens after the forloop
    :return: Forloop, List[Token], Error; Node with the forloop, left over token, error-object
    """
    start, left_over = find_until(tokens[1:], TokensTypes.WHILE)
    dowhile, left_over = find_until(left_over, TokensTypes.WITH)
    with_tokens, left_over = find_until(left_over, TokensTypes.ENDLINE)
    for_body, left_over = find_end(left_over, TokensTypes.FOR, TokensTypes.ENDFOR)

    start_node, error = get_type_assignment(start)
    if start_node is None:
        return None, left_over, Error(ErrorType.STATEMENT_ERROR,
                         f'For loop doesn\'t start with an assignment (type identifier is expression) at line {tokens[0].line_nmr}')
    if error.type != ErrorType.NO_ERROR:
        return None, [], error

    dowhile_node, error = get_compare(dowhile)
    if dowhile_node is None:
        return None, left_over, Error(ErrorType.STATEMENT_ERROR,
                         f'For loop doesn\'t have a valid compare (x compare y) at line {tokens[0].line_nmr}')
    if error.type != ErrorType.NO_ERROR:
        return None, left_over, error

    with_node, error = get_expression(with_tokens)
    if with_node is None:
        return None, left_over, Error(ErrorType.STATEMENT_ERROR,
                         f'For loop doesn\'t have a valid itteration expression at line {tokens[0].line_nmr}')
    if error.type != ErrorType.NO_ERROR:
        return None, left_over, error

    for_node = Forloop(start_node, dowhile_node, with_node)
    body_nodes, error = get_nodes(for_body)
    if error.type != ErrorType.NO_ERROR:
        return None, [], error

    for_node.body = body_nodes
    return for_node, left_over, Error(ErrorType.NO_ERROR, '')


def parse_while_loop(tokens: List[Token]) -> Tuple[Optional[Node], List[Token], Error]:
    """
    Parse tokens to a while-loop-node and left-over tokens. When an error occures, the returned node and left-over
    tokens will be None and an empty list.
    :param tokens: List[Token]; Tokens that form a while loop with optional extra tokens after the loop
    :return: While, List[Token], Error; Node with the while loop, left over token, error-object
    """
    expression_tokens, left_over = find_until(tokens[1:], TokensTypes.ENDLINE)

    body_tokens, left_over = find_end(left_over, TokensTypes.WHILE, TokensTypes.ENDWHILE)

    expression, error = get_expression(expression_tokens)
    if error.type != ErrorType.NO_ERROR:
        return None, [], error

    body, error = get_nodes(body_tokens)
    if error.type != ErrorType.NO_ERROR:
        return None, [], error

    return While(expression, body), left_over, Error(ErrorType.NO_ERROR, '')


def parse_if_statement(tokens: List[Token]) -> Tuple[Optional[Node], List[Token], Error]:
    """
    Parse tokens to a if-node and left-over tokens. When an error occures, the returned node and left-over
    tokens will be None and an empty list.
    :param tokens: List[Token]; Tokens that form a if(-else) statement with optional extra tokens after the statement
    :return: While, List[Token], Error; Node with the if/else statement, left over token, error-object
    """
    expression_tokens, left_over = find_until(tokens[1:], TokensTypes.ENDLINE)
    if_else_body_tokens, left_over = find_end(left_over, TokensTypes.IF, TokensTypes.ENDIF)

    if_body, else_body = find_if_else_bodies(if_else_body_tokens)

    if len(if_body) == 0:
        return None, [], Error(ErrorType.SYNTAX_ERROR, f'No if-body found for if-statement at line {tokens[0].line_nmr}')

    expression_node, error = get_compare(expression_tokens)

    if error.type != ErrorType.NO_ERROR:
        return None, [], error

    if_node = If(expression_node)
    if_body_nodes, error = get_nodes(if_body)
    if error.type != ErrorType.NO_ERROR:
        return None, [], error
    if_node.body = if_body_nodes

    else_body_nodes, error = get_nodes(else_body)
    if error.type != ErrorType.NO_ERROR:
        return None, [], error
    if_node.else_body = else_body_nodes

    return if_node, left_over, Error(ErrorType.NO_ERROR, '')


def parse_call_statement(tokens: List[Token]) -> Tuple[Optional[Node], List[Token], Error]:
    """
    Parse tokens to an call statement. Everything from the call-token till line-end is considered a parameter.
    Extra token after the end-line token will be returned as left-over
    :param tokens: List[Token]; Tokens describing a function call with optional extra tokens
    :return: Call, List[Token], Error; Call-node, left over tokens after the call, an error-object
    """
    if tokens[1].type == TokensTypes.IDENTIFIER:
        parameter_tokens, left_over = find_until(tokens[2:], TokensTypes.ENDLINE)
        parameter_error = check_parameters(parameter_tokens)
        if parameter_error.type != ErrorType.NO_ERROR:
            return None, [], parameter_error
        call = Call(tokens[1], parameter_tokens)

        return call, left_over, Error(ErrorType.NO_ERROR, '')

    else:
        return None, [], Error(ErrorType.SYNTAX_ERROR,
                         f'Expected function name at line {tokens[1].line_nmr} but got {tokens[1].value}')


def parse_type_assignment_statement(tokens: List[Token]) -> Tuple[Optional[Node], List[Token], Error]:
    """
    Parse tokens to an call statement. Everything from the type-token till line-end is considered part of the
    assignment. Extra tokens after the end-line token will be returned as left-over
    :param tokens: List[Token]; Tokens describing a type-assignment
    :return: TypeAssignment, List[Token], Error; Type-assignment-node, left over tokens, error-object
    """
    statement_tokens, left_over = find_until(tokens, TokensTypes.ENDLINE)

    statement, error = get_type_assignment(statement_tokens)
    if error.type != ErrorType.NO_ERROR:
        return None, [], error
    return statement, left_over, Error(ErrorType.NO_ERROR, '')


def parse_identifier(tokens: List[Token]) -> Tuple[Optional[Node], List[Token], Error]:
    """
    Parse a token list that starts with an identifier. This can indicate an assignment, unary expression, increment or
    decrement. This code will detect which option is correct and return a Node with the correct expression.
    :param tokens: List[Token]; Token list with the expression and optional extra tokens
    :return: Node, List[Token], Error; Node with correct expression, left-over tokens, error-object
    """
    if tokens[1].type == TokensTypes.ASSIGNMENT:
        expression_tokens, left_over = find_until(tokens[2:], TokensTypes.ENDLINE)

        expression, error = get_expression(expression_tokens)
        if error.type != ErrorType.NO_ERROR:
            return None, [], error

        node = Assignment(tokens[0], expression)

    elif tokens[1].type == TokensTypes.UNARY:
        expression_tokens, left_over = find_until(tokens[2:], TokensTypes.ENDLINE)

        expression, error = get_expression(expression_tokens)
        if error.type != ErrorType.NO_ERROR:
            return None, [], error

        node = Unary(tokens[0], tokens[1], expression)
    elif tokens[1].type == TokensTypes.INCDEC:
        if tokens[2].type == TokensTypes.ENDLINE:
            node = IncDec(tokens[0], tokens[1])
            left_over = tokens[3:]
        else:
            return None, [], Error(ErrorType.STATEMENT_ERROR, f'Invalid statement at line {tokens[0].line_nmr}')
    else:
        return None, [], Error(ErrorType.STATEMENT_ERROR, f'Invalid statement at line {tokens[0].line_nmr}')

    return node, left_over, Error(ErrorType.NO_ERROR, '')


def get_nodes(tokens: List[Token]) -> Tuple[List[Node], Error]:
    """
    Parse a list of tokens to a list of nodes. If an error occurs, the node-list will be empty and the error
    will be given through the error-object
    :param tokens: List[Token]; tokens that need to be parsed
    :return: List[Node], Error; List with nodes, Error-object containing errors
    """
    if len(tokens) <= 0:
        return [], Error(ErrorType.NO_ERROR, '')

    node_parse_functions = {
        TokensTypes.FOR: parse_for_loop,
        TokensTypes.WHILE: parse_while_loop,
        TokensTypes.IF: parse_if_statement,
        TokensTypes.CALL: parse_call_statement,
        TokensTypes.TYPE: parse_type_assignment_statement,
        TokensTypes.IDENTIFIER: parse_identifier
    }

    if tokens[0].type in node_parse_functions:
        node, left_over, error = node_parse_functions[tokens[0].type](tokens)

        if error.type != ErrorType.NO_ERROR:
            return [], error

        if len(left_over) > 0 and left_over[0].type == TokensTypes.ENDLINE:
            left_over = left_over[1:]

        next_nodes, error = get_nodes(left_over)
        if error.type != ErrorType.NO_ERROR:
            return [], error

        return [node, ] + next_nodes, Error(ErrorType.NO_ERROR, '')
    else:
        return [], Error(ErrorType.STATEMENT_ERROR, f'No valid statement could be formed at line {tokens[0].line_nmr}')


def find_function_definition(tokens: List[Token]) -> Tuple[Union[FunctionNode, None], List[Token], Error]:
    """
    Find and parse a function definition from a list of tokens. The list of tokens may contain multiple functions.
    If an error occurs, the FunctionNode will be None and the left-over token list might be empty
    :param tokens: List[Token]; list of tokens containing one or more function descriptions
    :return: FunctionNode, List[Token], Error; FunctionNode that can be called, left-over tokens, Error-object
    """
    if tokens[0].type == TokensTypes.TYPE:
        if tokens[2].type == TokensTypes.IDENTIFIER:
            parameter_list, tokens_after_parameters, error = get_parameter_list(tokens[3:])
            if error.type == ErrorType.NO_ERROR:
                body_tokens, left_over = find_until(tokens_after_parameters, TokensTypes.RETURN)
                if len(left_over) == 0:
                    return None, [], Error(ErrorType.SYNTAX_ERROR, f'No return found in function {tokens[2].value}')
                body_nodes, error = get_nodes(body_tokens)
                if error.type != ErrorType.NO_ERROR:
                    return None, [], error

                return_tokens, left_over = find_until(left_over, TokensTypes.ENDLINE)

                expression, error = get_expression(return_tokens)
                if error.type != ErrorType.NO_ERROR:
                    return None, [], error

                function_node = FunctionNode(tokens[2].value, tokens[0])
                function_node.return_line = return_tokens[0].line_nmr
                function_node.return_statement = expression
                function_node.body = body_nodes
                function_node.parameters = parameter_list

                return function_node, left_over, Error(ErrorType.NO_ERROR, '')

            else:
                return None, tokens_after_parameters, error
        else:
            return None, tokens, Error(ErrorType.INVALID_NAME_ERROR, f'Name \'{tokens[2].value}\' at line {str(tokens[3].line_nmr)} is not a valid name')
    else:
        return None, tokens, Error(ErrorType.UNKNOW_TYPE_ERROR, f'Type \'{tokens[0].value}\' at line {str(tokens[0].line_nmr)} is not valid')


@status_logger('Start parsing program')
def parse(tokens: List[Token]) -> Tuple[Dict[str, FunctionNode], Error]:
    """
    This parses a list of tokens to a dictionary of FunctionNodes indexed by the function names.
    :param tokens: List[Tokens]; A list of tokens that describe one or more functions that can be called
    :return: Dict[str, FunctionNode], Error; Dictionary with function-name as key and FunctionNode as value, Error-object
    """
    result = dict()

    while len(tokens) > 1:
        if tokens[1].type != TokensTypes.FUNCTION:
            return result, Error(ErrorType.SYNTAX_ERROR, f'No valid function definition at line {tokens[1].line_nmr}')

        function_node, left_over, error = find_function_definition(tokens)
        if error.type != ErrorType.NO_ERROR:
            return result, error
        result[function_node.name] = function_node
        tokens = left_over

    # Add build-in functionNodes
    result['print'] = FunctionNode(name='print', return_type=Token(TokensTypes.INT, 'int', -1))
    result['size'] = FunctionNode(name='size', return_type=Token(TokensTypes.INT, 'int', -1))
    result['input'] = FunctionNode(name='input', return_type=Token(TokensTypes.STRING, 'string', -1))

    return result, Error(ErrorType.NO_ERROR, '')