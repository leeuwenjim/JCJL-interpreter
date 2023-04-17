from typing import List, NamedTuple, Union
from decoder.lexer import Token


class Node:
    """
    Base class for all nodes
    """
    def __str__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return '[Empty Node]'

    def __repr__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return self.__str__()


    def __eq__(self, other) -> bool:
        """
        Check if an object is equal to self
        :param other: Other object
        :return: bool; are the objects the same
        """
        return isinstance(other, Node) and other.__class__.__name__ == Node.__class__.__name__


class Value(Node):
    """
    Node that represents a value
    """
    def __init__(self, value: Token):
        """
        Initialize the node with a value token
        :param value: Token; value of the node
        """
        self.value = value

    def __str__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return f'[Value Node: {self.value.value}]'

    def __repr__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return self.__str__()

    def __eq__(self, other) -> bool:
        """
        Check if other is the same as this value node
        :param other: Other object to compare
        :return: bool; is other object same as this object
        """
        if not isinstance(other, Value):
            return False
        return self.value == other.value


class Operator(Node):
    """
    Node that represents a operation (plus, min, etc) on two tokens
    """
    def __init__(self, left: Token, operator: Token, right: Token):
        """
        Initialize the operator node with the left, right and oparation
        :param left: Token; left side of the operation
        :param operator: Token; type of operation
        :param right: Token; right side of the operation
        """
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return f'[Operator Node: {self.left.value} {self.operator.value} {self.right.value}]'

    def __repr__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return self.__str__()

    def __eq__(self, other) -> bool:
        """
        Check if other is the same as this operator node
        :param other: Other object to compare
        :return: bool; is other object same as this object
        """
        if not isinstance(other, Operator):
            return False
        return self.left == other.left and self.operator == other.operator and self.right == other.right


class Call(Node):
    """
    This node represents a call to a function
    """
    def __init__(self, function: Token, parameters: List[Token]):
        self.function = function
        self.parameters = parameters

    def get_parameters_as_string(self, p: List[Token]):
        """
        Get parameters represented as a string
        :param p: List[Token]; List of parameters to format
        :return: str; formatted string representing the parameters
        """
        if len(p) == 0: return ''
        return p[0].value + ' ' + self.get_parameters_as_string(p[1:])

    def __str__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return f'[Call Node: {self.function.value}({self.get_parameters_as_string(self.parameters)})]'

    def __repr__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return self.__str__()

    def __eq__(self, other) -> bool:
        """
        Check if other is the same as this node
        :param other: Other object to compare
        :return: bool; is other object same as this object
        """
        if not isinstance(other, Call):
            return False
        return self.function == other.function and self.parameters == other.parameters


class Unary(Node):
    """
    This node represents an unary node where the right side is applied to the left side by the given operator
    """
    def __init__(self, left: Token, operator: Token, right: Node):
        """
        Initialize the unary node
        :param left: Token; Left side of the unary expression
        :param operator: Token; What operation should be applied
        :param right: Token; right side of the unary expression
        """
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return f'[Unary Node: {self.left.value} {self.operator.value} {self.right}]'

    def __repr__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return self.__str__()

    def __eq__(self, other) -> bool:
        """
        Check if other is the same as this node
        :param other: Other object to compare
        :return: bool; is other object same as this object
        """
        if not isinstance(other, Unary):
            return False
        return self.left == other.left and self.operator == other.operator and self.right == other.right


class IncDec(Node):
    """
    Node that represents an increment or decrement a token
    """
    def __init__(self, left: Token, operator: Token):
        """
        Initialize the IncDec node
        :param left: Token; what should be incremented or decremented
        :param operator: Token; Should the left side be incremented or decremented
        """
        self.left = left
        self.operator = operator

    def __str__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return f'[IncDec Node: {self.left.value} {self.operator.value}]'

    def __repr__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return self.__str__()

    def __eq__(self, other) -> bool:
        """
        Check if other is the same as this node
        :param other: Other object to compare
        :return: bool; is other object same as this object
        """
        if not isinstance(other, IncDec):
            return False
        return self.operator == other.operator and self.left == other.left


