import re

class LexicalAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def tokenize(self, input_string):
        tokens = []
        current_token = ''
        for char in input_string:
            if char.isdigit():
                current_token += char
            elif char.isalpha():
                current_token += char
            elif char in ['+', '*', '(', ')']:
                if current_token:
                    tokens.append((current_token, self.get_token_type(current_token)))
                    current_token = ''
                tokens.append((char, char))
            elif char == ' ':
                if current_token:
                    tokens.append((current_token, self.get_token_type(current_token)))
                    current_token = ''
            else:
                print(f"Error: Invalid character '{char}'")
                return None

        if current_token:
            tokens.append((current_token, self.get_token_type(current_token)))

        return tokens

    def get_token_type(self, lexeme):
        if lexeme.isdigit():
            return 'num'
        elif re.match("^[a-zA-Z]+$", lexeme):
            return 'id'
        else:
            return 'unknown'

    def add_to_symbol_table(self, token, lexeme):
        self.symbol_table[token] = lexeme

    def display_symbol_table(self):
        print("\nSymbol Table:")
        for token, lexeme in self.symbol_table.items():
            print(f"{token}: {lexeme}")


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

def print_tree(node, level=0, parent_line='', is_last_child=False):
    if node is not None:
        prefix = '└── ' if is_last_child else '├── '
        print(parent_line + prefix + node.value)
        parent_line += '    ' if is_last_child else '│   '
        num_children = len(node.children)
        for idx, child in enumerate(node.children):
            is_last = idx == num_children - 1
            print_tree(child, level + 1, parent_line, is_last)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.parse_tree = None
        self.error = False
        self.error_message = ""

    def parse(self):
        self.parse_tree = Node('E')
        if self.E(self.parse_tree) and not self.error:
            if self.current_token_index == len(self.tokens):
                return True
        self.error_message = "Invalid input string."
        return False

    def E(self, node):
        node.children.append(Node('T'))
        if self.T(node.children[-1]):
            if self.E_prime(node):
                return True
        return False

    def E_prime(self, node):
        if self.current_token_index < len(self.tokens):
            next_token = self.tokens[self.current_token_index]
            if next_token[1] == '+':
                node.children.append(Node('E\''))
                node.children[-1].children.append(Node('+'))
                self.current_token_index += 1
                node.children[-1].children.append(Node('T'))
                if self.T(node.children[-1].children[-1]):
                    if self.E_prime(node):
                        return True
                self.error_message = f"Error: Two consecutive '+' signs near token '{next_token[0]}'"
                self.error = True
                return False
        return True

    def T(self, node):
        node.children.append(Node('F'))
        if self.F(node.children[-1]):
            if self.T_prime(node):
                return True
        return False

    def T_prime(self, node):
        if self.current_token_index < len(self.tokens):
            next_token = self.tokens[self.current_token_index]
            if next_token[1] == '*':
                node.children.append(Node('T\''))
                node.children[-1].children.append(Node('*'))
                self.current_token_index += 1
                node.children[-1].children.append(Node('F'))
                if self.F(node.children[-1].children[-1]):
                    if self.T_prime(node):
                        return True
                self.error_message = f"Error: Unmatched parentheses near token '{next_token[0]}'"
                self.error = True
                return False
        return True

    def F(self, node):
        if self.current_token_index < len(self.tokens):
            next_token = self.tokens[self.current_token_index]
            if next_token[1] == '(':
                node.children.append(Node('('))
                self.current_token_index += 1
                node.children.append(Node('E'))
                if self.E(node.children[-1]):
                    if self.current_token_index < len(self.tokens):
                        if self.tokens[self.current_token_index][1] == ')':
                            node.children.append(Node(')'))
                            self.current_token_index += 1
                            return True
                        else:
                            self.error_message = f"Error: Unmatched parentheses near token '{next_token[0]}'"
                            self.error = True
                            return False
                    else:
                        self.error_message = "Error: Unmatched parentheses at end of input"
                        self.error = True
                        return False
                else:
                    self.error_message = f"Error: Invalid input near token '{next_token[0]}'"
                    self.error = True
                    return False
            elif next_token[1] == 'id' or next_token[1] == 'num':
                node.children.append(Node(next_token[0]))
                self.current_token_index += 1
                return True
        self.error_message = f"Error: Invalid input near token '{next_token[0]}'"
        self.error = True
        return False

def main():
    lexer = LexicalAnalyzer()
    input_string = input("Enter an input string: ")
    tokens = lexer.tokenize(input_string)
    if tokens:
        print("\nLexemes and Tokens:")
        for lexeme, token in tokens:
            print(f"{lexeme}: {token}")
        lexer.display_symbol_table()
        parser = Parser(tokens)
        if parser.parse():
            print("\nParse Tree:")
            print_tree(parser.parse_tree)
        else:
            print(parser.error_message)


if __name__ == "__main__":
    main()
