from sly import Lexer

class DLangLexer(Lexer):
    tokens = {'KEYWORD', 'IDENTIFIER', 'BOOLEAN', 'INTEGER', 'DOUBLE', 'STRING', 'OPERATOR'}

    # Ignored characters
    ignore = ' \t\r'

    # Token patterns
    KEYWORD = r'(nothing|int|double|bool|string|class|interface|null|this|extends|implements|for|while|if|else|return|break|new|ArrayInstance|Output|InputInt|InputLine)'
    BOOLEAN = r'(True|False)'
    INTEGER = r'\d+'
    DOUBLE = r'\d+\.(?:\d*([Ee][+-]?\d+)?)?'
    STRING = r'"[^"\n]*"'
    OPERATOR = r'(\+|-|\*|/|%|<=?|>=?|==?|!=|&&|\|\||!|;|,|\.|[\[\](){}])'

    # Identifier pattern with length check
    @(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def IDENTIFIER(self, t):
        if len(t.value) > 50:
            print(f"Error: Identifier '{t.value}' exceeds maximum length of 50 characters at line {self.lineno}")
            return None
        if t.value in self.keywords:
            t.type = 'KEYWORD'
        return t

    # Comments
    @(r'//.*')
    def COMMENT_SINGLE(self, t):
        pass

    @(r'/\*(.|\n)*?\*/')
    def COMMENT_MULTI(self, t):
        self.lineno += t.value.count('\n')

    # Line number tracking
    @(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # Error handling
    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1

    # Priority handling for keywords vs identifiers
    keywords = {'nothing', 'int', 'double', 'bool', 'string', 'class', 'interface', 'null', 'this', 'extends', 'implements', 'for', 'while', 'if', 'else', 'return', 'break', 'new', 'ArrayInstance', 'Output', 'InputInt', 'InputLine'}

if __name__ == '__main__':
    lexer = DLangLexer()
    try:
        while True:
            text = input('dlang > ')
            for tok in lexer.tokenize(text):
                print(f'type={tok.type}, value={tok.value}')
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except EOFError:
        print("\nEOF detected. Exiting.")
    finally:
        print("Lexical analysis complete.")