class TypeAssignment(Node):
    """
    Node that assigns a new identifier with an expression
    """
    def __init__(self, type: Token, id: Token, expression: Node):
        """
        Initialize the type assignment
        :param type: Token; type of the new identifier
        :param id: Token; identifier token
        :param expression: Node; expression for the new identifier
        """
        self.type = type
        self.id = id
        self.expression = expression

    def __str__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return f'[TypeAssignment Node: {self.type.value} {self.id.value} is {self.expression}]'

    def __repr__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return self.__str__()

    def __eq__(self, other) -> bool:
        """
        Check if other is the same as this node
        :param other: Other object to compare
        :return: bool; is other object same as this object
        """
        if not isinstance(other, TypeAssignment):
            return False
        return self.type == other.type and self.id == other.id and self.expression == other.expression


class Assignment(Node):
    """
    Assign new value to a identifier
    """
    def __init__(self, id: Token, expression: Node):
        """
        Initialize the assignment node
        :param id: Token; identifier that a new value needs to be assigned to
        :param expression: Node; expression with the new value
        """
        self.id = id
        self.expression = expression

    def __str__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return f'[Assignment Node: {self.id.value} is {self.expression}]'

    def __repr__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return self.__str__()

    def __eq__(self, other) -> bool:
        """
        Check if other is the same as this node
        :param other: Other object to compare
        :return: bool; is other object same as this object
        """
        if not isinstance(other, Assignment):
            return False
        return self.id == other.id and self.expression == other.expression


class Compare(Node):
    """
    Compare node that expresses a comparison between two tokens
    """
    def __init__(self, left: Token, operator: Token, right: Token):
        """
        Initialize the compare node
        :param left: Token; left side of the comparison
        :param operator: Token; comparison type
        :param right: Token; right side of the comparison
        """
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return f'[Compare Node: {self.left.value} {self.operator.value} {self.right.value}]'

    def __repr__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return self.__str__()

    def __eq__(self, other) -> bool:
        """
        Check if other is the same as this node
        :param other: Other object to compare
        :return: bool; is other object same as this object
        """
        if not isinstance(other, Compare):
            return False
        return self.left == other.left and self.operator == other.operator and self.right == other.right


class Forloop(Node):
    """
    Node that represents a for-loop
    """
    def __init__(self, start: TypeAssignment, dowhile: Compare, inc: Node, body: List[Node] = None):
        """
        Initialize the for loop node
        :param start: TypeAssignment; with what variable should the forloop start
        :param dowhile: Compare; comparison that expresses if the forloop should still run
        :param inc: Node; expression that is run after every forloop
        :param body: List[Node]; Nodes that must be executed for every loop
        """
        self.start = start
        self.dowhile = dowhile
        self.inc = inc
        self.body: List[Node] = body if body is not None else []

    def add_node(self, n: Node):
        """
        Add a node to the body of the forloop
        :param n: Node; Node to be added
        """
        self.body.append(n)

    def nodes_as_string(self, nodes: List[Node]) -> str:
        """
        Format given nodes as a string
        :param nodes: List[Node]; Nodes which must be given as a string
        :return str; string representing the given nodes
        """
        if len(nodes) == 0: return ''
        return f'\t{nodes[0]}\n{self.nodes_as_string(nodes[1:])}'

    def __str__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return f'[For Node: start = {self.start}; while = {self.dowhile}; increment = {self.inc}; body = \n{self.nodes_as_string(self.body)}]'

    def __eq__(self, other) -> bool:
        """
        Check if other is the same as this node
        :param other: Other object to compare
        :return: bool; is other object same as this object
        """
        if not isinstance(other, Forloop):
            return False
        return self.start == other.start and self.dowhile == other.dowhile and self.inc == other.inc and self.body == other.body


class While(Node):
    """
    Node representing a while loop
    """
    def __init__(self, dowhile: Node, body: List[Node] = None):
        """
        Initialize the while loop
        :param dowhile: Node; for how long should the while loop be executed
        :param body: List[Node]; List of nodes that must be run for every iteration
        """
        self.dowhile = dowhile
        self.body = body if body is not None else []

    def add_node(self, n: Node):
        """
        Add a node to body of the while loop
        :param n: Node; Node to be added
        """
        self.body.append(n)

    def nodes_as_string(self, nodes: List[Node]) -> str:
        """
        Represent given nodes as a string
        :param nodes: List[Node]; List of nodes to be represented in a string
        :return: str; String representation of the nodes
        """
        if len(nodes) == 0: return ''
        return f'\t{nodes[0]}\n{self.nodes_as_string(nodes[1:])}'

    def __str__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return f'[While Node: while = {self.dowhile}; body = \n{self.nodes_as_string(self.body)}]'

    def __eq__(self, other) -> bool:
        """
        Check if other is the same as this node
        :param other: Other object to compare
        :return: bool; is other object same as this object
        """
        if not isinstance(other, While):
            return False
        return self.dowhile == other.dowhile and self.body == other.__getattribute__()


