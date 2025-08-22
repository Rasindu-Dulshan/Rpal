from enum import Enum, auto


class TokenType(Enum):
    IDENTIFIER = auto()
    INTEGER = auto()
    OPERATOR = auto()
    STRING = auto()
    LPAREN = auto()
    RPAREN = auto()
    SEMICOLON = auto()
    COMMA = auto()
    COMMENT = auto()
    WHITESPACE = auto()
    EOF = auto()


class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f"Token({self.type.name}, '{self.value}', {self.line}, {self.column})"

    def __repr__(self):
        return self.__str__()


class LexerError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"{message} at line {line}, column {column}")
        self.line = line
        self.column = column


class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def tokenize(self):
        while self.position < len(self.source_code):
            current_char = self.source_code[self.position]

            # Skip whitespace (but track position)
            if current_char in " \t":
                self._advance()
                continue

            # Handle newlines
            if current_char == "\n":
                self.line += 1
                self.column = 1
                self._advance()
                continue

            # Handle inline comments
            if current_char == "/" and self._peek() == "/":
                self._handle_comment()
                continue

            # Handle strings
            # only handle sigle quoted string
            if current_char == "'":
                self._handle_string()
                continue

            # Handle identifiers
            # _abc this is invalid identifier should always start with a letter
            if current_char.isalpha():
                self._handle_identifier()
                continue

            # Handle integers
            if current_char.isdigit():
                self._handle_integer()
                continue

            # Handle punctuation
            if current_char in "(),;":
                self._handle_punctuation(current_char)
                continue

            # Handle operators
            if current_char in {
                "+",
                "-",
                "*",
                "<",
                ">",
                "&",
                ".",
                "@",
                "/",
                ":",
                "=",
                "~",
                "|",
                "$",
                "!",
                "#",
                "%",
                "_",
                "^",
                "[",
                "]",
                "{",
                "}",
                '"',
                "`",
                "?",
            }:
                self._handle_operator()
                continue

            # If we get here, it's an invalid character
            raise LexerError(
                f"Invalid character '{current_char}'", self.line, self.column
            )

        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens

    def _advance(self):
        self.position += 1
        self.column += 1

    def _peek(self, lookahead=1):
        if self.position + lookahead >= len(self.source_code):
            return None
        return self.source_code[self.position + lookahead]

    def _handle_comment(self):
        start_line = self.line
        start_column = self.column
        value = "//"
        self._advance()  # Skip first /
        self._advance()  # Skip second /

        # Consume until end of line
        while (
            self.position < len(self.source_code)
            and self.source_code[self.position] != "\n"
        ):
            value += self.source_code[self.position]
            self._advance()

        self.tokens.append(Token(TokenType.COMMENT, value, start_line, start_column))

    def _handle_string(self):
        start_line = self.line
        start_column = self.column
        value = "'"
        self._advance()  # Skip opening quote

        while self.position < len(self.source_code):
            current_char = self.source_code[self.position]

            # Handle escape sequences
            # check current char is blackslash not double backslash
            # in python "abc\\" means abc\ (string)
            if current_char == "\\":
                escape_start_col = self.column
                self._advance()  # Skip the backslash

                if self.position >= len(self.source_code):
                    raise LexerError(
                        "Unterminated escape sequence", self.line, escape_start_col
                    )

                next_char = self.source_code[self.position]
                escape_map = {"t": "\t", "n": "\n", "\\": "\\", "'": "'"}

                if next_char in escape_map:
                    # Add the actual escaped character
                    value += escape_map[next_char]
                    self._advance()  # Skip the escaped character
                else:
                    raise LexerError(
                        f"Invalid escape sequence '\\{next_char}'",
                        self.line,
                        escape_start_col,
                    )
                continue

            # Check for closing quote
            if current_char == "'":
                value += "'"
                self._advance()
                self.tokens.append(
                    Token(TokenType.STRING, value, start_line, start_column)
                )
                return

            # Add regular characters
            value += current_char
            self._advance()

        # If we get here, we didn't find a closing quote
        raise LexerError("Unterminated string", start_line, start_column)

    def _handle_identifier(self):
        start_line = self.line
        start_column = self.column
        value = self.source_code[self.position]
        self._advance()

        while self.position < len(self.source_code):
            current_char = self.source_code[self.position]
            if current_char.isalnum() or current_char == "_":
                value += current_char
                self._advance()
            else:
                break

        self.tokens.append(Token(TokenType.IDENTIFIER, value, start_line, start_column))

    def _handle_integer(self):
        start_line = self.line
        start_column = self.column
        value = self.source_code[self.position]
        self._advance()

        while self.position < len(self.source_code):
            current_char = self.source_code[self.position]
            if current_char.isdigit():
                value += current_char
                self._advance()
            else:
                break

        self.tokens.append(Token(TokenType.INTEGER, value, start_line, start_column))

    def _handle_punctuation(self, char):
        token_type = {
            "(": TokenType.LPAREN,
            ")": TokenType.RPAREN,
            ";": TokenType.SEMICOLON,
            ",": TokenType.COMMA,
        }.get(char)

        if token_type is None:
            raise LexerError(f"Unexpected punctuation '{char}'", self.line, self.column)

        self.tokens.append(Token(token_type, char, self.line, self.column))
        self._advance()

    def _handle_operator(self):
        start_line = self.line
        start_column = self.column
        value = self.source_code[self.position]
        self._advance()

        # Handle multi-character operators (like '>=', '<=', '==', etc.)
        while self.position < len(self.source_code):
            current_char = self.source_code[self.position]
            if current_char in {
                "+",
                "-",
                "*",
                "<",
                ">",
                "&",
                ".",
                "@",
                "/",
                ":",
                "=",
                "~",
                "|",
                "$",
                "!",
                "#",
                "%",
                "_",
                "^",
                "[",
                "]",
                "{",
                "}",
                '"',
                "`",
                "?",
            }:
                value += current_char
                self._advance()
            else:
                break

        self.tokens.append(Token(TokenType.OPERATOR, value, start_line, start_column))
