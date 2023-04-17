import unittest


class IntegrationTest(unittest.TestCase):
    """
    Test the full interpreter against a known input and output
    """
    def test_lexer_parser(self):
        from io import StringIO
        import sys
        from decoder import lexer
        from decoder import parser
        from decoder import nodes
        from decoder import enums
        sys.stdout = StringIO()

        input = [
            ('bool function is_odd int n', 1),
            ('bool result is false', 2),
            ('if n notequals 0', 3),
            ('n minmin', 4),
            ('result is call is_even n', 5),
            ('endif', 6),
            ('return result', 7),
        ]

        tokens, error = lexer.lex_lines(input)
        if error.type != enums.ErrorType.NO_ERROR:
            self.assertEqual(error.type, enums.ErrorType.NO_ERROR, 'An error occured during lexing')

        functions, error = parser.parse(tokens)
        if error.type != enums.ErrorType.NO_ERROR:
            self.assertEqual(error.type, enums.ErrorType.NO_ERROR, 'An error occured during parsing')

        sys.stdout = sys.__stdout__

        is_odd_function = nodes.FunctionNode('is_odd', lexer.Token(enums.TokensTypes.TYPE, 'bool', 1))
        is_odd_function.parameters = [nodes.Parameter(lexer.Token(enums.TokensTypes.TYPE, 'int', 1), 'n')]
        is_odd_function.return_line = 7
        is_odd_function.return_statement = nodes.Value(lexer.Token(enums.TokensTypes.IDENTIFIER, 'result', 7))
        is_odd_function.body = [
            nodes.TypeAssignment(
                lexer.Token(enums.TokensTypes.TYPE, 'bool', 2),
                lexer.Token(enums.TokensTypes.IDENTIFIER, 'result', 2),
                nodes.Value(
                    lexer.Token(enums.TokensTypes.BOOL, 'false', 2)
                )
            ),
            nodes.If(
                nodes.Compare(
                    lexer.Token(enums.TokensTypes.IDENTIFIER, 'n', 3),
                    lexer.Token(enums.TokensTypes.COMPARE, 'notequals', 3),
                    lexer.Token(enums.TokensTypes.INT, '0', 3)
                ),
                [
                    nodes.IncDec(
                        lexer.Token(enums.TokensTypes.IDENTIFIER, 'n', 4),
                        lexer.Token(enums.TokensTypes.INCDEC, 'minmin', 4)
                    ),
                    nodes.Assignment(
                        lexer.Token(enums.TokensTypes.IDENTIFIER, 'result', 5),
                        nodes.Call(
                            lexer.Token(enums.TokensTypes.IDENTIFIER, 'is_even', 5),
                            [
                                lexer.Token(enums.TokensTypes.IDENTIFIER, 'n', 5),
                            ]
                        )
                    )
                ],
                []
            ),
        ]

        expected = {
            'is_odd': is_odd_function,
            'print':  nodes.FunctionNode(name='print', return_type=lexer.Token(enums.TokensTypes.INT, 'int', -1)),
            'size': nodes.FunctionNode(name='size', return_type=lexer.Token(enums.TokensTypes.INT, 'int', -1)),
            'input': nodes.FunctionNode(name='input', return_type=lexer.Token(enums.TokensTypes.STRING, 'string', -1)),
        }


        self.assertEqual(functions, expected, 'Function node was not generated correctly')


if __name__ == '__main__':
    unittest.main()
