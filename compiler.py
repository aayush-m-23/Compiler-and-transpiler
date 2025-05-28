class Lexer:
    def __init__(self, source_code):
        self.code = source_code
        self.tokens = []

    def tokenize(self):
        lines = self.code.strip().splitlines()
        indent_stack = [0]

        for line in lines:
            if not line.strip():
                continue

            stripped = line.lstrip()
            indent = len(line) - len(stripped)

            if indent > indent_stack[-1]:
                self.tokens.append(('INDENT', None))
                indent_stack.append(indent)
            while indent < indent_stack[-1]:
                self.tokens.append(('DEDENT', None))
                indent_stack.pop()

            for op in ['=', '+', '-', '*', '/', '%', '>', '<']:
                stripped = stripped.replace(op, f' {op} ')

            words = stripped.strip().split()
            for word in words:
                if word.isdigit():
                    self.tokens.append(('NUMBER', int(word)))
                elif word in ('let', 'print', 'if', 'else', 'while', 'for', 'to'):
                    self.tokens.append((word.upper(), word))
                elif word in ('=', '+', '-', '*', '/', '%', '>', '<'):
                    self.tokens.append((word, word))
                elif word.isidentifier():
                    self.tokens.append(('IDENTIFIER', word))
                else:
                    raise SyntaxError(f"Unknown token: {word}")
            self.tokens.append(('EOL', None))

        while len(indent_stack) > 1:
            self.tokens.append(('DEDENT', None))
            indent_stack.pop()

        self.tokens.append(('EOF', None))
        return self.tokens
