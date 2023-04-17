import os
from typing import List, Tuple, Union
from decoder.utils import status_logger
from decoder.enums import ErrorType
from decoder.utils import Error


def process_line(line: str) -> str:
    '''
    This functions processes a single JCJL line. All unnecessary whitespace is deleted and also lines that are comments or empty
    :param line: str; Line to be processed
    :return: str; processed line
    '''
    line = line.strip()
    if line.startswith('comment'):
        line = ''
    return line


def process_lines(lines: List[str], line_number) -> List[Tuple[str, int]]:
    '''
    This function processes all lines of a JCJL program
    :param lines: list; List of JCJL program lines
    :return: str; Single string that contains the cleaned up program
    '''
    if len(lines) < 1:
        []
    if len(lines) == 1:
        if len(lines[0].strip()) > 0:
            return [(process_line(lines[0]), line_number), ]
        else:
            return []
    processed_line = process_line(lines[0])

    result = list()
    if processed_line:
        result.append((processed_line, line_number))
    return result + process_lines(lines[1:], line_number+1)


@status_logger('Start reading in file')
def read_program(file: str) -> Union[List[Tuple[str, int]], Error]:
    '''
    This functions reads and processes a JCJL program from a file. Throws a file not found error if the file couldn't be found
    :param file: str; File to be processed
    :return: List[Tuple[str, int]] | Error; This function returns a list of lines, including line numbers, as a tuple. Or an error will be returned
    '''
    if not os.path.isfile(file):
        return Error(ErrorType.FILE_NOT_FOUND_ERROR, f'Couldn\'t find file: {file}')

    if not os.path.exists(file):
        return Error(ErrorType.FILE_NOT_FOUND_ERROR, f'Couldn\'t find file: {file}')


    lines = []
    with open(file, 'r') as program_file:
        lines = program_file.readlines()

    program = process_lines(lines, 1)
    return program
