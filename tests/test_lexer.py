import unittest
from src.lexer import Lexer, Token, TokenType


class TestLexer(unittest.TestCase):
    def test_identifiers(self):
        lexer = Lexer("x y_z abc123 _invalid")
        tokens = lexer.tokenize()

        expected = [
            (TokenType.IDENTIFIER, "x"),
            (TokenType.IDENTIFIER, "y_z"),
            (TokenType.IDENTIFIER, "abc123"),
            (TokenType.IDENTIFIER, "_invalid"),
            (TokenType.EOF, "")
        ]

        self.assertEqual(len(tokens), len(expected))
        for token, (expected_type, expected_value) in zip(tokens, expected):
            self.assertEqual(token.type, expected_type)
            self.assertEqual(token.value, expected_value)

    def test_integers(self):
        lexer = Lexer("123 456789 0")
        tokens = lexer.tokenize()

        expected = [
            (TokenType.INTEGER, "123"),
            (TokenType.INTEGER, "456789"),
            (TokenType.INTEGER, "0"),
            (TokenType.EOF, "")
        ]

        self.assertEqual(len(tokens), len(expected))
        for token, (expected_type, expected_value) in zip(tokens, expected):
            self.assertEqual(token.type, expected_type)
            self.assertEqual(token.value, expected_value)

    def test_strings(self):
        lexer = Lexer("'hello' 'escaped \\' quote' 'new\\nline'")
        tokens = lexer.tokenize()

        expected = [
            (TokenType.STRING, "'hello'"),
            (TokenType.STRING, "'escaped \\' quote'"),
            (TokenType.STRING, "'new\\nline'"),
            (TokenType.EOF, "")
        ]

        self.assertEqual(len(tokens), len(expected))
        for token, (expected_type, expected_value) in zip(tokens, expected):
            self.assertEqual(token.type, expected_type)
            self.assertEqual(token.value, expected_value)

    def test_operators(self):
        lexer = Lexer("+ - * / <= >= == != && ||")
        tokens = lexer.tokenize()

        expected = [
            (TokenType.OPERATOR, "+"),
            (TokenType.OPERATOR, "-"),
            (TokenType.OPERATOR, "*"),
            (TokenType.OPERATOR, "/"),
            (TokenType.OPERATOR, "<="),
            (TokenType.OPERATOR, ">="),
            (TokenType.OPERATOR, "=="),
            (TokenType.OPERATOR, "!="),
            (TokenType.OPERATOR, "&&"),
            (TokenType.OPERATOR, "||"),
            (TokenType.EOF, "")
        ]

        self.assertEqual(len(tokens), len(expected))
        for token, (expected_type, expected_value) in zip(tokens, expected):
            self.assertEqual(token.type, expected_type)
            self.assertEqual(token.value, expected_value)

    def test_punctuation(self):
        lexer = Lexer("( ) ; ,")
        tokens = lexer.tokenize()

        expected = [
            (TokenType.LPAREN, "("),
            (TokenType.RPAREN, ")"),
            (TokenType.SEMICOLON, ";"),
            (TokenType.COMMA, ","),
            (TokenType.EOF, "")
        ]

        self.assertEqual(len(tokens), len(expected))
        for token, (expected_type, expected_value) in zip(tokens, expected):
            self.assertEqual(token.type, expected_type)
            self.assertEqual(token.value, expected_value)

    def test_comments(self):
        lexer = Lexer("x // This is a comment\ny // Another comment")
        tokens = lexer.tokenize()

        expected = [
            (TokenType.IDENTIFIER, "x"),
            (TokenType.COMMENT, "// This is a comment"),
            (TokenType.IDENTIFIER, "y"),
            (TokenType.COMMENT, "// Another comment"),
            (TokenType.EOF, "")
        ]

        self.assertEqual(len(tokens), len(expected))
        for token, (expected_type, expected_value) in zip(tokens, expected):
            self.assertEqual(token.type, expected_type)
            self.assertEqual(token.value, expected_value)

    def test_whitespace(self):
        lexer = Lexer("  x   y\tz\nw")
        tokens = lexer.tokenize()

        expected = [
            (TokenType.IDENTIFIER, "x"),
            (TokenType.IDENTIFIER, "y"),
            (TokenType.IDENTIFIER, "z"),
            (TokenType.IDENTIFIER, "w"),
            (TokenType.EOF, "")
        ]

        self.assertEqual(len(tokens), len(expected))
        for token, (expected_type, expected_value) in zip(tokens, expected):
            self.assertEqual(token.type, expected_type)
            self.assertEqual(token.value, expected_value)

    def test_error_handling(self):
        with self.assertRaises(Exception) as context:
            lexer = Lexer("x @$ invalid")
            lexer.tokenize()
        self.assertTrue("Invalid character" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
