from typing import Callable, List, TypeVar, Optional, Any
from decoder.enums import ErrorType
from functools import wraps


class Error():
    """
    Generic error class that can be used to format errors
    """
    def __init__(self, type: ErrorType, message: str):
        """
        Initialize an error-object
        :param type: ErrorType; type of error
        :param message: str; message of the error
        """
        self.type = type
        self.message = message

    def __str__(self) -> str:
        """
        Get the error as a string
        :return: str; formatted error
        """
        return f'{self.type.value}: \n{self.message}'

    def __repr__(self) -> str:
        """
        Get the representation of the error as a string
        :return: str; formatted error
        """
        return self.__str__()


# Define generic types
A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')


def literal_identifier_function_looper(function_list: List[Callable[[A, B], Optional[C]]], a: A, b: B) -> Optional[C]:
    """
    Iterate over a list of functions to find the first function call that is not None. If all function return None with
    the given parameters, the result will be None.
    :param function_list: List[Callable]; List of functions that all take the same two parameters and return the same type
    :param a: First parameter of generic type
    :param b: Second parameter of generic type
    :return: Type is defined by the given functions
    """
    if len(function_list) == 0:
        return None
    if len(function_list) == 1:
        return function_list[0](a, b)
    result = function_list[0](a, b)
    return result if result is not None else literal_identifier_function_looper(function_list[1:], a, b)


def status_logger(message: str) -> Callable:
    """
    This decorator logs a message to the console when a function is called. Message is given as a parameter
    :param message: str; the message that must be logged when the decorated function is called
    :return: function decorator
    """
    def outer_wrapper(func: Callable) -> Callable:
        """
        Function wrapper
        :param func: Callable; The function that will be decorated
        :return: Callable; Function that will run the decorated function after printing the message
        """
        @wraps(func)
        def inner_wrapper(*args, **kwargs) -> Any:
            """
            This function prints the message before calling the function
            :param args: given arguments
            :param kwargs: given keyword arguments
            :return: result of the decorated function
            """
            print(message)
            return func(*args, **kwargs)
        return inner_wrapper
    return outer_wrapper
