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
    print("Type your code below. Enter 'exit' to quit or press Ctrl+C to terminate.")

    while True:
        try:
            # Prompt for input
            text = input('dlang > ')
            
            # Exit condition
            if text.strip().lower() == 'exit':
                print("Exiting...")
                break

            # Tokenize the input
            tokens = lexer.tokenize(text)
            if not tokens:
                print("No tokens found. Please enter valid DLang code.")
                continue

            # Display tokens
            for tok in tokens:
                print(f'type={tok.type}, value={tok.value}')

        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
            break
        except EOFError:
            print("\nEOF detected. Exiting.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

    print("Lexical analysis complete.")