class If(Node):
    """
    Node representing a if-statement
    """
    def __init__(self, cmp: Compare, body: List[Node] = None, else_body: List[Node] = None):
        """
        Initialize the if statement node
        :param cmp: Compare; statement to check which block must be executed
        :param body: List[Node]; List of nodes for the if-body
        :param else_body: List[Node]; List of nodes for the else-body
        """
        self.cmp = cmp
        self.body = body if body is not None else []
        self.else_body = else_body if else_body is not None else []

    def add_if_node(self, n: Node):
        """
        Add node to the if body
        :param n: Node; Node to be added
        """
        self.body.append(n)

    def add_else_node(self, n: Node):
        """
        Add node to the else body
        :param n: Node; Node to be added
        """
        self.else_body.append(n)

    def nodes_as_string(self, nodes: List[Node]) -> str:
        """
        Represent given nodes as a string
        :param nodes: List[Node]; List of nodes to be represented in a string
        :return: str; String representation of the nodes
        """
        if len(nodes) == 0: return ''
        return f'\t{nodes[0]}\n{self.nodes_as_string(nodes[1:])}'

    def __str__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return f'[If Node: condition = {self.cmp}; if_body = \n{self.nodes_as_string(self.body)}else_body = \n{self.nodes_as_string(self.else_body)}]'

    def __eq__(self, other) -> bool:
        """
        Check if other is the same as this node
        :param other: Other object to compare
        :return: bool; is other object same as this object
        """
        if not isinstance(other, If):
            return False
        return self.cmp == other.cmp and self.body == other.body and self.else_body == other.else_body


class Parameter(NamedTuple):
    """
    Named Tuple representing a parameter with a type and a name
    """
    type: Token
    name: str

    def __eq__(self, other) -> bool:
        """
        Check if other is the same as this parameter
        :param other: Other object to compare
        :return: bool; is other object same as this object
        """
        if not isinstance(other, Parameter):
            return False
        return self.type == other.type and self.name == other.name


class FunctionNode:
    """
    Function node that has a body that is executed, return statement and
    """
    def __init__(self, name: str, return_type: Token):
        """
        Initialize the function node
        :param name: str; Name of the function definition
        :param return_type: Token; What type does the function return
        """
        self.name: str = name
        self.parameters: List[Parameter] = []
        self.return_type: Token = return_type
        self.return_line: int = 0
        self.body: List[Node] = []
        self.return_statement: Union[Node, None] = None

    def add_parameter(self, p: Parameter):
        """
        Add a parameter to the function
        :param p: Parameter; What parameter must be added
        """
        self.parameters.append(p)

    def add_node(self, n: Node):
        """
        Add a node to the function body
        :param n: Node; Node that must be added
        """
        self.body.append(n)

    def set_return(self, n: Node):
        """
        Set the return statement
        :param n: Node; new return statement
        """
        self.return_statement = n

    def nodes_as_string(self, nodes: List[Node]) -> str:
        """
        Represent given nodes as a string
        :param nodes: List[Node]; List of nodes to be represented in a string
        :return: str; String representation of the nodes
        """
        if len(nodes) == 0: return ''
        return f'\t{nodes[0]}\n{self.nodes_as_string(nodes[1:])}'

    def __str__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return f'(FunctionNode name = {self.name}; return = {self.return_statement}; body=\n{self.nodes_as_string(self.body)})'

    def __repr__(self):
        """
        Represent the node as a string
        :return: str; node representation
        """
        return self.__str__()

    def __eq__(self, other) -> bool:
        """
        Check if other is the same as this function node
        :param other: Other object to compare
        :return: bool; is other object same as this object
        """
        if not isinstance(other, FunctionNode):
            return False
        return self.name == other.name and \
            self.parameters == other.parameters and \
            self.return_type == other.return_type and \
            self.return_line == other.return_line and \
            self.return_statement == other.return_statement and \
            self.body == other.body