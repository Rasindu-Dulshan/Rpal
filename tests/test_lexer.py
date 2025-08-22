import unittest
from src.lexer import Lexer, TokenType, LexerError


class TestLexer(unittest.TestCase):
    def test_identifiers(self):
        lexer = Lexer("x y_z abc123 Abc")
        tokens = lexer.tokenize()

        expected = [
            (TokenType.IDENTIFIER, "x", 1, 1),
            (TokenType.IDENTIFIER, "y_z", 1, 3),
            (TokenType.IDENTIFIER, "abc123", 1, 7),
            (TokenType.IDENTIFIER, "Abc", 1, 14),
            (TokenType.EOF, "", 1, 17),
        ]

        self.assertEqual(len(tokens), len(expected))
        for token, (
            expected_type,
            expected_value,
            expected_line,
            expected_column,
        ) in zip(tokens, expected):
            self.assertEqual(
                token.type, expected_type, f"Token type mismatch for '{token.value}'"
            )
            self.assertEqual(
                token.value, expected_value, f"Token value mismatch for {token.type}"
            )
            self.assertEqual(
                token.line,
                expected_line,
                f"Line mismatch for '{token.value}': expected {expected_line}, got {token.line}",
            )
            self.assertEqual(
                token.column,
                expected_column,
                f"Column mismatch for '{token.value}': expected {expected_column}, got {token.column}",
            )

    def test_integers(self):
        lexer = Lexer("123 456789 0")
        tokens = lexer.tokenize()

        expected = [
            (TokenType.INTEGER, "123", 1, 1),
            (TokenType.INTEGER, "456789", 1, 5),
            (TokenType.INTEGER, "0", 1, 12),
            (TokenType.EOF, "", 1, 13),
        ]

        self.assertEqual(len(tokens), len(expected))
        for token, (
            expected_type,
            expected_value,
            expected_line,
            expected_column,
        ) in zip(tokens, expected):
            self.assertEqual(
                token.type, expected_type, f"Token type mismatch for '{token.value}'"
            )
            self.assertEqual(
                token.value, expected_value, f"Token value mismatch for {token.type}"
            )
            self.assertEqual(
                token.line,
                expected_line,
                f"Line mismatch for '{token.value}': expected {expected_line}, got {token.line}",
            )
            self.assertEqual(
                token.column,
                expected_column,
                f"Column mismatch for '{token.value}': expected {expected_column}, got {token.column}",
            )

    def test_negative_integers(self):
        # Note: '-' and '+' are operators, not part of integer
        lexer = Lexer("-123 +456")
        tokens = lexer.tokenize()

        expected = [
            (TokenType.OPERATOR, "-", 1, 1),
            (TokenType.INTEGER, "123", 1, 2),
            (TokenType.OPERATOR, "+", 1, 6),
            (TokenType.INTEGER, "456", 1, 7),
            (TokenType.EOF, "", 1, 10),
        ]

        self.assertEqual(len(tokens), len(expected))
        for token, (
            expected_type,
            expected_value,
            expected_line,
            expected_column,
        ) in zip(tokens, expected):
            self.assertEqual(token.type, expected_type)
            self.assertEqual(token.value, expected_value)
            self.assertEqual(token.line, expected_line)
            self.assertEqual(token.column, expected_column)

    def test_strings(self):
        # for positioning use this -->  "'hello' 'escaped \' quote' 'new\nline' 'tab\t'"
        lexer = Lexer("'hello' 'escaped \\' quote' 'new\\nline' 'tab\\t'")
        tokens = lexer.tokenize()

        expected = [
            (TokenType.STRING, "'hello'", 1, 1),
            (TokenType.STRING, "'escaped ' quote'", 1, 9),
            (TokenType.STRING, "'new\nline'", 1, 28),
            (TokenType.STRING, "'tab\t'", 1, 40),
            (TokenType.EOF, "", 1, 47),
        ]

        self.assertEqual(len(tokens), len(expected))
        for token, (
            expected_type,
            expected_value,
            expected_line,
            expected_column,
        ) in zip(tokens, expected):
            self.assertEqual(
                token.type, expected_type, f"Token type mismatch for '{token.value}'"
            )
            self.assertEqual(
                token.value, expected_value, f"Token value mismatch for {token.type}"
            )
            self.assertEqual(
                token.line,
                expected_line,
                f"Line mismatch for '{token.value}': expected {expected_line}, got {token.line}",
            )
            self.assertEqual(
                token.column,
                expected_column,
                f"Column mismatch for '{token.value}': expected {expected_column}, got {token.column}",
            )

    def test_strings_multiline(self):
        code = """'first' 'second\\nline'
        'third'"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        expected = [
            (TokenType.STRING, "'first'", 1, 1),
            (TokenType.STRING, "'second\nline'", 1, 9),
            (TokenType.STRING, "'third'", 2, 10),
            (TokenType.EOF, "", 2, 17),
        ]

        self.assertEqual(len(tokens), len(expected))
        for token, (
            expected_type,
            expected_value,
            expected_line,
            expected_column,
        ) in zip(tokens, expected):
            self.assertEqual(token.type, expected_type)
            self.assertEqual(token.value, expected_value)
            self.assertEqual(token.line, expected_line)
            self.assertEqual(token.column, expected_column)

    def test_invalid_escape_sequences(self):
        invalid_cases = [
            (r"'\m'", (1, 2)),
            (r"'\x41'", (1, 2)),
            (r"'\ '", (1, 2)),  # Space after backslash
            (r"'\u263A'", (1, 2)),  # Unicode escape
            ("'good\\nbad\\m'", (1, 11)),  # Valid then invalid
        ]

        for code, (line, col) in invalid_cases:
            with self.subTest(code=code):
                with self.assertRaises(LexerError) as cm:
                    lexer = Lexer(code)
                    lexer.tokenize()
                ex = cm.exception
                self.assertEqual(ex.line, line)
                self.assertEqual(ex.column, col)
                self.assertIn("Invalid escape sequence", str(ex))

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
            (TokenType.EOF, ""),
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
            (TokenType.EOF, ""),
        ]

        self.assertEqual(len(tokens), len(expected))
        for token, (expected_type, expected_value) in zip(tokens, expected):
            self.assertEqual(token.type, expected_type)
            self.assertEqual(token.value, expected_value)

    def test_comments(self):
        lexer = Lexer("x // This is a comment\ny // Another comment\n")
        tokens = lexer.tokenize()

        expected = [
            (TokenType.IDENTIFIER, "x"),
            (TokenType.COMMENT, "// This is a comment"),
            (TokenType.IDENTIFIER, "y"),
            (TokenType.COMMENT, "// Another comment"),
            (TokenType.EOF, ""),
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
            (TokenType.EOF, ""),
        ]

        self.assertEqual(len(tokens), len(expected))
        for token, (expected_type, expected_value) in zip(tokens, expected):
            self.assertEqual(token.type, expected_type)
            self.assertEqual(token.value, expected_value)

    def test_error_handling(self):
        with self.assertRaises(LexerError):
            lexer = Lexer("'\\m'")
            lexer.tokenize()

    def test_unterminated_string(self):
        with self.assertRaises(LexerError):
            lexer = Lexer("'hello")
            lexer.tokenize()


if __name__ == "__main__":
    unittest.main()
