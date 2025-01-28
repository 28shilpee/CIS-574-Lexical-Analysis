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
    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def IDENTIFIER(self, t):
        if len(t.value) > 50:
            print(f"Error: Identifier '{t.value}' exceeds maximum length of 50 characters at line {self.lineno}")
            return None
        if t.value in self.keywords:
            t.type = 'KEYWORD'
        return t

    # Comments
    @_(r'//.*')
    def COMMENT_SINGLE(self, t):
        pass

    @_(r'/\*(.|\n)*?\*/')
    def COMMENT_MULTI(self, t):
        self.lineno += t.value.count('\n')

    # Line number tracking
    @_(r'\n+')
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
    
    print("DLang Lexical Analyzer")
    print("Reading code from 'input.txt'. Please ensure the file exists.")

    try:
        # Open the input file
        with open('input.txt', 'r') as file:
            text = file.read()

        # Tokenize the input
        tokens = lexer.tokenize(text)
        if not tokens:
            print("No tokens found. Please enter valid DLang code.")
        else:
            # Display tokens
            for tok in tokens:
                print(f'type={tok.type}, value={tok.value}')

    except FileNotFoundError:
        print("Error: 'input.txt' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    print("Lexical analysis complete.")